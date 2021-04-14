
import datetime
import psycopg2
import config as cfg
from Model.service_meta import IntermediateMeta, IQMeta, SXDWMeta
import numpy as np
import time


class ServiceDblink(object):

    def __init__(self):
        pass

    @staticmethod
    def query_intermediate_list(seek_start, seek_end):
        """
        :param seek_start: str
        :param seek_end: str
        :return:
        """
        # 将date、seek_start、seek_end字符串转为date、time格式
        # seek_start_query = datetime.strptime(seek_start, '%Y-%m-%d %H:%M:%S')
        # seek_end_query = datetime.strptime(seek_end, '%Y-%m-%d %H:%M:%S')

        # 编写sql语句
        sql = "select id, count, packages, satellite, arrival_time, duration, freq_down, \
              freq_unit, iqlocation, iqlen, bitrate, coderate, bandwidth, fs_rate, snr, freq_carrier, modulation_mode " \
              "from %s where arrival_time between '%s' and '%s'" % (cfg.TABLE_ZPSX, seek_start, seek_end)

        # 连接数据库
        conn = psycopg2.connect(database=cfg.DATABASE, user=cfg.USER, password=cfg.PASSWORD_DB,
                                host=cfg.SERVER_IP, port=cfg.PORT_DB)
        cur = conn.cursor()
        cur.execute(sql)
        zpsxs = cur.fetchall()
        conn.close()

        # 格式化中频数据
        zpsxs_uni = []
        for zpsx in zpsxs:
            zpsxs_uni.append(IntermediateMeta(id=zpsx[0], count=zpsx[1], packages=zpsx[2], satellite=zpsx[3],
                                              arrival_time=zpsx[4], duration=zpsx[5], freq_down=zpsx[6],
                                              freq_unit=zpsx[7], iqlocation=zpsx[8], iqlen=zpsx[9], bitrate=zpsx[10],
                                              coderate=zpsx[11], bandwidth=zpsx[12], fs_rate=zpsx[13], snr=zpsx[14],
                                              freq_carrier=zpsx[15], modulation_mode=zpsx[16]))

        return zpsxs_uni

    @staticmethod
    def query_intermediate_iq(id_zpsx):
        """
        :param id_zpsx: 中频时隙数据编号
        :return:
        """

        # 编写sql语句
        sql = "select iqlocation from %s where id=%s" % (cfg.TABLE_ZPSX, id_zpsx)

        # 连接数据库
        conn = psycopg2.connect(database=cfg.DATABASE, user=cfg.USER, password=cfg.PASSWORD_DB,
                                host=cfg.SERVER_IP, port=cfg.PORT_DB)
        cur = conn.cursor()
        cur.execute(sql)
        iqlocation = cur.fetchall()[0][0].strip()
        conn.close()

        # 从文件读取iq两路数据并格式化
        iq = np.load(iqlocation).tolist()
        iq_uni = []
        iq_uni.append(IQMeta(iq[0], iq[1]))

        return iq_uni

    @staticmethod
    def query_intermediate_list_sxdw(seek_time):
        """
        :param seek_time: str
        :return:
        """
        # 将date、seek_start、seek_end字符串转为date、time格式
        # seek_start_query = datetime.strptime(seek_start, '%Y-%m-%d %H:%M:%S')
        # seek_end_query = datetime.strptime(seek_end, '%Y-%m-%d %H:%M:%S')

        seek_time_date = datetime.datetime.strptime(seek_time, '%Y-%m-%d %H:%M:%S')
        seek_time_before = str(seek_time_date - datetime.timedelta(seconds=cfg.SECOND_BEFORE_SXDW))
        seek_time_after = str(seek_time_date + datetime.timedelta(seconds=cfg.SECOND_AFTER_SXDW))

        # 编写sql语句
        sql = "select id, count, packages, satellite, arrival_time, duration, freq_down, \
              freq_unit, iqlocation, iqlen, bitrate, coderate, bandwidth, fs_rate, snr, freq_carrier, modulation_mode " \
              "from %s where arrival_time between '%s' and '%s'" % (cfg.TABLE_ZPSX, seek_time_before, seek_time_after)

        # 连接数据库
        conn = psycopg2.connect(database=cfg.DATABASE, user=cfg.USER, password=cfg.PASSWORD_DB,
                                host=cfg.SERVER_IP, port=cfg.PORT_DB)
        cur = conn.cursor()
        cur.execute(sql)
        zpsxs = cur.fetchall()
        conn.close()

        # 格式化中频数据
        zpsxs_uni = []
        for zpsx in zpsxs:
            zpsxs_uni.append(IntermediateMeta(id=zpsx[0], count=zpsx[1], packages=zpsx[2], satellite=zpsx[3],
                                              arrival_time=zpsx[4], duration=zpsx[5], freq_down=zpsx[6],
                                              freq_unit=zpsx[7], iqlocation=zpsx[8], iqlen=zpsx[9], bitrate=zpsx[10],
                                              coderate=zpsx[11], bandwidth=zpsx[12], fs_rate=zpsx[13], snr=zpsx[14],
                                              freq_carrier=zpsx[15], modulation_mode=zpsx[16]))

        return zpsxs_uni


    @staticmethod
    def query_sxdw_list_intermediate(seek_time):
        """
        :param seek_time:
        :return:
        """

        seek_time_date = datetime.datetime.strptime(seek_time, '%Y-%m-%d %H:%M:%S')
        seek_time_before = str(seek_time_date - datetime.timedelta(seconds=cfg.SECOND_BEFORE_INTERMEDIATE))
        seek_time_after = str(seek_time_date + datetime.timedelta(seconds=cfg.SECOND_AFTER_INTERMEDIATE))

        # 编写sql语句
        sql = "select id, id_sxdw, arrival_time, freq_down, freq_down_unit, batchnumber, true_value_lon, "\
                      "true_value_lat, true_value_error, result_confidence, false_value_lon, false_value_lat," \
                      "freq_up, freq_up_unit, multi_access_mode, modulate_pattern, code_mode, bandwidth," \
                      "bandwidth_unit, sps, sps_unit, medial_sat_norad, adjacent_sat_norad1, adjacent_sat_norad2 " \
                      "from %s where arrival_time between '%s' and '%s'" % (cfg.TABLE_SXDW, seek_time_before, seek_time_after)

        # 连接数据库
        conn = psycopg2.connect(database=cfg.DATABASE, user=cfg.USER, password=cfg.PASSWORD_DB,
                                host=cfg.SERVER_IP, port=cfg.PORT_DB)
        cur = conn.cursor()
        cur.execute(sql)
        sxdws = cur.fetchall()
        conn.close()

        # 格式化定位数据
        sxdws_uni = []
        for sxdw in sxdws:
            sxdws_uni.append(SXDWMeta(id=sxdw[0], id_sxdw=sxdw[1], arrival_time=sxdw[2], freq_down=sxdw[3],
                                      freq_down_unit=sxdw[4], batchnumber=sxdw[5], true_value_lon=sxdw[6],
                                      true_value_lat=sxdw[7], true_value_error=sxdw[8], result_confidence=sxdw[9],
                                      false_value_lon=sxdw[10], false_value_lat=sxdw[11], freq_up=sxdw[12],
                                      freq_up_unit=sxdw[13], multi_access_mode=sxdw[14], modulate_pattern=sxdw[15],
                                      code_mode=sxdw[16], bandwidth=sxdw[17], bandwidth_unit=sxdw[18], sps=sxdw[19],
                                      sps_unit=sxdw[20], medial_sat_norad=sxdw[21], adjacent_sat_norad1=sxdw[22],
                                      adjacent_sat_norad2=sxdw[23]))

        return sxdws_uni

















