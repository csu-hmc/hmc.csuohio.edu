Development Setup on Ubuntu 13.04
=================================

Note: Plone 4.2+ supports Python2.7.

Make a virtual environment for your Plone development (assumes you have
virtualenvwrapper already installed)::

   $ mkvirtualenv hmc-web-dev

Make sure you have PIL dependencies::

   (hmc-web-dev)$ sudo aptitude install libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev

Install PIL into the environment::

   (hmc-web-dev)$ wget http://effbot.org/downloads/Imaging-1.1.7.tar.gz
   (hmc-web-dev)$ tar -vzxf Imaging-1.1.7.tar.gz
   (hmc-web-dev)$ cd Imaging-1.1.7
   (hmc-web-dev)$ python setup.py install

Make a directory for your website somewhere::

   (hmc-web-dev)$ mkdir ~/path/to/hmc.csuohio.edu
   (hmc-web-dev)$ cd ~/path/to/hmc.csuohio.edu

Setup a spot in your home directory where you can cache all the buildout junk
for any Plone sites you may be developing::

  (hmc-web-dev)$ mkdir ~/.buildout
  (hmc-web-dev)$ mkdir ~/.buildout/eggs
  (hmc-web-dev)$ mkdir ~/.buildout/extends
  (hmc-web-dev)$ mkdir ~/.buildout/downloads
  (hmc-web-dev)$ touch ~/.buildout/default.cfg

The `default.cfg` file should look like (replace with your user name)::

  (hmc-web-dev)$ cat ~/.buildout/default.cfg
  [buildout]
  eggs-directory = /home/moorepants/.buildout/eggs
  download-cache = /home/moorepants/.buildout/downloads
  extends-cache = /home/moorepants/.buildout/extends

May be able to use `eggs-directory = ${env:HOME}/.buildout/eggs`

Create a `versions.cfg`, `packages.cfg`, `buildout.cfg` following the model in
Professional Plone 4 Development::

   (hmc-web-dev)$ cat buildout.cfg
   # Development environment buildout
   # ================================

   [buildout]
   parts =
       instance
       test
       coverage-report
       omelette
       zopepy
       zopeskel
       checkversions
       mkrelease

   extends =
       packages.cfg

   # Packages to check out/update when buildout is run
   auto-checkout =

   # Make sure buildout always attempts to update packages
   always-checkout = force

   # Development Zope instance. Installs the ``bin/instance`` script
   [instance]
   recipe = plone.recipe.zope2instance
   http-address = 8080
   user = admin:admin
   verbose-security = on
   eggs =
       ${eggs:main}
       ${eggs:devtools}

   # Test runner. Run: ``bin/test`` to execute all tests
   [test]
   recipe = zc.recipe.testrunner
   eggs = ${eggs:test}
   defaults = ['--auto-color', '--auto-progress']

   # Coverage report generator.
   # Run: ``bin/test --coverage=coverage``
   # and then: ``bin/coveragereport``
   [coverage-report]
   recipe = zc.recipe.egg
   eggs = z3c.coverage
   scripts = coveragereport
   arguments = ('parts/test/coverage', 'coverage')

   # Installs links to all installed packages to ``parts/omelette``.
   # On Windows, you need to install junction.exe first
   [omelette]
   recipe = collective.recipe.omelette
   eggs =
       ${eggs:main}
       ${eggs:devtools}

   # Installs the ``bin/zopepy`` interpreter.
   [zopepy]
   recipe = zc.recipe.egg
   eggs =
       ${eggs:main}
       ${eggs:devtools}
   interpreter = zopepy

   # Installs ZopeSkel, which can be used to create new packages
   # Run: ``bin/zopeskel``
   [zopeskel]
   recipe = zc.recipe.egg
   eggs = ZopeSkel

   # Tool to help check for new versions.
   # Run: ``bin/checkversions versions.cfg``
   [checkversions]
   recipe = zc.recipe.egg
   eggs = z3c.checkversions [buildout]

   # Tool to make releases
   # Run: ``bin/mkrelease --help``
   [mkrelease]
   recipe = zc.recipe.egg
   eggs = jarn.mkrelease
   (hmc-web-dev)$ cat versions.cfg
   # Project-specific version pins
   # =============================

   [versions]
   # Buildout
   mr.developer=1.25
   collective.recipe.omelette=0.16

   # Development tools
   bpython=0.12
   pygments=1.6
   Products.DocFinderTab=1.0.5
   Products.PDBDebugMode = 1.3.1
   Products.PrintingMailHost = 0.7
   z3c.coverage=2.0.0
   jarn.mkrelease=3.7
   lazy = 1.1
   setuptools-git=1.0
   setuptools-hg = 0.4
   setuptools-subversion = 3.1

   # ZopeSkel
   ZopeSkel=2.21.2
   Cheetah=2.2.1
   Paste = 1.7.5.1
   PasteScript=1.7.5
   PasteDeploy=1.5.0
   (hmc-web-dev)$ cat packages.cfg
   # Information about packages and known good version sets
   # ======================================================

   [buildout]
   extensions = mr.developer buildout.dumppickedversions
   extends =
   # Known good sets of eggs we may be using
       http://dist.plone.org/release/4.3.1/versions.cfg
       versions.cfg

   versions = versions
   unzip = true

   # Egg sets
   [eggs]
   main =
       Plone
   test =
   devtools =
       bpython
       plone.reload
       Products.PDBDebugMode
       Products.PrintingMailHost
       Products.DocFinderTab

   # Checkout locations
   [sources]

