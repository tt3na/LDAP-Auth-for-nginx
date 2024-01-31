FROM almalinux:9

ENV LANG ja_JP.UTF-8
ENV TZ Asia/Tokyo

RUN groupadd -g 1000 abc
RUN useradd --uid 1000 --gid 1000 --shell /bin/bash -G abc abc

RUN ulimit -n 1024000 && yum update -y
RUN yum install -y httpd openldap-clients

RUN mv /etc/httpd/conf.d/welcome.conf /etc/httpd/conf.d/welcome.conf.bak

WORKDIR /home/abc

CMD ["/home/abc/entrypoint.sh"]
