[watcher:MediaBrowser]
cmd = mono 
args = MediaBrowser.Server.Mono.exe -programdata /config
copy_env = True
uid = {{ USER_ID | default(99) }}
gid = {{ GROUP_ID | default(100) }}
working_dir = /opt/mediabrowser
autostart = true
respawn = true
max_retry = -1
stdout_stream.class = FileStream
stdout_stream.time_format = %Y-%m-%d %H:%M:%S
stdout_stream.filename = /config/clogs/MediaBrowser.log
stderr_stream.class = StdoutStream
signleton = True
use_sockets = False
