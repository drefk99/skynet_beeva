#!/bin/bash
# -*- ENCODING: UTF-8 -*-

#If vietualenv is in another loction change the source

source ../env/bin/activate
yest_man=`expr $(date +%d) - 1`

python test_embed.py bancomer $(date +%Y-%m-$yest_man) $(date +%Y-%m-%d)
python test_embed.py banorte $(date +%Y-%m-$yest_man) $(date +%Y-%m-%d)
python test_embed.py banamex $(date +%Y-%m-$yest_man) $(date +%Y-%m-%d)
python test_embed.py scotiabank $(date +%Y-%m-$yest_man) $(date +%Y-%m-%d)
python test_embed.py HSBC $(date +%Y-%m-$yest_man) $(date +%Y-%m-%d)
python test_embed.py santander $(date +%Y-%m-$yest_man) $(date +%Y-%m-%d)
#python charls.py bancomer 2017-03-16 2017-03-17
