#!/usr/bin/python3
import os
def call(cmd):
    if cmd =='get_prod_list' :
        os.system('/home/ua10082/py/urcosme/get_prod_list.py &')
    elif cmd== 'get_review_detail':
        os.system('/home/ua10082/py/urcosme/get_review_detail.py &')
    elif cmd=='prod_review_list':
        os.system('/home/ua10082/py/urcosme/prod_review_list.py &')
    elif cmd=='get_user_reviews':
        os.system('/home/ua10082/py/urcosme/get_user_reviews.py &')
