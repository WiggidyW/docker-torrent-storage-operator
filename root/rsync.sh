#!/bin/ash
rsync --remove-source-files -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /keys/${SSH_KEY} -p ${STORAGE_SSH_PORT}" -arv /downloads/ ${IP}:${STORAGE_DOWNLOADS_PATH}
rsync --remove-source-files -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /keys/${SSH_KEY} -p ${STORAGE_SSH_PORT}" -arv /torrents/ ${IP}:${STORAGE_TORRENTS_PATH}
