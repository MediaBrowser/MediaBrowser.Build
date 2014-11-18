#! /bin/sh
umask 002

HOME="$(getent passwd $USER | awk -F ':' '{print $6}')"
conf_file_path="MediaBrowser/MediaBrowserServer/MediaBrowserServer.cfg"
program_data_path="/var/opt/MediaBrowser/MediaBrowserServer"                                
program_path="/opt/MediaBrowser/MediaBrowserServer/bin"

if [ -r /etc/opt/$conf_file_path ]; then
    echo "Reading system-wide config...." >&2
    . /etc/opt/$conf_file_path
fi
if [ -r ~/.$conf_file_path ]; then
    echo "Reading user config...." >&2
    . ~/.$conf_file_path
fi

if [ "$mono_path" != "" ]; then
    export PATH=$mono_path/bin:$PATH
    export LD_LIBRARY_PATH=$mono_path/lib:$LD_LIBRARY_PATH
    export PKG_CONFIG_PATH=$mono_path/lib/pkgconfig:$PKG_CONFIG_PATH
fi
cd "$program_path"
../helpers/check_mono.sh
mkdir -p $program_data_path
mono MediaBrowser.Server.Mono.exe -programdata "$program_data_path"
