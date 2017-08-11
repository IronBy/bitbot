FROM microsoft/dotnet-framework:4.6.2

MAINTAINER Valery Sushko (v.sushko@itransition.com)

SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

# Install chocolatey
RUN iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex
RUN choco feature enable -n allowGlobalConfirmation

RUN choco install python3

RUN mkdir c:/slackbot

ADD ./*.py c:/slackbot/

RUN pip install slackbot

WORKDIR c:/slackbot/

ENTRYPOINT python run.py