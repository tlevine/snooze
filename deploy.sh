#!/bin/sh

git push
ssh www-data@thomaslevine.com 'cd /srv/www/snooze; git pull'
