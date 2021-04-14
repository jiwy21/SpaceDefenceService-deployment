FROM python:3.6.0

WORKDIR /SpaceDefenceService

COPY . .

# RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
RUN pip install -i https://pypi.douban.com/simple -r requirements.txt

CMD python /SpaceDefenceService/run.py && python /SpaceDefenceService/sxdw_monitor.py && python /SpaceDefenceService/zpsx_monitor.py


