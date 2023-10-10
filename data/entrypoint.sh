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

mv /etc/httpd/conf.d/welcome.conf /etc/httpd/conf.d/welcome.conf.bak

/usr/sbin/httpd -DFOREGROUND

exit 0
