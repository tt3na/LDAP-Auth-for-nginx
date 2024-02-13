#!/bin/bash

sed -i 's/User apache/User abc/g' /etc/httpd/conf/httpd.conf
sed -i 's/Group apache/Group abc/g' /etc/httpd/conf/httpd.conf

cat << FIN >> /etc/httpd/conf/httpd.conf

<Directory "/home/abc/web">
        Options +Indexes +FollowSymLinks +ExecCGI
	AddHandler cgi-script .cgi .ajax
        AllowOverride All
        Require all granted
</Directory>

NameVirtualHost *:80
<VirtualHost *:80>
    DocumentRoot /home/abc/web
</VirtualHost>
FIN

cat << FIN > /home/abc/web/.htaccess
SetEnv LDAP_HOST $LDAP_HOST
SetEnv LDAP_PORT $LDAP_PORT
SetEnv LDAP_BASE_DN $LDAP_BASE_DN
SetEnv REDIRECT $REDIRECT
FIN

cat << FIN >> /etc/httpd/conf.modules.d/00-mpm.conf
ScriptSock /var/run/httpd/cgid.sock
FIN

mkdir /home/abc/session
mkdir /home/abc/log

chown abc:abc /var/run/httpd
chown -R abc:abc /home/abc/session
chown -R abc:abc /home/abc/log

mv /etc/httpd/conf.d/welcome.conf /etc/httpd/conf.d/welcome.conf.bak

exec /usr/sbin/httpd -DFOREGROUND

exit 0
