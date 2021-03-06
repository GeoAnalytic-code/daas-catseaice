FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
  python3 python3-pip \
  firefox-geckodriver \
  xvfb \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir selenium

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY . /opt/app
WORKDIR /opt/app
CMD ["python3", "src/catseaice.py"]
