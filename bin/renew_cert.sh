#!/bin/bash

# Renew all SSL certs.
certbot renew > /root/cert-renew.log 2>&1
LE_STATUS=$?

if [ "$LT_STATUS" != 0 ]; then
	echo Automated SSL renewal failed:
	cat /root/cert-renew.log
	exit 1
fi

# Restart services
/usr/bin/systemctl restart nginx
