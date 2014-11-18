%global name MediaBrowserServer
%global version %(f=$(ls -1 %_topdir/SOURCES/|grep .tar.gz);echo $f | cut -c 1-$((${#f}-7)))
%global release Stable
%global data_dir /var/opt/MediaBrowser/MediaBrowserServer
%global install_dir /opt/MediaBrowser/MediaBrowserServer


Name:           %{name}
Version:        %{version}
Release:        %{release}.<CI_CNT>.<B_CNT>
Summary:        Media Browser Server is a home media server built on top of other popular open source technologies such as Service Stack, jQuery, jQuery mobile, and Mono.
Vendor:         Media Browser
Group:          Applications/Multimedia
BuildArch:      noarch
License:        GPL
URL:            http://mediabrowser.tv/
Source0:        https://github.com/MediaBrowser/MediaBrowser/archive/%{version}.tar.gz
Source1:        MBServer_scripts.tar.bz2
AutoReqProv: no
BuildRequires: mono-opt-devel,mono-devel
Requires: mono-devel > 3.2.7, libgdiplus > 3.0.0, libmediainfo, libwebp >= 0.4.1, sqlite >= 3.8.2	
%global debug_package %{nil}

%description
Media Browser Server is a home media server built on top of other popular open source technologies such as Service Stack, jQuery, jQuery mobile, and Mono.
It features a REST-based api with built-in documention to facilitate client development. We also have client libraries for our api to enable rapid development.
%prep

%setup -n MediaBrowser-%{version} -q
mkdir -p src; find -maxdepth 1 -mindepth 1 -not -name src -exec mv '{}' src \;
%setup -n MediaBrowser-%{version} -q -T -D -a 1 

%build
/opt/mono/env.sh
cd src/
mkdir -p ../opt/MediaBrowser/MediaBrowserServer/bin
echo "xbuild: cleaning build folder"
/opt/mono/bin/xbuild /p:Configuration="Release Mono" /p:Platform="Any CPU" /t:clean MediaBrowser.Mono.sln /verbosity:quiet > ../opt/MediaBrowser/MediaBrowserServer/bin/buildLogs.txt
/opt/mono/bin/xbuild /p:Configuration="Release Mono" /p:Platform="Any CPU" /t:build MediaBrowser.Mono.sln >> ../opt/MediaBrowser/MediaBrowserServer/bin/buildLogs.txt
mv MediaBrowser.Server.Mono/bin/Release\ Mono/* ../opt/MediaBrowser/MediaBrowserServer/bin
cd ..
rm -rf src 
%pre
getent group media >/dev/null || groupadd -r media
getent passwd MediaBrowserServer >/dev/null || useradd -r -g media -d %{data_dir} -s /sbin/nologin -c "Account under which Media Browser Server runs" MediaBrowserServer
%install
mkdir -p %{buildroot}%{install_dir}
mkdir -p %{buildroot}%{data_dir}
cp -vR * %{buildroot}
%post
#CHECK VERSION OF MONO
mono_path=""
conf_file_path="MediaBrowser/MediaBrowserServer/MediaBrowserServer.cfg"

if [ -r /etc/opt/$conf_file_path ]; then
    echo "Reading system-wide config...." >&2
    . /etc/opt/$conf_file_path
fi

MONO_VERSION=$("$mono_path/bin/mono" --version |cut -d' ' -f5 | head -1)

#http://stackoverflow.com/questions/3511006/how-to-compare-versions-of-some-products-in-unix-shell

vercomp ()
{
  typeset    IFS='.'
  typeset -a v1=( $1 )
  typeset -a v2=( $2 )
  typeset    n diff

  for (( n=0; n<4; n+=1 )); do
    diff=$((v1[n]-v2[n]))
    if [ $diff -ne 0 ] ; then
      [ $diff -le 0 ] && echo '-1' || echo '1'
      return
    fi
  done
  echo  '0'
}


if [[ -e "$mono_path/bin/mono"  &&  $(vercomp $MONO_VERSION "3.2.7") -eq 1 ]]; then
    echo "THe server can access a compliant mono" 
else
	echo "adding mono_path to cfg file at /etc/"
    echo "mono_path=\"/opt/mono\"" > /etc/opt/MediaBrowser/MediaBrowserServer/MediaBrowserServer.cfg
fi

systemctl daemon-reload

%files
%{install_dir}
%attr(775,MediaBrowserServer,media) %{data_dir}
/etc/sudoers.d/MediaBrowserServer
/etc/systemd/system/MediaBrowserServer.service
/usr/
%config(noreplace) /etc/opt/MediaBrowser/MediaBrowserServer/MediaBrowserServer.cfg
%changelog 
* %(date -u +"%a %b %d %Y") Jose
- Update to version %{version}
