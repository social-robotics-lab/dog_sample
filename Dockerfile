FROM ubuntu

RUN sed -i 's@archive.ubuntu.com@ftp.jaist.ac.jp/pub/Linux@g' /etc/apt/sources.list


WORKDIR /workspace

# Python
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    python3 \
    python3-pip \
    python3-tk \
    python3-dev

# OpenJTalk
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    ffmpeg \
    hts-voice-nitech-jp-atr503-m001 \
    open-jtalk \
    open-jtalk-mecab-naist-jdic \
    unzip \
    wget

RUN wget --no-check-certificate http://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.8/MMDAgent_Example-1.8.zip \
    && unzip MMDAgent_Example-1.8.zip \
    && cp -r MMDAgent_Example-1.8/Voice/mei/ /usr/share/hts-voice/ \
    && rm -rf MMDAgent_Example-1.8.zip MMDAgent_Example-1.8

# Input Japanese in console
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    language-pack-ja-base \
    language-pack-ja


RUN pip3 install pydub pysimplegui


ENV DISPLAY host.docker.internal:0.0
ENV LANG=ja_JP.UTF-8

# Japanese font
RUN apt-get -y install fonts-ipafont

RUN useradd -m -d /home/sota -s /bin/bash sota
USER sota
WORKDIR /tmp

