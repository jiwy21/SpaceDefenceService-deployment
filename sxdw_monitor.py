


import shutil
import pandas as pd
import config as cfg
import psycopg2
import time
import os
import sys
from log import console_out

sys.path.append(os.getcwd())


class sxdw2db:

    def __init__(self):
        self.original_path = cfg.DIR_ORIGINAL_SXDW
        self.processed_path = cfg.DIR_SAVED_SXDW
        self.rubbish_path = cfg.DIR_RUBBISH_SXDW
        self.time_delay = cfg.TIME_DELAY

    def illegal(self, file):
        return (file.split('_')[0] != 'sxdw') or (file.split('.')[-1] != 'csv') or (len(file.split('_')) != 3)

    def mv2rubbish(self, file):
        shutil.move(self.original_path + file, self.rubbish_path + file)

    def mv2processed(self, file):
        shutil.move(self.original_path + file, self.processed_path + file)

    def write2db(self, file):

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

        sxdws = pd.read_csv(self.original_path + file).values

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
            sql = "insert into %s (id, id_sxdw, arrival_time, freq_down, freq_down_unit, batchnumber, true_value_lon, " \
                  "true_value_lat, true_value_error, result_confidence, false_value_lon, false_value_lat," \
                  "freq_up, freq_up_unit, multi_access_mode, modulate_pattern, code_mode, bandwidth," \
                  "bandwidth_unit, sps, sps_unit, medial_sat_norad, adjacent_sat_norad1, adjacent_sat_norad2) " % cfg.TABLE_SXDW + \
                  "values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
                  "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (cur_id, id_sxdw, arrival_time,
                                                                                   freq_down, freq_down_unit,
                                                                                   batchnumber, true_value_lon,
                                                                                   true_value_lat, true_value_error,
                                                                                   result_confidence,
                                                                                   false_value_lon, false_value_lat,
                                                                                   freq_up, freq_up_unit,
                                                                                   multi_access_mode, modulate_pattern,
                                                                                   code_mode,
                                                                                   bandwidth, bandwidth_unit, sps,
                                                                                   sps_unit, medial_sat_norad,
                                                                                   adjacent_sat_norad1,
                                                                                   adjacent_sat_norad2)

            cur.execute(sql)

        conn.commit()
        conn.close()



if __name__ == '__main__':

    sxdw_db = sxdw2db()
    logging = console_out(cfg.sxdw_log)
    logging.debug('sxdw_monitor start!')

    cnt = 0
    mod = 3600 / cfg.TIME_DELAY
    while 1:

        time.sleep(sxdw_db.time_delay)
        cnt += 1
        if cnt % mod == 0:
            logging.info('sxdw_monitor is still monitoring!')
            cnt = 0

        files = os.listdir(sxdw_db.original_path)

        if len(files) != 0:

            for file in files:

                logging.info(file + ' detected!')

                # Check
                if sxdw_db.illegal(file):
                    sxdw_db.mv2rubbish(file)
                    logging.info(file + ' has been put into rubbish.')
                else:
                    sxdw_db.write2db(file)
                    sxdw_db.mv2processed(file)
                    logging.info(file + ' processed done!')













































