# MediaBrowser Server
FROM ubuntu:trusty
MAINTAINER Carlos Hernandez <carlos@techbyte.ca>

# Let the container know that there is no tty
ENV DEBIAN_FRONTEND noninteractive

# Set locale to UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
RUN locale-gen en_US en_US.UTF-8
RUN update-locale LANG=en_US.UTF-8
RUN dpkg-reconfigure locales

# Set user nobody to uid and gid of unRAID, uncomment for unRAID
RUN usermod -u 99 nobody
RUN usermod -g 100 nobody
RUN usermod -s /bin/bash nobody

# Update ubuntu
RUN apt-mark hold initscripts udev plymouth mountall;\
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 637D1286;\
    echo 'APT::Get::Assume-Yes "true";' > /etc/apt/apt.conf.d/90forceyes;\
    echo 'deb http://archive.ubuntu.com/ubuntu trusty main universe restricted' > /etc/apt/sources.list;\
    echo 'deb http://archive.ubuntu.com/ubuntu trusty-updates  main universe restricted' >> /etc/apt/sources.list;\
    echo 'deb http://ppa.launchpad.net/apps-z/mediabrowser/ubuntu trusty main' >> /etc/apt/sources.list;\
    apt-get update;\
    echo exit 101 > /usr/sbin/policy-rc.d && chmod +x /usr/sbin/policy-rc.d;\
    dpkg-divert --local --rename --add /sbin/initctl;\
    ln -sf /bin/true /sbin/initctl;\
    apt-get -y upgrade && apt-get clean

# Install dependencies
RUN apt-get install -qy --force-yes libmono-cil-dev Libgdiplus mediainfo libwebp-dev wget libsqlite3-dev python-pip python-tornado python-zmq python-psutil\
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
