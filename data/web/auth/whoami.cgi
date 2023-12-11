#!/bin/bash -vx

export LANG=ja_JP.UTF-8

homd=/home/abc
sesd=$homd/session
logd=$homd/log

tmp=/tmp/tmp_$$

# logfile=LOG.${HOSTNAME}.$(basename $0)_$(date +%Y%m%d%H%M%S)_$$
# exec 2>$logd/$logfile

ERROR_HOLDER(){
	echo "Status: 403"
	echo "Content-type: text/html; charset=UTF-8"
	echo ""
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
	echo "Status: 403"
	echo "Content-type: text/html; charset=UTF-8"
	echo ""
	rm -rf $tmp-*
	exit 0
fi

# セッションファイルが存在しない場合はNG
if [ ! -s $sesd/SESSION.$sessionid ]; then
	echo "Status: 403"
	echo "Content-type: text/html; charset=UTF-8"
	echo ""
	rm -rf $tmp-*
	exit 0
fi

echo "Status: 200"
echo "Content-type: text/html"
echo ""
awk '$1=="user"{print $2}' $sesd/SESSION.$sessionid

rm -rf $tmp-*
exit 0
