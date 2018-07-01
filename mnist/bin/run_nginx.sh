#!/bin/bash

echo $SSHFS_ID
echo $SSHFS_HOST
echo $SSHFS_VOLUME
/root/volume/bin/mount_sshfs.sh $SSHFS_ID $SSHFS_HOST $SSHFS_VOLUME
echo $S3_ACCOUNT
/root/volume/bin/mount_s3.sh $S3_ACCOUNT
/root/volume/bin/mount_blob.sh

PATH_BASE="/root/mnt/dfs/notebooks-skp/mnist"
FILE_LOG="nginx-skp-mnist.log"

mkdir -p /root/volume/logs/nginx

PATH_BASE="$PATH_BASE" nginx -c $PATH_BASE/etc/nginx/nginx.conf >> /root/volume/logs/$FILE_LOG 2>&1
