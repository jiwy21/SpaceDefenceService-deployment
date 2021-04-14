

# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.getcwd())




import config as cfg
from View import app
import config as cfg
from log import console_out




if __name__ == '__main__':
    logging = console_out(cfg.services_log)
    logging.debug('services start!')
    app.run(host='', port=cfg.PORT, debug=False, threaded=False)






