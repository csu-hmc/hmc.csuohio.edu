Server Setup
============

Here's how I setup the hmc.csuohio.edu webserver on Amazon Cloud Services.

Go to the AWS management console at aws.amazon.com.

Sign up for Ec2 and verify the account by phone (they call you and ask for a
pin).

Get this AMI ami-23d9a94a from http://cloud-images.ubuntu.com/locator/ec2/,
(Ubuntu Server 12.04 LTS 64 bit).

Launch an instance with this AMI (be sure to switch to reserved instance in a
year after our free trial runs out so that it will be cheaper). Save the key
for the instance here::

   $ mkdir ~/.ec2
   $ ls ~/.ec2
   $ hmckey.pem
   $ chmod 600 ~/.ec2/hmckey.pem

Make a webserver security group for the instance with an HTTP and SSH rule
(i.e. only ports 80 and 22).

Now allocate an Elastic IP address for this instance then associate it with the
instance. This is the IP I got::

   54.221.204.249

Now ssh in::

   $ ssh -i ~/.ec2/hmckey.pem ubuntu@54.221.204.249

Now create users so they can log in::

   # adduser <username>
   # sudo mkdir /home/<username>/.ssh
   # sudo chmod 700 /home/<username>/.ssh
   # chown <username>:<username> /home/<username>/.ssh

Now go back to my personal machine and scp my public key to the
/home/<username>/.ssh/authorized_keys on the server::

   scp -i ~/.ec2/hmckey.pem ~/.ssh/ida_ras.pub ubuntu@54.221.204.249:/home/<username>/.ssh/authorized_keys

Back to the server and do this on the server for correct permissions::

   # chmod 600 .ssh/authorized_keys
   # chown <username>:<username> .ssh/authorized_keys

Give me super user permissions::

   # sudo adduser <username> sudo
   # exit

Now log in with <username>::

   $ ssh <username>@54.221.204.249

Install some stuff::

   # sudo aptitude update && sudo aptitude upgrade
   # sudo aptitude install htop

Set the timezone to Ohio::

   # sudo dpkg-reconfigure tzdata

Select 'US/Eastern'.

Install nginx::

   # sudo aptitude install nginx

Get the dependencies for Plone::

   # sudo apt-get install python-dev build-essential wv poppler-utils libxml2-dev libxslt1-dev libssl-dev libreadline-dev libjpeg-dev libz-dev libfreetype6 libfreetype6-dev

Install Plone from the Unified installer::

   # wget https://launchpad.net/plone/4.3/4.3.1/+download/Plone-4.3.1r1-UnifiedInstaller.tgz
   # tar -zxvf Plone-4.3.1r1-UnifiedInstaller.tgz
   # cd Plone-4.3.1r1-UnifiedInstaller/
   # sudo ./install.sh standalone

Plone can then be started with::

   # sudo -u plone_daemon /usr/local/Plone/zinstance/bin/{start|stop|restart|status}

Buildout run with::

   # sudo -u plone_buildout /usr/local/Plone/zinstance/bin/builout

Upload the  nginx configuration file and create a symlink for it to enable::

    $ scp hmc.csuohio.edu.conf 54.221.204.249:/home/<username>/hmc.csuohio.edu.conf
    $ ssh 54.221.204.249
    # sudo mv hmc.csuohio.edu.conf /etc/nginx/sites-available/hmc.csuohio.edu.conf
    # sudo ln -s /etc/nginx/sites-available/hmc.csuohio.edu.conf /etc/nginx/sites-enabled/hmc.csuohio.edu.conf
    # sudo /etc/init.d/nginx restart

You my gmail account for now for the mail smtp in Plone. Google now blocks
attempts to login and I got supciisou login warnings from goolge. COuld fingure
this out until I did this:
http://angelsurfer.blogspot.com/2013/04/gmail-smtp-setup-to-moodle.html
Went to some website that open google account for loggin in.

smtp: smpt.gmail.com
port: 587
username: <username>@gmail.com
password: <gmail passowrd>

I aslo Checked the Force TTL in the ZMI Mailhost.

