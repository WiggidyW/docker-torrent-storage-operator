FROM alpine

LABEL maintainer="wiggidy" mail="wiggidy@riseup.net"
LABEL description="Torrent storage controller for kubernetes which integrates a DaemonSet torrent cluster with an additional standalone torrent client."

ARG STORAGE_MESSENGER_PORT
ARG STORAGE_LABELS
ARG SSH_KEY

ENV STORAGE_DOWNLOADS_PATH=/downloads \
    STORAGE_TORRENTS_PATH=/torrents \
    STORAGE_NAMESPACE=default \
    STORAGE_SSH_PORT=22 \
    LOCK_FILE=lock

RUN apk add --no-cache \
    openssh-client \
    rsync \
    python3 \
 && pip3 install --no-cache-dir \
    requests \
    kubernetes \
 && mkdir /downloads \
 && mkdir /torrents \
 && mkdir /keys

COPY ./root /

RUN chmod +x /init.py /rsync.sh

VOLUME /downloads /torrents /keys

CMD ["/init.py"]
