#!/usr/bin/python3
import json
from py import jconfig2
import mysql.connector

def get_dataset_profile():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result={}
    
    sql = "SELECT count(*) FROM urcosme_reviews"
    cursor.execute(sql)
    for (u) in cursor:
        result['reviews']=u[0]
    
    sql = "SELECT count(*) FROM urcosme_users"
    cursor.execute(sql)
    for (u) in cursor:
        result['users']=u[0]
    
    sql = "SELECT count(*) FROM urcosme_brands"
    cursor.execute(sql)
    for (u) in cursor:
        result['brands']=u[0]

    sql = "SELECT count(*) FROM urcosme_prods"
    cursor.execute(sql)
    for (u) in cursor:
        result['prods']=u[0]

    
#    myobj=[result]
    return result
    #myobj=[{'id':1, 'name':"Oli Bob \n steve",'age':"55"},
    #    {'id':2, 'name':"Mary May", 'age':"1" },
    #    {'id':3, 'name':"Christine Lobowski", 'age':"42" },
    #    {'id':4, 'name':"Brendon Philips", 'age':"125" },
    #    {'id':5, 'name':"Margret Marmajuke", 'age':"16"}]
    
    
def get_comments():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database)
    cursor = cnx.cursor()
    myobj=[]
    
    sql = "select b.brand,p.name,r.age,r.content from urcosme_reviews r,urcosme_prods p,urcosme_brands b where p.prodid=r.prodid and p.brandid=b.pixid limit 100;"
    cursor.execute(sql)
    for (u) in cursor:
        myobj.append({'brand':u[0],'name':u[1],'age':u[2],'content':u[3]})
    return myobj
    
    
#    print(json.dumps(myobj))
def get_crawler_status():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database)
    cursor = cnx.cursor()
    myobj=[]
    
    sql = "SELECT logtype,max(logtime) FROM gsearch.crawler_log group by logtype order by max(logtime) desc limit 10"
    cursor.execute(sql)
    for (u) in cursor:
        myobj.append({'logtype':u[0],'val':str(u[1])})
    return myobj

def get_brand_sum_raw_ts():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port)
    cursor = cnx.cursor()
    myobj=[]
    
    sql = "select distinct brand_name FROM oneil.sum_raw_ts;"
    cursor.execute(sql)
    for (u) in cursor:
        myobj.append({'brand':u[0]})
    return myobj

def get_product_sum_raw_ts():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port)
    cursor = cnx.cursor()
    myobj=[]
    
    
    sql = "select distinct prod FROM oneil.sum_raw_ts;"
    cursor.execute(sql)
    for (u) in cursor:
        myobj.append({'product':u[0]})
        
    return myobj

def get_reviews():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database)
    cursor = cnx.cursor()
    myobj=[]
    
    sql = "select r.content from urcosme_reviews r,urcosme_prods p,urcosme_brands b where p.prodid=r.prodid and p.brandid=b.pixid limit 10;"
    cursor.execute(sql)
    for (u) in cursor:
        myobj.append({'content':u[0]})
    return myobj

def get_prod_1028():
    cnx = mysql.connector.connect(user='jared', password='iscae100',host='140.96.83.145',port=3306,database='gsearch', charset='utf8')
    cursor = cnx.cursor()
    myobj=[]
    sql = "select prodid,prodname,population,population*5 as population_viz,substring(listing_date,1,10),DATEDIFF(substring(listing_date,1,10),'2009-08-01')/10.0 as x_label,avg_score from gsearch.prod_1028"
    #sql = "select t.* ,g.raw_ts1,raw_ts2,concat(g.grow_rate,'(',g.grow_rate_percent,'%)') as 'lasted week growth' from Serena.toplist t ,Serena.grow_rate g where t.brand_name=g.brand_name and t.prod=g.prod order by g.grow_rate_percent desc"
    cursor.execute(sql)
    for (u) in cursor:
        myobj.append({'prodid':u[0],'prodname':u[1],'population':u[2],'population_viz':u[3],'listing_date':u[4],'x_label':u[5],'avg_score':u[6]})
    return myobj



def get_prodinfo():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database, charset='utf8')
    cursor = cnx.cursor()
    myobj=[]
    
    #sql = "select b.brand,p.name,r.age,r.content from urcosme_reviews r,urcosme_prods p,urcosme_brands b where b.brand='SK-II' and p.prodid=r.prodid and p.brandid=b.pixid limit 100;"
    sql = "select brandid,b.brand,p.category,avg(likes) as avg_likes,avg(buy) as avg_buy,avg( cast(REPLACE(price, 'NT$', '') as unsigned ) ) as avg_price,min(cast(REPLACE(price, 'NT$', '') as unsigned )) as min_price,max(cast(REPLACE(price, 'NT$', '') as unsigned )) as max_price  from gsearch.urcosme_prods p,gsearch.urcosme_brands b where REPLACE(price, 'NT$', '') !='' and REPLACE(price, 'NT$', '') not like'%---%' and REPLACE(price, 'NT$', '') not like '%/%' and p.brandid=b.pixid and p.brandid in ('7','76','24','224','68','38','81','50','53','55','113' ) group by brandid,b.brand,p.category order by avg_buy desc"
    cursor.execute(sql)
    for (u) in cursor:
        myobj.append({'Brand_Id':u[0],'brand_name':u[1],'Category':u[2],'Avg_likes':u[3],'Avg_Buy':u[4],'Avg_Price':u[5],'Min_Price':u[6],'Max_Price':u[7]})
    return myobj
                  

#myobj=[{'id':1, 'name':"Oli Bob \n steve",'age':"55"},
#    {'id':2, 'name':"Mary May", 'age':"1" },
#    {'id':3, 'name':"Christine Lobowski", 'age':"42" },
#    {'id':4, 'name':"Brendon Philips", 'age':"125" },
#    {'id':5, 'name':"Margret Marmajuke", 'age':"16"}]

#  print(json.dumps(myobj))



