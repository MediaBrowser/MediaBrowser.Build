#!/bin/sh

echo "--> start.sh script running..."

mkdir -p /config/clogs
touch /config/clogs/MediaBrowser.log

chmod 666 /config/clogs/*

envtpl /etc/circus.d/MediaBrowser.ini.tpl --allow-missing
envtpl /etc/mediabrowser.conf.tpl --allow-missing

run-parts -v  --report /etc/setup.d

echo "---> Starting circus..."
exec /usr/local/bin/circusd /etc/circus.ini
