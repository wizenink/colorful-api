FROM ubuntu:18.04

MAINTAINER David Maseda Neira "[david.maseda@udc.es]"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev wget

COPY ./requirements.txt /server/requirements.txt

WORKDIR /server
RUN mkdir /server/models
#ADD http://davidmaseda.online/pix2pix.tar.gz /server/models/
RUN wget http://davidmaseda.online/pix2pix.tar.gz -O /server/pix2pix.tar.gz
RUN ls -liah /server/models
RUN tar -xvzf  /server/pix2pix.tar.gz -C /server/models
RUN rm /server/pix2pix.tar.gz

RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt

COPY . /server

ENTRYPOINT [ "python3.6" ]

CMD [ "main.py" ]
