FROM alpine

LABEL maintainer="wiggidy" mail="wiggidy@riseup.net"
LABEL description="Torrent storage controller for kubernetes which integrates a DaemonSet torrent cluster with an additional standalone torrent client."

ARG STORAGE_DOWNLOADS_PATH = /downloads
ARG STORAGE_TORRENTS_PATH = /torrents
ARG STORAGE_NAMESPACE = default
ARG STORAGE_SSH_PORT = 22
ARG STORAGE_MESSENGER_PORT
ARG STORAGE_LABELS
ARG SSH_KEY

ENV IP

RUN apk add --no-cache \
    openssh-client \
    rsync \
    python3 \
 && pip3 install --no-cache-dir \
    requests \
    kubernetes \
 && apk del --no-cache --purge pip3 \
 && mkdir /downloads \
 && mkdir /torrents \
 && mkdir /keys

COPY ./root /

RUN chmod +x /init.py /rsync.sh

VOLUME /downloads /torrents /keys

CMD ["/init.py"]
