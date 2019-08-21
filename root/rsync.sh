#!/bin/ash
rsync --remove-source-files -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /keys/${KEY}" -arv /downloads/ ${IP}:${TARGET_DOWNLOADS_PATH}
rsync --remove-source-files -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /keys/${KEY}" -arv /torrents/ ${IP}:${TARGET_TORRENTS_PATH}
