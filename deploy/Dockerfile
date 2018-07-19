FROM python:3.6.5

RUN apt-get update \
    && apt-get -y install vim wget

RUN pip install Flask==1.0.2
RUN pip install flask-restplus==0.11.0
RUN pip install requests==2.18.4
RUN pip install beautifulsoup4==4.6.0
RUN pip install lxml==4.2.1
RUN pip install gevent==1.3.2.post0
RUN pip install gunicorn==19.8.1
RUN pip install nose2==0.7.4

ADD . /opt/newjob
WORKDIR /opt/newjob

CMD tail -f /dev/null
