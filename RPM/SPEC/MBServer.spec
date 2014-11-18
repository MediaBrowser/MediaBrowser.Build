%global name MediaBrowserServer
%global version %(f=$(ls -1 %_topdir/SOURCES/|grep .tar.gz);echo $f | cut -c 1-$((${#f}-7)))
%global release Stable
%global data_dir /var/opt/MediaBrowser/MediaBrowserServer
%global install_dir /opt/MediaBrowser/MediaBrowserServer

Name:           %{name}
Version:        %{version}
%if "%(echo $USER)" == "abuild"
Release:        %{release}.<CI_CNT>.<B_CNT>
%else
Release:        %{release}
%endif
Summary:        Media Browser Server is a home media server built on top of other popular open source technologies such as Service Stack, jQuery, jQuery mobile, and Mono.
Vendor:         Media Browser
Group:          Applications/Multimedia
BuildArch:      noarch
License:        GPL
URL:            http://mediabrowser.tv/
Source0:        https://github.com/MediaBrowser/MediaBrowser/archive/%{version}.tar.gz
Source1:        root.tar.bz2
AutoReqProv: no
BuildRequires: mono-devel > 3.2.7
Requires: mono-devel > 3.2.7, libgdiplus > 3.0.0, libmediainfo, libwebp >= 0.4.1, sqlite >= 3.8.2	
%global debug_package %{nil}

%description
Media Browser Server is a home media server built on top of other popular open source technologies such as Service Stack, jQuery, jQuery mobile, and Mono.
It features a REST-based api with built-in documention to facilitate client development. We also have client libraries for our api to enable rapid development.
%prep

%setup -n MediaBrowser-%{version} -q
mkdir -p src; find -maxdepth 1 -mindepth 1 -not -name src -exec mv '{}' src \;
%setup -c -n MediaBrowser-%{version} -q -T -D -a 1 
mv root/* ./
rm -r root

%build

. .%{install_dir}/helpers/check_mono.sh
echo $mono_path
buildLogs="%{install_dir}/bin/buildLogs.txt"
cd src/
mkdir -p ..%{install_dir}/bin
$mono_path/bin/xbuild /p:Configuration="Release Mono" /p:Platform="Any CPU" /t:clean MediaBrowser.Mono.sln > ..$buildLogs
$mono_path/bin/xbuild /p:Configuration="Release Mono" /p:Platform="Any CPU" /t:build MediaBrowser.Mono.sln >> ..$buildLogs
mv MediaBrowser.Server.Mono/bin/Release\ Mono/* ..%{install_dir}/bin
cd ..
rm -rf src
cd .%{install_dir}/bin
rm -rf libwebp
rm -rf MediaInfo
rm -rf sqlite3
rm -rf ./*.dylib
echo  "<configuration><dllmap dll=\"libwebp\" target=\"libwebp.so\" os=\"linux\"/></configuration>" > Imazen.WebP.dll.config
echo  "<configuration><dllmap dll=\"sqlite3\" target=\"libsqlite3.so.0.8.6\" os=\"linux\"/></configuration>" > System.Data.SQLite.dll.config

%pre

getent group media >/dev/null || groupadd -r media
getent passwd MediaBrowserServer >/dev/null || useradd -r -g media -d %{data_dir} -s /sbin/nologin -c "Account under which Media Browser Server runs" MediaBrowserServer

%install
mkdir -p %{buildroot}%{install_dir}
mkdir -p %{buildroot}%{data_dir}
cp -vR * %{buildroot}

%post

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