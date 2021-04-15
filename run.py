

# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.getcwd())


from View import app
import config as cfg
import logging


if __name__ == '__main__':
    app.debug = True
    handler = logging.FileHandler(cfg.services_log)
    app.logger.addHandler(handler)
    app.run(host='', port=cfg.PORT, debug=False, threaded=False)






