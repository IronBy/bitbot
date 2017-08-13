FROM lbates2000/python-windows

MAINTAINER Valery Sushko (v.sushko@itransition.com)

SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

RUN mkdir c:/slackbot

ADD ./*.py c:/slackbot/

RUN pip install slackbot

WORKDIR c:/slackbot/

ENTRYPOINT python run.py