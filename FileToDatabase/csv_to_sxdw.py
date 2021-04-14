
# -*- coding:utf-8 -*-

import config as cfg
import os
import psycopg2
import pandas as pd


# 编写sql语句，连接数据库并写入数据
sql = "select count(*), max(id) from %s" % cfg.TABLE_SXDW

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

for file in os.listdir(cfg.SXDW_SOURCE_DIR):

    print(file)

    # 文件路径
    file_path = cfg.SXDW_SOURCE_DIR + '/' + file

    with open(file_path, 'r') as f:

            sxdws = pd.read_csv(file_path).values

            for sxdw in sxdws:
                # 唯一标识号
                cur_id += 1

                # sxdw标识号
                id_sxdw = sxdw[0]

                freq_down = sxdw[3]

                freq_down_unit = sxdw[4]

                batchnumber = sxdw[5]

                true_value_lon = sxdw[6]

                true_value_lat = sxdw[7]

                true_value_error = sxdw[8]

                result_confidence = sxdw[9]

                false_value_lon = sxdw[10]

                false_value_lat = sxdw[11]

                freq_up = sxdw[12]

                freq_up_unit = sxdw[13]

                multi_access_mode = sxdw[14]

                modulate_pattern = sxdw[15]

                code_mode = sxdw[16]

                bandwidth = sxdw[17]

                bandwidth_unit = sxdw[18]

                sps = sxdw[19]

                sps_unit = sxdw[20]

                medial_sat_norad = sxdw[21]

                adjacent_sat_norad1 = sxdw[22]

                adjacent_sat_norad2 = sxdw[23]

                arrival_time = sxdw[1] + ' ' + sxdw[2]

                # 编写sql语句，连接数据库并写入数据
                sql = "insert into %s (id, id_sxdw, arrival_time, freq_down, freq_down_unit, batchnumber, true_value_lon, "\
                          "true_value_lat, true_value_error, result_confidence, false_value_lon, false_value_lat," \
                          "freq_up, freq_up_unit, multi_access_mode, modulate_pattern, code_mode, bandwidth," \
                          "bandwidth_unit, sps, sps_unit, medial_sat_norad, adjacent_sat_norad1, adjacent_sat_norad2) " % cfg.TABLE_SXDW + \
                          "values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
                          "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (cur_id, id_sxdw, arrival_time,
                          freq_down, freq_down_unit, batchnumber, true_value_lon, true_value_lat, true_value_error, result_confidence,
                          false_value_lon, false_value_lat, freq_up, freq_up_unit, multi_access_mode, modulate_pattern, code_mode,
                          bandwidth, bandwidth_unit, sps, sps_unit, medial_sat_norad, adjacent_sat_norad1, adjacent_sat_norad2)

                cur.execute(sql)


# conn.commit()
conn.close()




































