Setup the init scripts::

   # sudo cp ~/Plone-4.3.1r1-UnifiedInstaller/init_scripts/ubuntu/plone-standalone /etc/init.d/plone
   # sudo chmod 755 /etc/init.d/plone
   # sudo update-rc.d plone defaults

Note that the init.d script needs to be modified to have ``sudo -u
plone_daemon`` so that the service runs under plone_daemon and not root. See
the ``plone`` script included in this repo.

Setup backups and offsite data dumps.

Setup ufw firewall.

Setup regular database packing.

Now copy in my custom buildout recipe or start modifying the buildout one.

Change admin password in the root ZMI (8080:manage).

Config
======

Security settings
Use email address as login name

Enable user folders

TinyMCE

Paste from word
paste from plain text

Editing
Show 'Short Name' on content? yes

In Plone 4, there are two steps you need to take in order to easily embed content:

First, go to Site Setup>TinyMCE Visual Editor then click on the Toolbar tab.

    Enable the checkbox next to "Insert/edit Media"
    Scroll down to the bottom of the screen and click "Save"

Then, go to Site Setup>HTML Filtering

    Add iframe to custom tags.
    Scroll down to the bottom of the screen and click "Save"

With these changes made, you should be able to click newly-added "Embed Media" button in the TinyMCE toolbar.  You can paste in the URL of a YouTube video, and TinyMCE will do the rest for you!

I add the diazo product for theming

enabled global comments
comment transformation: intellgient text

allow caption images

For quick mathjax support I put::

   <script type="text/x-mathjax-config">
   MathJax.Hub.Config({
     TeX: { equationNumbers: { autoNumber: "AMS" } }
   });
   </script>
   <script type="text/javascript"
     src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
   </script>

In the site settings>JavaScript for web statistics support box. This should be
moved to the HEAD block in the template and I should think about whether we
need to have auto numbered equations.

Backup
======

The current offsite backup scheme is the following:

I'm using the collective.recipe.backup_ buildout recipe which ultimately runs
the repozo recipe/script with sane defaults. Repozo allows you take backups
without stopping Plone/Zope. I use the bin/backup script which does incremental
backups (except the database has been packed, then it does a full backup). This
creates backups in the following directories:

- ``/usr/local/Plone/zinstance/var/backups``
- ``/usr/local/Plone/zinstance/var/blobstoragebackups``

.. _collective.recipe.backup: https://pypi.python.org/pypi/collective.recipe.backup

Note that if you run the ``bin/snapshotbackup`` manually then the full backups
will be in these directories:

- ``/usr/local/Plone/zinstance/var/snapshotbackups``
- ``/usr/local/Plone/zinstance/var/blobstoragebackups``

Then I edit the crontab of the the ``plone_daemon`` user::

   $ sudo crontab -u plone_daemon -e

to include this crobjob::

   # Run the Plone backup scripts the 1st and 16th day of each month at 3 AM.
   1 3 1,16 * * /usr/local/Plone/zinstance/bin/backup && /home/moorepants/copy_backup_to_home.sh

The backup script must be run by ``plone_daemon``. If you use
z3c.recipe.crontab_ the backup script will be run by ``plone_buildout`` which
will not have the right permissions to copy all the backup files.

.. _z3c.recipe.crontab: https://pypi.python.org/pypi/z3c.recipe.usercrontab

The ``copy_backup_to_home.sh`` runs after the backup script simply copies the
pertinent directories to ``moorepants``'s home directoy. The script is executed
and owned by ``plone_daemon``. It copies the backup directories recursively
into ``/home/moorepants/tmp_backup`` which is owned by the ``hmc_backup``
group. Both ``moorepants`` and ``plone_daemon`` are in the ``hmc_backup``
group. It also set the ownsr of the copied files and directories recursively to
``moorepants:hmcbackup``.

Then on the 2nd and 17th day of the month a cron job runs a script on the
moorepants.info server that uses rsync to copy the files from
``hmc.csuohio.edu:/home/moorepants/tmp_backup`` to
``moorepants.info:/home/moorepants/website-backups/hmc.csuohio.edu``.

Other
-----

This look promising for backup to S3:

http://blog.linuxacademy.com/linux/how-to-backup-linux-to-amazon-s3-using-s3cmd/
