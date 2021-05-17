# 构建docker镜像
# docker build -t qaopenserver .

# 执行docker镜像
#docker run -d --name myqaopen -p 8000:8000 qaopenserver:latest

FROM python:3.7

MAINTAINER mengdegong@blued.com

ADD . .

USER root

RUN pip3 install -r requirements.txt

WORKDIR .

EXPOSE 8000

ENTRYPOINT python manage.py runserver 0.0.0.0:8000
