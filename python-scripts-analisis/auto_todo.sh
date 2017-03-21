#!/bin/bash
# -*- ENCODING: UTF-8 -*-



source /home/graduate/Bank_sentiment_analysis/env/bin/activate
yest_man=`expr $(date +%d) - 1`

python test_embed.py bancomer $(date +%Y-%m-$yest_man) $(date +%Y-%m-%d)
python test_embed.py banorte $(date +%Y-%m-$yest_man) $(date +%Y-%m-%d)
python test_embed.py banamex $(date +%Y-%m-$yest_man) $(date +%Y-%m-%d)
python test_embed.py scotiabank $(date +%Y-%m-$yest_man) $(date +%Y-%m-%d)
python test_embed.py HSBC $(date +%Y-%m-$yest_man) $(date +%Y-%m-%d)
python test_embed.py santander $(date +%Y-%m-$yest_man) $(date +%Y-%m-%d)
#python charls.py bancomer 2017-03-16 2017-03-17
