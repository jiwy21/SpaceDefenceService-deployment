
# -*- coding:utf-8 -*-

import config as cfg
import struct
from datetime import date
import os
import psycopg2
from Utils.snr_estimate import snr_estimate
from Utils.fc_bw_estimate import fc_bw_estimate
from Utils.code_rate_estimate import code_rate_estimate
from Utils.mod_recognition import mod_recognition
import numpy as np

# 编写sql语句，连接数据库并写入数据
sql = "select count(*), max(id) from %s" % cfg.TABLE_ZPSX

conn = psycopg2.connect(database=cfg.DATABASE, user=cfg.USER, password=cfg.PASSWORD_DB,
                        host=cfg.SERVER_IP, port=cfg.PORT_DB)
cur = conn.cursor()
cur.execute(sql)
res = cur.fetchall()[0]
if res[0] == 0:
    cur_id = 0
else:
    cur_id = res[1]


I = []
Q = []

for file in os.listdir(cfg.ZPSX_SOURCE_DIR):

    print(file)
    cur_dir = cfg.ZPSX_DEST_DIR + file.split('.')[0] + '/'
    if not os.path.exists(cur_dir):
        os.mkdir(cur_dir)

    # 文件路径
    file_path = cfg.ZPSX_SOURCE_DIR + '/' + file

    with open(file_path, 'rb') as f:

        while True:

            # 包头32字节
            head_package = f.read(32)
            if len(head_package) < 32:
                break

            # 时隙计数
            count = f.read(4)
            count_resolved = struct.unpack('i', count)[0]

            # 时隙数据分包的总包数
            packages = f.read(2)
            packages_resolved = struct.unpack('H', packages)[0]

            # 时隙数据分包的包序号
            serial = f.read(2)
            serial_resolved = struct.unpack('H', serial)[0]

            # 所属卫星
            satellite = f.read(1)
            satellite_resolved = struct.unpack('B', satellite)[0]

            # 数据对应日期
            d = f.read(2)
            date_resolved = struct.unpack('H', d)[0]

            # 数据对应开始时间
            start = f.read(4)
            start_resolved = struct.unpack('i', start)[0]

            # 数据的持续时间
            duration = f.read(4)
            duration_resolved = struct.unpack('i', duration)[0]

            # 下行频点
            freq_down = f.read(4)
            freq_down_resolved = struct.unpack('i', freq_down)[0]

            # 频点单位
            freq_unit = f.read(1)
            freq_unit_resolved = struct.unpack('B', freq_unit)[0]

            # 保留1
            retain1 = f.read(4)
            retain1_resolved = struct.unpack('i', retain1)[0]

            # 保留2
            retain2 = f.read(4)
            retain2_resolved = struct.unpack('i', retain2)[0]

            # 数据有效长度
            length = f.read(2)
            length_resolved = struct.unpack('H', length)[0]

            # 时隙数据体解析
            for n in range(0, length_resolved // 8):
                i = struct.unpack('f', f.read(4))[0]
                q = struct.unpack('f', f.read(4))[0]

                I.append(i)
                Q.append(q)

            # 某时隙数据体末尾数据不足1024，则跳过补齐的数据
            if length_resolved < 1024:
                f.seek(1024 - length_resolved, 1)

            # 若到达时隙数据末尾，则进行参数估计及解析入库
            if serial_resolved == packages_resolved:

                # 如果包数太少，则不入库
                # if packages_resolved < cfg.MIN_PACKAGES:
                #     print('Alert too few packages, file: %s, count: %s, packages: %s'
                #           % (file, count_resolved, packages_resolved))
                #     I = []
                #     Q = []
                #     continue

                # 日期（YYYY-mm-dd）
                arrival_date = str(date.fromordinal(date_resolved + cfg.DAYS_DELTA))

                # 开始时间（HH：MM：SS）
                total_second = start_resolved / 10000
                total_hour   = total_second / 3600
                hour         = int(total_hour)
                res_minute   = (total_hour - hour) * 60
                minute       = int(res_minute)
                res_second   = (res_minute - minute) * 60
                # second       = int(res_second)
                # microsecond  = res_second - second

                # 转换为（YYYY-mm-dd HH:MM:SS）形式到达时间
                arrival_time = '%s %02d:%02d:%2.4f' \
                               % (arrival_date, hour, minute, res_second)

                # 下行频率及单位（kHz）
                freq_map = {0: 'unknown', 1: 'Hz', 2: 'kHz', 3: 'MHz', 4: 'GHz', 5: 'else'}
                freq_unit_resolved = freq_map[freq_unit_resolved]
                down_freq = freq_down_resolved

                # 比特率（bps）
                bit_rate = ((packages_resolved - 1) * 1024 + length_resolved) / 2 * 8 \
                    / (duration_resolved * 1e-4)
                bit_rate = float('%.4f' % bit_rate)

                # 采样率（Hz）
                fs_rate = ((packages_resolved - 1) * 128 + length_resolved / 8) / (duration_resolved * 1e-4)

                # 带宽（Hz）
                # alpha = 0.16  # alpha为低通滤波器滚降系数，取值一般不小于0.15
                # band_width = (1 + alpha) * code_rate
                band_width = 25000

                # 信噪比（dB）
                signal = []
                for i in range(len(I)):
                    signal.append(complex(I[i], Q[i]))
                if len(signal) < cfg.N_SNR * cfg.K_SNR:
                    snr = -1

                    print('Alert too few packages, file: %s, count: %s, packages: %s'
                          % (file, count_resolved, packages_resolved))
                else:
                    snr = snr_estimate(signal)
                # print(snr)

                # 频点（Hz）
                [freq_carrier, band_width_x] = fc_bw_estimate(signal, fs_rate)
                # print(freq_carrier)

                # 码速率（Hz）
                # m = 4  # m为单位码元对应的比特数，调制方式为QPSK时，m = 4
                # code_rate = bit_rate / (math.log(m) / math.log(2))
                code_rate = code_rate_estimate(iq=signal, a=cfg.SCALE, fs=fs_rate)
                # print(code_rate)

                # 调制模式
                modulation_mode = mod_recognition(iq=signal, fs=fs_rate)
                # print(modulation_mode)

                # 打印输出
                # print(file, count_resolved, sep=":")
                # print("arrival_time: ", arrival_time, type(arrival_time))
                # print("down_freq(kHz): ", down_freq, type(down_freq))
                # print("bit_rate(bps): ", bit_rate, type(bit_rate))
                # print("code_rate(Hz): ", code_rate, type(code_rate))
                # print("band_width(Hz): ", band_width, type(band_width))
                # print("count: ", count_resolved, type(count_resolved))
                # print("packages: ", packages_resolved, type(packages_resolved))
                # print("satellite: ", satellite_resolved, type(satellite_resolved))
                # print("duration: ", duration_resolved, type(duration_resolved))
                # print("length of IQ: ", len(I), type(I))

                cur_id += 1
                iqlocation = cur_dir + arrival_date + '_' + str(count_resolved) + '_' + str(cur_id) + '.npy'

                # 编写sql语句，连接数据库并写入数据
                sql = "insert into %s (id, count, packages, satellite, duration, freq_down, freq_unit, iqlocation, iqlen, " \
                      "bitrate, coderate, bandwidth, arrival_time, fs_rate, snr, freq_carrier, modulation_mode)" % cfg.TABLE_ZPSX + " values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
                      "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (cur_id, count_resolved, packages_resolved, satellite_resolved, duration_resolved,
                      down_freq, freq_unit_resolved, iqlocation, len(I), bit_rate, code_rate, band_width, arrival_time, fs_rate, snr, freq_carrier, modulation_mode)
                cur.execute(sql)

                # IQ路数据落盘
                IQ = [I, Q]
                IQ_np = np.array(IQ)
                np.save(iqlocation, IQ_np)

                # IQ数据展示
                # plt.figure()
                # plt.subplot(2, 1, 1)
                # plt.plot(I)
                # plt.subplot(2, 1, 2)
                # plt.plot(Q)
                # plt.show()

                I = []
                Q = []

    # 每一个文件处理完成向数据库提交一次
    conn.commit()

# 所有文件都处理完关闭数据库连接
conn.close()












































