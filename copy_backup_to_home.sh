# This script runs on hmc.csuohio.edu and copies the backup files to
# moorepants's home directory and sets the permissions so that they can be
# accessed via the moorepants user. This script should be run by plone_daemon.
for DIR in backups blobstoragebackups blobstoragesnapshots snapshotbackups
do
	# Don't check owner (o), group (g), or permmission (p) for copy.
	rsync -rltD --delete /usr/local/Plone/zinstance/var/$DIR /home/moorepants/tmp_backup
done
chmod -R g+rw /home/moorepants/tmp_backup
chown -R plone_daemon:hmc_backup /home/moorepants/tmp_backup
