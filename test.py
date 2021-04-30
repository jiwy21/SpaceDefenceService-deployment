

import os

if __name__ == '__main__':

    path = '1/2/3'
    if not os.path.exists(path):
        os.makedirs(path, 0o777)
































