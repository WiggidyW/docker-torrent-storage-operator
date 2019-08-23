#!/bin/ash
IP=$1
if [ -e /downloads/*.${LOCK_FILE} ] || [ -e /torrents/*.${LOCK_FILE} ]; then echo "error: files in use" && exit; fi;
ls /downloads > /downloads_list.txt && ls /torrents > /torrents_list.txt
rsync --remove-source-files -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /keys/${SSH_KEY} -p ${STORAGE_SSH_PORT}" -arv --files-from=/downloads_list.txt /downloads $IP:${STORAGE_DOWNLOADS_PATH}
rsync --remove-source-files -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /keys/${SSH_KEY} -p ${STORAGE_SSH_PORT}" -arv --files-from=/torrents_list.txt /torrents $IP:${STORAGE_TORRENTS_PATH}
