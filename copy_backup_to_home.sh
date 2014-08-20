for DIR in backups blobstoragebackups blobstoragesnapshots snapshotbackups
do
	rm -rf /home/moorepants/tmp_backup/$DIR
	cp -r /usr/local/Plone/zinstance/var/$DIR /home/moorepants/tmp_backup
done
# This is to remove the plone_daemon:plone_group permissions so that moorepants
# has permissions to download them from a remote server.
chown -R moorepants:moorepants /home/moorepants/tmp_backup
