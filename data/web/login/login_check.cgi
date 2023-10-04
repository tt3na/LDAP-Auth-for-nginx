#!/bin/bash -vx

homd=/home/abc
sesd=$homd/session
logd=$homd/log
tmp=/tmp/tmp_$$

todayhms=$(date +%Y%m%d%H%M%S)

# logfile=LOG.${HOSTNAME}.$(basename $0)_$(date +%Y%m%d%H%M%S)_$$
# exec 2>$logd/$logfile

ERROR_HOLDER(){
	echo "Content-type: text/html; charset=UTF-8"
	echo ""
	echo "error"
	rm -rf $tmp-*
	exit 1	
}

trap ERROR_HOLDER ERR
set -o pipefail

if [ -n "$CONTENT_LENGTH" ];then
	dd bs=$CONTENT_LENGTH	|
	sed 's/&/\n/g'		| 
	sed 's/=/ /g'	> $tmp-name
else
	: > $tmp-name
fi

if [ -n "$QUERY_STRING" ];then
	echo "$QUERY_STRING"	|
	sed 's/&/\n/g' 		| 
	sed 's/=/ /g'   > $tmp-get
else
	: > $tmp-get
fi

user=$(awk '$1=="USER"{print $2}' $tmp-name)

# パスワードを扱うのでログの記録停止
set +vx
trap : ERR
pass=$(awk '$1=="PASSWORD"{print $2}' $tmp-name)
phash=$(echo $pass | md5sum | awk '{print $1}')

# 空判定
if [ "$user" == "" ] || [ "$pass" == "" ]; then
	code=1
fi

# LDAP認証
ldapwhoami -x -D "cn=$user,$LDAP_BASE_DN" -w $pass -H ldap://$LDAP_HOST:$LDAP_PORT
if [ $? -eq 0 ]; then
    code=0
else
    code=1
fi

# ログ記録再開
set -vx
trap ERROR_HOLDER ERR

if [ $code -eq 0 ];then
	sesid=$(echo $todayhms$user | md5sum | awk '{print $1}')
	cat <<- FIN > $sesd/SESSION.$sesid
	sessionid $sesid
	user $user
	login $todayhms
	FIN
	echo "Content-type: text/html"
	echo "Set-Cookie: sessionId=$sesid; path=/; expires=$(LANG=en_US;date -u +"%a, %d %b %Y 14:59:59 GMT")"
	echo ""
	cat <<- FIN
	<!DOCTYPE html>
	<html>
		<head>
		</head>
		<body onload="location.href='$REDIRECT'"></body>
	</html>
	FIN
else
	echo "Content-type: text/html"
	echo ""
	cat <<- FIN
	<!DOCTYPE html>
	<html>
		<head>
		</head>
		<body onload="location.href='/login'"></body>
	</html>
	FIN
fi

rm -rf $tmp-*
exit 0
