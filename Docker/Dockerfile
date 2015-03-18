# MediaBrowser Server
FROM ubuntu:utopic
MAINTAINER Carlos Hernandez <carlos@techbyte.ca>

# Let the container know that there is no tty
ENV DEBIAN_FRONTEND noninteractive

# Set locale to UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
RUN locale-gen en_US en_US.UTF-8
RUN update-locale LANG=en_US.UTF-8
RUN dpkg-reconfigure locales

# Update ubuntu
RUN apt-mark hold initscripts udev plymouth mountall;\
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 637D1286;\
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF;\
    echo 'APT::Get::Assume-Yes "true";' > /etc/apt/apt.conf.d/90forceyes;\
    echo 'deb http://archive.ubuntu.com/ubuntu utopic main universe restricted' > /etc/apt/sources.list;\
    echo 'deb http://archive.ubuntu.com/ubuntu utopic-updates  main universe restricted' >> /etc/apt/sources.list;\
    echo 'deb http://ppa.launchpad.net/apps-z/mediabrowser-daily/ubuntu utopic main' >> /etc/apt/sources.list;\
# Add mono 3.10
    echo "deb http://download.mono-project.com/repo/debian wheezy/snapshots/3.10.0 main" >> /etc/apt/sources.list;\
    echo 'deb http://download.mono-project.com/repo/debian wheezy-apache24-compat main' >> /etc/apt/sources.list;\
    apt-get update;\
    echo exit 101 > /usr/sbin/policy-rc.d && chmod +x /usr/sbin/policy-rc.d;\
    dpkg-divert --local --rename --add /sbin/initctl;\
    ln -sf /bin/true /sbin/initctl;\
    apt-get -y upgrade && apt-get clean

# Install dependencies
RUN apt-get install -qy --force-yes libmono-cil-dev mediainfo wget libsqlite3-dev libc6-dev python-pip python-tornado python-zmq python-psutil imagemagick-6.q8 libmagickwand-6.q8-2\
    && apt-get clean

# Install and Configure Circus
RUN pip --no-input install --upgrade pip
RUN pip --no-input install circus;\
    pip --no-input install envtpl
RUN mkdir /etc/circus.d /etc/setup.d

# Install latest MediaBrowser release from development PPA 
RUN apt-get install -qy --force-yes mediabrowser

# Expose config volume
VOLUME /config 

# Add config files
ADD ./files/circus.ini /etc/circus.ini
ADD ./files/start.sh /start.sh
ADD ./files/circus.d/MediaBrowser.ini.tpl /etc/circus.d/MediaBrowser.ini.tpl
ADD ./files/setup.d/mediabrowser /etc/setup.d/mediabrowser
ADD ./files/setup.d/mediabrowser.conf.tpl /etc/mediabrowser.conf.tpl

# Default MB3 HTTP/tcp server port
EXPOSE 8096/tcp
# Default MB3 HTTPS/tcp server port
EXPOSE 8920/tcp
# UDP server port
EXPOSE 7359/udp
# ssdp port for UPnP / DLNA discovery
EXPOSE 1900/udp
# Make start script executable and initiate container with start script.
RUN chmod u+x  /start.sh
ENTRYPOINT ["/start.sh"]
