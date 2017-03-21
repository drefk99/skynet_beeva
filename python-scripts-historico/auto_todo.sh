#!/bin/bash
# -*- ENCODING: UTF-8 -*-



source env/bin/activate
yest_man=`expr $(date +%d) + 1`

python charls.py bancomer $(date +%Y-%m-%d) $(date +%Y-%m-$yest_man)
#python charls.py bancomer 2017-03-16 2017-03-17
