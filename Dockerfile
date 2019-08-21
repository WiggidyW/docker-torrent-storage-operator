FROM alpine

LABEL maintainer="wiggidy" mail="wiggidy@riseup.net"
LABEL description="Torrent storage controller for kubernetes which integrates a DaemonSet torrent cluster with an additional standalone torrent client."

ARG STORAGE_DOWNLOADS_PATH
ARG STORAGE_TORRENTS_PATH
ARG STORAGE_MESSENGER_PORT
ARG STORAGE_SSH_PORT
ARG STORAGE_NAMESPACE
ARG STORAGE_LABELS
ARG SSH_KEY

ENV IP

RUN apk add --no-cache \
    openssh-client \
    rsync \
    python \
 && pip install --no-cache-dir \
    requests \
    kubernetes \
 && mkdir /downloads \
 && mkdir /torrents \
 && mkdir /keys

COPY ./root /

RUN chmod +x /init.py /rsync.sh

VOLUME /downloads /torrents /keys

CMD ["/init.py"]
