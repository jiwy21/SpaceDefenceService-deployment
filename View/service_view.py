

from View import app
from Logic.service_logic import ServiceLogic
from flask import request
from log import console_out
import config as cfg
logging = console_out(cfg.services_log)

@app.route('/intermediate_list', methods=['GET', 'POST'])
@app.route('/intermediate_list.json', methods=['GET', 'POST'])
def intermediate_list():
    """
    :return: 中频数据json列表
    """
    logging.info(str(request))

    seek_start = request.args.get('time_begin')
    seek_end = request.args.get('time_end')

    logic = ServiceLogic()
    return logic.list_intermediate(seek_start, seek_end)


@app.route('/intermediate_IQ', methods=['GET', 'POST'])
@app.route('/intermediate_IQ.json', methods=['GET', 'POST'])
def intermediate_iq():
    """
    :return: IQ两路数据
    """
    logging.info(str(request))

    id_zpsx = int(request.args.get('id_zpsx'))

    logic = ServiceLogic()
    return logic.extract_iq(id_zpsx)


@app.route('/intermediate_list_sxdw', methods=['GET', 'POST'])
@app.route('/intermediate_list_sxdw.json', methods=['GET', 'POST'])
def intermediate_list_sxdw():
    """
    :return: 中频数据json列表
    """
    logging.info(str(request))

    seek_time = request.args.get('time_seek')

    logic = ServiceLogic()
    return logic.list_intermediate_sxdw(seek_time)


@app.route('/sxdw_list_intermediate', methods=['GET', 'POST'])
@app.route('/sxdw_list_intermediate.json', methods=['GET', 'POST'])
def sxdw_list_intermediate():
    """
    :return: 定位数据json列表
    """
    logging.info(str(request))

    seek_time = request.args.get('time_seek')

    logic = ServiceLogic()
    return logic.list_sxdw_intermediate(seek_time)















