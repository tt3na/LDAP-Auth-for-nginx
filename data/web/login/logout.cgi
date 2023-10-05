#!/bin/bash -vx

homd=/home/abc
sesd=$homd/session
logd=$homd/log
tmp=/tmp/tmp_$$

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

# Cookieの取得とセッション管理
if [ ! -z "$HTTP_COOKIE" ]; then
        echo "$HTTP_COOKIE"                    |
        sed 's/; /\n/g'                        |
        sed 's/=/ /g'                      > $tmp-cookie

        # CookieよりセッションIDを取得
        sessionid=$(awk '$1=="sessionId"{print $2}' $tmp-cookie)
else
	sessionid="none"
fi

# セッションファイルがある場合は消去
if [ -s $sesd/SESSION.$sessionid ]; then
	rm -rf $sesd/SESSION.$sessionid
fi

echo "Content-type: text/html"
echo "Set-Cookie: sessionId=; path=/;"
echo ""
cat <<- FIN
<!DOCTYPE html>
<html>
	<head>
	</head>
	<body onload="location.href='/login'"></body>
</html>
FIN

rm -rf $tmp-*
exit 0
