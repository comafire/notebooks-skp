#!/bin/bash

echo $SSHFS_ID
echo $SSHFS_HOST
echo $SSHFS_VOLUME
/root/volume/bin/mount_sshfs.sh $SSHFS_ID $SSHFS_HOST $SSHFS_VOLUME
echo $S3_ACCOUNT
/root/volume/bin/mount_s3.sh $S3_ACCOUNT
/root/volume/bin/mount_blob.sh

SDATE="2018-07-01 08:00:00"
PATH_BASE="/root/mnt/dfs/notebooks-skp/mnist"
PATH_DATA="/root/mnt/dfs/data/mnist"
FILE_LOG="flask-skp-mnist.log"

pip2 install -r /root/volume/etc/jupyter/requirements.txt >> /root/volume/logs/$FILE_LOG 2>&1
pip3 install -r /root/volume/etc/jupyter/requirements.txt >> /root/volume/logs/$FILE_LOG 2>&1

mkdir -p /root/volume/logs

SDATE="$SDATE" PATH_DATA="$PATH_DATA" \
FLASK_APP="$PATH_BASE/src/backend/sdm.py" FLASK_DEBUG=1 \
flask run --host=0.0.0.0 >> /root/volume/logs/$FILE_LOG 2>&1

#python3 $PATH_BASE/src/backend/sdm.py
