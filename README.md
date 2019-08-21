# docker-torrent-storage-operator

IN: Single torrent client, this image must be a sidecar to it. Share their torrents and downloads directories. Torrent client must export its completed downloads along with the corresponding torrent files to the shared directories on completion simultaneously.

OUT: Clustered torrent clients. Must be a DaemonSet. This image will rsync the torrents and downloads to the daemonsetted torrent client with the highest available storage. Storage is queried over HTTP. Recipient must have an SSH server. I personally set up a triple pod setting - torrent client, storage querier available over http, and ssh server. SSH server and torrent client share downloads and torrents directories.
