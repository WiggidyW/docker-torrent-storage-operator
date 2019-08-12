#!/bin/ash
echo "server {listen ${PORT}; location / {proxy_pass http://${IP}:${PORT};}}" \
> /etc/nginx/conf.d/loadbalance-storage-controller.conf
nginx -s reload
