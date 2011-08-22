#!/bin/bash
data=`date +%d_%H%M`
mysqldump --user=django_login --password="testus_cumulus" click2eat | xz > /home/rif/click2eat_backup/backup-$data.sql.xz

## Putting the backup on a ftp
#cd db
#ftp -i -n << EOF
#open ftpserver.example.net
#user username password
#bin
#mput backup-$data.sql.gz
#bye
#EOF