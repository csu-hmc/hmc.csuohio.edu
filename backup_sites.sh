# This script runs on the moorepants.info server and rsync's the backup files
# from hmc.csuohio.edu to an offsite location.
for DIR in backups blobstoragebackups blobstoragesnapshots snapshotbackups
do
    rsync -a moorepants@hmc.csuohio.edu:/home/moorepants/tmp_backup/$DIR /home/jasonkmoore/website-backups/hmc.csuohio.edu/
done
