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

For Plone::

sudo apt-get install python-setuptools python-dev build-essential libssl-dev
libxml2-dev libxslt1-dev libbz2-dev

sudo apt-get install libjpeg62-dev libreadline-gplv2-dev wv poppler-utils
python-imaging

Development Setup on Ubuntu 13.04
=================================

You need Python 2.6.8 but it fails to build on Ubuntu 13.04, so use this ppa::

   $ sudo add-apt-repository ppa:fkrull/deadsnakes
   $ sudo apt-get update
   $ sudo apt-get install python2.6 python2.6-dev

Make a virtual environment for your plone dev (assumes you have
virtualenvwrapper already installed)::

   $ mkvirtualenv -p /usr/bin/python2.6 hmc-web-dev

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

Now get the buildout bootstrap script (use the latest 1.7.x version don't use
2.x)::

   (hmc-web-dev)$ wget https://raw.github.com/buildout/buildout/1/bootstrap/bootstrap.py

Run bootstrap to setup the buildout commands in bin::

   (hmc-web-dev)$ python bootstrap.py

Setup a spot in your home directory where you can cache all the buildout junk
for any plone sites you may be developing::

  (hmc-web-dev)$ mkdir ~/.buildout
  (hmc-web-dev)$ mkdir ~/.buildout/eggs
  (hmc-web-dev)$ mkdir ~/.buildout/extends
  (hmc-web-dev)$ mkdir ~/.buildout/downloads

The default.cfg file should look like (replace with your user name)::

  (hmc-web-dev)$ vim ~/.buildout/default.cfg
  (hmc-web-dev)$ cat ~/.buildout/default.cfg
  [buildout]
  eggs-directory = /home/moorepants/.buildout/eggs
  download-cache = /home/moorepants/.buildout/downloads
  extends-cache = /home/moorepants/.buildout/extends

May be able to use `eggs-directory = ${env:HOME}/.buildout/eggs`

Create a buildout.cfg::

   (hmc-web-dev)$ vim buildout.cfg

Make sure you have all the requirements for a Plone install::

  (hmc-web-dev)$ sudo aptitude install libxml2-dev libxslt-dev
  (hmc-web-dev)$ pip install cython
  there are probably more, but I just had them installed already

Now download and install plone/zope with buildout::

  (hmc-web-dev)$ bin/buildout
