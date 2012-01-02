#!/bin/bash
data=`date +%d_%H%M`
mysqldump --single-transaction --user=django_login --password="testus_cumulus" click2eat > /tmp/sqldump.sql
tar cJf /mnt/local-backup/backup-$data.tar.xz /tmp/sqldump.sql /home/www-data/bucatar/static/upload/
rm /tmp/sqldump.sql
rsync -var /mnt/local-backup/ /mnt/remote-backup/


