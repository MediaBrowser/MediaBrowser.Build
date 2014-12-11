#!/bin/sh

echo "--> start.sh script running..."

mkdir -p /config/clogs
touch /config/clogs/MediaBrowser.log

chmod 666 /config/clogs/*

run-parts -v  --report /etc/setup.d

envtpl /etc/circus.d/MediaBrowser.ini.tpl --allow-missing

echo "---> Starting circus..."
exec /usr/local/bin/circusd /etc/circus.ini
