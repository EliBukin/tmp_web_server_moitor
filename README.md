# tmp_web_server_moitor

#This is the dockerfile that is been used:

FROM alpine:latest

RUN apk add --no-cache python3-dev \
&& apk add py3-pip \
&& pip3 install --upgrade pip \
&& pip freeze > requirements.txt \
&& pip3 --no-cache-dir install -r requirements.txt \
&& pip3 install beautifulsoup4 \
&& apk add git \
&& pip3 install twilio \
&& pip3 install lxml
