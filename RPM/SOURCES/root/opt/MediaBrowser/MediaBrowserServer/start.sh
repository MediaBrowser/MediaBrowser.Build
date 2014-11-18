#! /bin/sh
umask 002

HOME="$(getent passwd $USER | awk -F ':' '{print $6}')"
conf_file_path="MediaBrowser/MediaBrowserServer/MediaBrowserServer.cfg"
program_data_path="/var/opt/MediaBrowser/MediaBrowserServer"                                
program_path="/opt/MediaBrowser/MediaBrowserServer/bin"
FFmpeg="/bin/ffmpeg"
FFprobe="/bin/ffprobe"

if [ -r /etc/opt/$conf_file_path ]; then
    echo "Reading system-wide config...." >&2
    . /etc/opt/$conf_file_path
fi
if [ -r ~/.$conf_file_path ]; then
    echo "Reading user config...." >&2
    . ~/.$conf_file_path
fi

cd "$program_path"
. ../helpers/check_mono.sh
cd "$program_path"
ifFFmpeg=""
if [[ -x $FFmpeg ]]; then ifFFmpeg="-ffmpeg $FFmpeg"; fi;
ifFFprobe=""
if [[ -x $FFprobe ]]; then ifFFprobe="-ffprobe $FFprobe"; fi;
mkdir -p $program_data_path
$mono_path/bin/mono MediaBrowser.Server.Mono.exe -programdata "$program_data_path" $ifFFmpeg $ifFFprobe