Now get the buildout bootstrap script (use the latest 1.7.x version don't use
2.x)::

   (hmc-web-dev)$ wget https://raw.github.com/buildout/buildout/1/bootstrap/bootstrap.py

Run bootstrap to setup the buildout commands in bin (requires that you have a
`buildout.cfg` in the working directory::

   (hmc-web-dev)$ python bootstrap.py

Make sure you have all the requirements for a Plone install. Here are some that
I didn't already have installed::

  (hmc-web-dev)$ sudo aptitude install libxml2-dev libxslt-dev
  (hmc-web-dev)$ pip install cython

Now download and install Plone with buildout::

  (hmc-web-dev)$ bin/buildout

Start the development server with::

  (hmc-web-dev)$ bin/instance fg

View it in your web browser at http://localhost:8080. Stop it with `<Ctrl-C>`.

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

   # adduser moorepants
   # sudo mkdir /home/moorepants/.ssh
   # sudo chmod 700 /home/moorepants/.ssh
   # chown moorepants:moorepants /home/moorepants/.ssh

Now go back to my personal machine and scp my public key to the
/home/moorepants/.ssh/authorized_keys on the server::

   scp -i ~/.ec2/hmckey.pem ~/.ssh/ida_ras.pub ubuntu@54.221.204.249:/home/moorepants/.ssh/authorized_keys

Back to the server and do this on the server for correct permissions::

   # chmod 600 .ssh/authorized_keys
   # chown moorepants:moorepants .ssh/authorized_keys

Give me super user permissions::

   # sudo adduser moorepants sudo
   # exit

Now log in with moorepants::

   $ ssh moorepants@54.221.204.249

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

    $ scp hmc.csuohio.edu.conf 54.221.204.249:/home/moorepants/hmc.csuohio.edu.conf
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
username: username@gmail.com
password: <gmail passowrd>

I aslo Checked the Force TTL in the ZMI Mailhost.

Setup the init scripts::

   # sudo cp ~/Plone-4.3.1r1-UnifiedInstaller/init_scripts/ubuntu/plone-standalone /etc/init.d/plone
   # sudo chmod 755 /etc/init.d/plone
   # sudo update-rc.d plone defaults

Setup backups and offsite data dumps.

Setup ufw firewall.

Setup regular database packing.

Now copy in my custom buildout recipe or start modifying the buildout one.
