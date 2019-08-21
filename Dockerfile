FROM alpine

LABEL maintainer="wiggidy" mail="wiggidy@riseup.net"
LABEL description="minimal rTorrent in Docker, intended for use with remote (local or internet) XMLRPC controller such as ruTorrent or Flood."
LABEL version="1.0"

ARG STORAGE_DOWNLOADS_PATH
ARG STORAGE_TORRENTS_PATH
ARG STORAGE_MESSENGER_PORT
ARG STORAGE_SSH_PORT
ARG STORAGE_NAMESPACE
ARG STORAGE_LABELS
ARG SSH_KEY

ENV IP
