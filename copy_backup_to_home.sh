for DIR in backups blobstoragebackups blobstoragesnapshots snapshotbackups
do
	rm -rf /home/moorepants/tmp_backup/$DIR
	#cp -r --no-preserve=ownership /usr/local/Plone/zinstance/var/$DIR /home/moorepants/tmp_backup
	cp -r /usr/local/Plone/zinstance/var/$DIR /home/moorepants/tmp_backup
done
# The user plone_buildout runs this script so it does not have permissions
# enough to change all the files because they are owned by
# plone_daemon:plone_group so the following command fails.
# If the --no-preseve=ownership flag is used in cp then the owner is
# plone_buildout:plone_group, so it should now be able to modify the files
# ownership but that doesn't seem to happen.
#chmod -r g+rw /home/moorepants/tmp_backup
#chown -R moorepants:hmc_backup /home/moorepants/tmp_backup
