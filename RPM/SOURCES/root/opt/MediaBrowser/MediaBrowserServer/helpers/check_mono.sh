#!/bin/sh
mono_path="$1"
if [ -z "$mono_path" ]; then mono_path="";fi
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
    echo "Can access a compliant mono" 
else
	echo "Trying Mono at /opt/mono"
    mono_path="/opt/mono"
fi
if [ "$mono_path" != "" ]; then
    export PATH=$mono_path/bin:$PATH
    export LD_LIBRARY_PATH=$mono_path/lib:$LD_LIBRARY_PATH
    export PKG_CONFIG_PATH=$mono_path/lib/pkgconfig:$PKG_CONFIG_PATH
fi
