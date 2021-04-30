

# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.getcwd())


from View import app
import Config.config as cfg
import logging


if __name__ == '__main__':
    app.debug = True

    if not os.path.exists(cfg.DIR_LOGS):
        os.makedirs(cfg.DIR_LOGS, mode=0o777)

    services_log = cfg.DIR_LOGS + cfg.services_log
    handler = logging.FileHandler(services_log)
    app.logger.addHandler(handler)
    app.run(host='', port=cfg.PORT, debug=False, threaded=False)






