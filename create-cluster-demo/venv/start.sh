#!/bin/bash
screen -S dst_web -X stuff "^C^M"
sleep 5
screen -dmS dst_web ./bin/uwsgi ./config.ini
# screen -dmS dst_web /www/wwwroot/dst.suke.fun/venv/bin/uwsgi /www/wwwroot/dst.suke.fun/venv/config.ini