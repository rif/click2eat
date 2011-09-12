#!/bin/bash
data=`date +%d_%H%M`
mysqldump --user=django_login --password="testus_cumulus" click2eat | xz > /mnt/local-backup/backup-$data.sql.xz
rsync -var /mnt/local-backup/ /mnt/remote-backup/

## Putting the backup on a ftp
#cd db
#ftp -i -n << EOF
#open ftpserver.example.net
#user username password
#bin
#mput backup-$data.sql.gz
#bye
#EOF