FROM python:3.8.0
MAINTAINER "hynemankan"
WORKDIR /code
COPY . .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
EXPOSE 29090
CMD gunicorn -c gun.conf app:app