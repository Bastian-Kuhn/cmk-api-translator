FROM alpine:3.6
WORKDIR /srv


RUN apk add --no-cache python3 \
    uwsgi \
    ca-certificates \
    gcc \
    g++ \
    linux-headers \
    python3-dev \
    uwsgi-python3 \
    openssl-dev

RUN ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

ARG envconfig
ENV conf=$envconfig

COPY . /srv/

CMD [ "uwsgi", "--master", "/srv/configs/uwsgi_docker.ini" ]

EXPOSE 9090
