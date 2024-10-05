FROM anolis-registry.cn-zhangjiakou.cr.aliyuncs.com/openanolis/python:3.11.1-8.6
MAINTAINER "hynemankan"
WORKDIR /code
COPY . .
RUN python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
EXPOSE 29090
CMD gunicorn -w 4 -b 0.0.0.0:29090 app:app