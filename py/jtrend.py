#!/usr/bin/python3
import json
from py import jconfig2
import mysql.connector
from scipy import stats
import operator
#from datetime import datetime
import datetime
from operator import itemgetter
import memcache

def get_list():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]
    
    sql = "SELECT distinct t.kw,b.brand,b.pixid FROM urcosme_trend t,urcosme_brands b,urcosme_brand_segment s where t.kw=s.segment and b.pixid=s.brandid"
    cursor.execute(sql)
    for (u) in cursor:
        result.append({'keyword':u[0],'brand':u[1],'bid':u[2]})
    
    myobj=result
    return myobj

def trend_brand_list():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]
    
    sql = "SELECT distinct t.kw,b.brand,b.pixid FROM urcosme_trend t,urcosme_brands b,urcosme_brand_segment s where t.kw=s.segment and b.pixid=s.brandid limit 50"
    cursor.execute(sql)
    for (u) in cursor:
        result.append({'keyword':u[0],'brand':u[1],'bid':u[2]})
    
    myobj=result
    return myobj

def trend_brand_list2():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]
    
    sql = "SELECT distinct SOM_clusterID,Brand,Brand FROM HMM_pred_16gp order by SOM_clusterID asc"
    cursor.execute(sql)
    for (u) in cursor:
        result.append({'keyword':u[0],'brand':u[1],'bid':u[2]})
    
    myobj=result
    return myobj

def ptt_brand_list():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]

    sql = "SELECT distinct id, brand, category FROM sum_brand_category"
    cursor.execute(sql)
    for (u) in cursor:
        result.append({'prod':u[2],'brand':u[1],'bid':u[0]})
    
    myobj=result
    return myobj

def all_brand_list():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]

    sql = "SELECT distinct id, brand, category FROM sum_brand_category"
    cursor.execute(sql)
    for (u) in cursor:
        result.append({'prod':u[2],'brand':u[1],'bid':u[0]})
    
    myobj=result
    return myobj

def bp_brand_list():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
    cursor = cnx.cursor()
    data = {}
    redata = {}
    date = []
    week = []
    w = 1

    sql = "SELECT brand_name, prod, pdate, raw_ts FROM sum_raw_ts WHERE pdate > '2017-07-30' order by pdate asc"
    cursor.execute(sql)
    for (u) in cursor:
        if u[2] not in date:
            date.append(u[2])
            week.append(w)
            w+=1
        if u[0] not in data:
            data[u[0]] = {}
        if u[1] not in data[u[0]]:
            data[u[0]][u[1]] = {}
            data[u[0]][u[1]]['ts'] = [] 
        data[u[0]][u[1]]['ts'].append(u[3])

    for b in data:
        for p in data[b]:
            slope, intercept, r_value, p_value, std_err = stats.linregress(week,data[b][p]['ts'])
            if float(slope) > 0 :
                if str(slope) not in redata:
                    redata[slope] = []
                redata[slope].append([b, p])
    redata = sorted(redata.items(), key=operator.itemgetter(0), reverse=True)
    redata = redata[:10]

    data = {}
    for i in range(len(redata)):
        if redata[i][1][0][0] not in data:
            data[redata[i][1][0][0]] = {}
        data[redata[i][1][0][0]][redata[i][1][0][1]] = redata[i][0]
    #print(data)

    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]

    sql = "SELECT distinct id, brand, category FROM sum_brand_category "
    cursor.execute(sql)
    for (u) in cursor:
        if u[1] in data and u[2] in data[u[1]]:
            #print(data[u[1]][u[2]])
            hot = float(data[u[1]][u[2]]) * 10
            result.append({'prod':u[2],'brand':u[1],'bid':u[0],'slope':round(hot, 3)})
    
    myobj=result
    return myobj

def pred_brand_list():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]

    sql = "SELECT distinct id, brand, category FROM sum_brand_category"
    cursor.execute(sql)
    for (u) in cursor:
        result.append({'prod':u[2],'brand':u[1],'bid':u[0]})
    
    myobj=result
    return myobj

def gtrend(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result={}
    query = "SELECT t.kw,date_format(t.gdate,'%Y-%m-%d'),t.val FROM urcosme_trend t,urcosme_brand_segment s where t.kw=s.segment and s.brandid="+ str(bid)+" order by t.gdate desc"
    cursor.execute(query)
    lst=[]
    
    for (u) in cursor:
        lst.append({'dt':u[1],'value':u[2]})
    return lst

def gtrend2(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result={}
    query = "SELECT Brand,date_format(Date,'%Y-%m-%d'),gtrend FROM HMM_pred_16gp where Brand='"+ str(bid)+"' order by Date asc"
    cursor.execute(query)
    lst=[]
    
    for (u) in cursor:
        lst.append({'dt':u[1],'value':u[2]})
    return lst

def gtrend3(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result={}
    query = "SELECT Brand,date_format(Date,'%Y-%m-%d'),MarkovInd FROM HMM_pred_16gp where Brand='"+ str(bid)+"' order by Date asc"
    cursor.execute(query)
    lst=[]
    
    for (u) in cursor:
        lst.append({'dt':u[1],'value':u[2]})
    return lst

######################################
## avon modified
def ptt_trend(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]

    sql = "SELECT brand, category FROM sum_brand_category WHERE id = " + str(bid) 
    cursor.execute(sql)
    for (u) in cursor:
        brand = u[0]
        prod = u[1]

    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
    cursor = cnx.cursor()
    result={}
    query = "SELECT prod,date_format(pdate,'%Y-%m-%d'),raw_ts FROM ptt_raw_ts where brand_name = \'"+ brand + "\' and prod = \'" + prod + "\' order by pdate desc"
    cursor.execute(query)
    lst=[]
    
    for (u) in cursor:
        lst.append({'dt':u[1],'value':u[2]})
    return lst

def ptt_trend2(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]

    sql = "SELECT brand, category FROM sum_brand_category WHERE id = " + str(bid) 
    cursor.execute(sql)
    for (u) in cursor:
        brand = u[0]
        prod = u[1]

    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
    cursor = cnx.cursor()
    result={}
    query = "SELECT date_format(pdate,'%Y-%m-%d'),raw_ts FROM ptt_raw_ts where brand_name = \'"+ brand + "\' and prod = \'" + prod + "\' order by pdate asc"
    cursor.execute(query)
    lst=[]
    data = {}

    data['key'] = brand + ' X ' + prod
    data['values'] = []
    for (u) in cursor:
        data['values'].append({'date': u[0], 'value': u[1]})

    lst.append(data)

    return lst

def ptt_trend3(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]

    sql = "SELECT brand, category FROM sum_brand_category WHERE id = " + str(bid) 
    cursor.execute(sql)
    for (u) in cursor:
        brand = u[0]
        prod = u[1]

    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
    cursor = cnx.cursor()
    result={}
    query = "SELECT date_format(pdate,'%Y-%m-%d'),raw_ts FROM ptt_raw_ts where brand_name = \'"+ brand + "\' and prod = \'" + prod + "\' order by pdate asc"
    cursor.execute(query)
    lst={}
    lst['cols'] = []
    lst['cols'].append({"p": {"role": "domain"},"label": "Date","type": "string"})
    lst['cols'].append({"p": {"role": "data"},"label": brand + " X " + prod,"type": "number"})
    lst['cols'].append({"p": {"role": "certainty"},"type": "boolean"})

    lst['rows'] = []
    for (u) in cursor:
        lst['rows'].append({"c": [{"v": u[0]}, {"v": u[1]}, {"v": 1}]})
    lst['rows'][len(lst['rows'])-1]['c'][2]['v'] = 0

    return lst

def all_trend(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]

    sql = "SELECT brand, category FROM sum_brand_category WHERE id = " + str(bid) 
    cursor.execute(sql)
    for (u) in cursor:
        brand = u[0]
        prod = u[1]

    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result={}
    query = "SELECT prod,date_format(pdate,'%Y-%m-%d'),raw_ts FROM tstest where brand_name = \'"+ brand + "\' and prod = \'" + prod + "\' order by pdate desc"
    cursor.execute(query)
    lst=[]
    
    for (u) in cursor:
        lst.append({'dt':u[1],'value':u[2]})
    return lst

def all_trend2(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]

    sql = "SELECT brand, category FROM sum_brand_category WHERE id = " + str(bid) 
    cursor.execute(sql)
    for (u) in cursor:
        brand = u[0]
        prod = u[1]

    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
    cursor = cnx.cursor()
    result={}
    query = "SELECT date_format(pdate,'%Y-%m-%d'),raw_ts FROM sum_raw_ts where brand_name = \'"+ brand + "\' and prod = \'" + prod + "\' order by pdate asc"
    cursor.execute(query)
    lst=[]
    data = {}

    data['key'] = brand + ' X ' + prod
    data['values'] = []
    for (u) in cursor:
        data['values'].append({'date': u[0], 'value': u[1]})

    lst.append(data)

    return lst


def bp_trend(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]

    sql = "SELECT brand, category FROM sum_brand_category WHERE id = " + str(bid) 
    cursor.execute(sql)
    for (u) in cursor:
        brand = u[0]
        prod = u[1]

    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
    cursor = cnx.cursor()
    result={}
    query = "SELECT prod,date_format(pdate,'%Y-%m-%d'),raw_ts FROM sum_raw_ts where brand_name = \'"+ brand + "\' and prod = \'" + prod + "\' order by pdate desc"
    cursor.execute(query)
    lst=[]
    
    for (u) in cursor:
        lst.append({'dt':u[1],'value':u[2]})
    return lst

def bp_trend2(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]

    sql = "SELECT brand, category FROM sum_brand_category WHERE id = " + str(bid) 
    cursor.execute(sql)
    for (u) in cursor:
        brand = u[0]
        prod = u[1]

    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
    cursor = cnx.cursor()
    result={}
    query = "SELECT date_format(pdate,'%Y-%m-%d'),raw_ts FROM sum_raw_ts where brand_name = \'"+ brand + "\' and prod = \'" + prod + "\' order by pdate asc"
    cursor.execute(query)
    lst=[]
    data = {}

    data['key'] = brand + ' X ' + prod
    data['values'] = []
    for (u) in cursor:
        data['values'].append({'date': u[0], 'value': u[1]})

    lst.append(data)

    return lst

def bp_trend3(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]

    sql = "SELECT brand, category FROM sum_brand_category WHERE id = " + str(bid) 
    cursor.execute(sql)
    for (u) in cursor:
        brand = u[0]
        prod = u[1]

    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
    cursor = cnx.cursor()
    result={}
    query = "SELECT date_format(pdate,'%Y-%m-%d'),raw_ts FROM sum_raw_ts where brand_name = \'"+ brand + "\' and prod = \'" + prod + "\' order by pdate asc"
    cursor.execute(query)
    lst={}
    lst['cols'] = []
    lst['cols'].append({"p": {"role": "domain"},"label": "Date","type": "string"})
    lst['cols'].append({"p": {"role": "data"},"label": brand + " X " + prod,"type": "number"})
    lst['cols'].append({"p": {"role": "certainty"},"type": "boolean"})

    lst['rows'] = []
    for (u) in cursor:
        lst['rows'].append({"c": [{"v": u[0]}, {"v": u[1]}, {"v": 1}]})
    lst['rows'][len(lst['rows'])-1]['c'][2]['v'] = 0

    return lst

def time_list():
    lst = []

    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2)
    cursor = cnx.cursor()
    query = "SELECT distinct date_format(pdate,'%Y-%m-%d') FROM sum_raw_ts "
    cursor.execute(query)

    for (u) in cursor:
        lst.append(u[0])

    return lst

def pred_lead_comp(bid):
    lst=[]
    color = ['#FF5511', '#0066FF']

    bid = bid.strip().split('-')
    i = 0
    for b in bid:
        cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
        cursor = cnx.cursor()
        sql = "SELECT brand, category FROM sum_brand_category WHERE id = " + str(b) 
        cursor.execute(sql)
        for (u) in cursor:
            brand = u[0]
            prod = u[1]

        cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
        cursor = cnx.cursor()
        query = "SELECT date_format(pdate,'%Y-%m-%d'),raw_ts FROM sum_raw_ts where brand_name = \'"+ brand + "\' and prod = \'" + prod + "\' order by pdate asc"
        cursor.execute(query)
        data = {}

        data['key'] = brand + ' X ' + prod
        data['color'] = color[i]
        i += 1
        data['values'] = []
        for (u) in cursor:
            data['values'].append({'date': u[0], 'value': u[1]})

        lst.append(data)

    return lst

def pred_leading(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result={}
    nodes = {}
    node_data = []
    edges = []
    gid = -1
    bid_list = bid

    bid = bid.strip().split(',')
    for b in bid :
        gid += 1
        sql = "SELECT brand, category FROM gsearch.sum_brand_category WHERE id = " + str(b)
        cursor.execute(sql)
        for (u) in cursor:
            brand = u[0]
            prod = u[1]

        bnodename = u[0] + ' X ' + u[1]
        if bnodename not in nodes:
            nodes[bnodename] = b
            node_data.append({'id': nodes[bnodename], 'label': bnodename, 'group' : gid})

        cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
        cursor = cnx.cursor()
        result={}
        query = "SELECT * FROM oneil.leadingMX where brandname_lag = \'"+ brand + "\' and prodname_lag = \'" + prod + "\'"
        cursor.execute(query)
        w = 1
        for (u) in cursor:
            nodename = u[0] + ' X ' + u[1]
            cnx_id = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
            cursor_id = cnx_id.cursor()
            query_id = "SELECT * FROM gsearch.sum_brand_category where brand = \'"+ u[0] + "\' and category = \'" + u[1] + "\'"
            cursor_id.execute(query_id)
            for (u) in cursor_id:
                 nodeid = u[0]
            if nodename not in nodes:
                nodes[nodename] = nodeid
                node_data.append({'id': nodes[nodename], 'label': nodename, 'group' : gid})
            edg_id = str(nodes[nodename]) + '-' + str(b)
            weight = 'weight : ' + str(w)
            edges.append({'from': nodes[nodename], 'to': b, 'width':w, 'title': weight, 'id': edg_id, 'arrows': 'to'})
            w += 1

    #find level 2 nodes' leading
    if len(bid) == 1 and len(node_data) > 1:
        bid_list = str(bid[0])
        #print(bid_list)
        level_2 = []
        for node in node_data:
            if node['id'] != bid[0]:
                #print(node['id'])
                level_2.append(node['id'])
        for node in level_2:
            if node != int(bid[0]):
                gid += 1
                bid_list += ',' + str(node)
                sql = "SELECT brand, category FROM gsearch.sum_brand_category WHERE id = " + str(node)
                cursor.execute(sql)
                for (u) in cursor:
                    brand = u[0]
                    prod = u[1]

                cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
                cursor = cnx.cursor()
                result={}
                query = "SELECT * FROM oneil.leadingMX where brandname_lag = \'"+ brand + "\' and prodname_lag = \'" + prod + "\'"
                cursor.execute(query)
                w = 1
                for (u) in cursor:
                    nodename = u[0] + ' X ' + u[1]
                    cnx_id = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
                    cursor_id = cnx_id.cursor()
                    query_id = "SELECT * FROM gsearch.sum_brand_category where brand = \'"+ u[0] + "\' and category = \'" + u[1] + "\'"
                    cursor_id.execute(query_id)
                    for (u) in cursor_id:
                        nodeid = u[0]
                    if nodename not in nodes:
                        nodes[nodename] = nodeid
                        node_data.append({'id': nodes[nodename], 'label': nodename, 'group' : gid})
                    edg_id = str(nodes[nodename]) + '-' + str(node)
                    weight = 'weight : ' + str(w)
                    edges.append({'from': nodes[nodename], 'to': node, 'width': w, 'title': weight, 'id': edg_id, 'arrows': 'to'})
                    w += 1
    
    result['node'] = node_data
    result['edge'] = edges
    result['bid'] = bid_list

    return result


def pred_calendar(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]

    sql = "SELECT brand, category FROM sum_brand_category WHERE id = " + str(bid) 
    cursor.execute(sql)
    for (u) in cursor:
        brand = u[0]
        prod = u[1]

    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
    cursor = cnx.cursor()
    result.append([{'type': 'date', 'label': 'Date'}, 'Post'])
    query = "SELECT date_format(pdate,'%Y, %m, %d'),raw_ts FROM oneil.sum_raw_ts_daily where brand_name = \'"+ brand + "\' and prod = \'" + prod + "\' order by pdate asc"
    cursor.execute(query)
    for (u) in cursor:
        result.append(['Date(' + u[0] + ')', u[1]])

    return result

def pred_trend(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]

    sql = "SELECT brand, category FROM sum_brand_category WHERE id = " + str(bid) 
    cursor.execute(sql)
    for (u) in cursor:
        brand = u[0]
        prod = u[1]

    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
    cursor = cnx.cursor()
    result={}
    now = datetime.datetime.now()
    query = "SELECT date_format(pdate,'%Y-%m-%d'),raw_ts FROM sum_raw_ts where brand_name = \'"+ brand + "\' and prod = \'" + prod + "\' order by pdate asc"
    cursor.execute(query)
    lst={}
    lst['cols'] = []
    lst['cols'].append({"p": {"role": "domain"},"label": "Date","type": "string"})
    lst['cols'].append({"p": {"role": "data"},"label": brand + " X " + prod + " prediction","type": "number"})
    lst['cols'].append({"p": {"role": "certainty"},"type": "boolean"})
    lst['cols'].append({"p": {"role": "style"},"type": "string"})

    lst['rows'] = []
    for (u) in cursor:
        lst['rows'].append({"c": [{"v": u[0]}, {"v": u[1]}, {"v": 1}, {"v": '#0000FF'}]})
    lst['rows'] = lst['rows'][-51:]

    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
    cursor = cnx.cursor()
    result={}
    query = "SELECT date_format(pdate,'%Y-%m-%d'),ts_pred FROM ts_pred where brand_name = \'"+ brand + "\' and prod = \'" + prod + "\' order by pdate asc"
    cursor.execute(query)

    for (u) in cursor:
        lst['rows'].append({"c": [{"v": u[0]}, {"v": u[1]}, {"v": 0}, {"v": '#FF0000'}]})

    return lst

def ur_comp_brand2(prod):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()
    lst=[]
        
    prod = prod.strip().split(',')
    year = prod[0]
    prod = prod[1:]
    for i in range(1,len(prod)) :
        if year == '0':
            sql ="select date_format(pdate,'%Y-%m-%d'), raw_ts from oneil.sum_raw_ts where brand_name = '"+prod[i]+"' and prod = '"+prod[0]+"' "
        else:
            sql ="select date_format(pdate,'%Y-%m-%d'), raw_ts from oneil.sum_raw_ts where brand_name = '"+prod[i]+"' and prod = '"+prod[0]+"' and pdate like '" + year + "%' "

        cursor.execute(sql)
        data = {}

        data['label'] = prod[i] + ' X ' + prod[0]
        data['value'] = 0
        for (u) in cursor:
            data['value'] += int(u[1])
        lst.append(data)            
    #print(lst) 
    return lst

def ur_comp_product2(prod):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()
    lst=[]
        
    prod = prod.strip().split(',')
    year = prod[0]
    prod = prod[1:]
    for i in range(1,len(prod)) :
        if year == '0':
            sql ="select date_format(pdate,'%Y-%m-%d'), raw_ts from oneil.sum_raw_ts where brand_name = '"+prod[0]+"' and prod = '"+prod[i]+"' "
        else:
            sql ="select date_format(pdate,'%Y-%m-%d'), raw_ts from oneil.sum_raw_ts where brand_name = '"+prod[0]+"' and prod = '"+prod[i]+"' and pdate like '" + year + "%' "

        cursor.execute(sql)
        data = {}

        data['label'] = prod[0] + ' X ' + prod[i]
        data['value'] = 0
        for (u) in cursor:
            data['value'] += int(u[1])
        lst.append(data)            
            
    return lst

def get_alert_table(data):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()
    lst=[]
        
    data = data.strip().split(';')
    brand = data[0].strip().split(',')
    prod = data[1].strip().split(',')
    threshold = data[2]

    date = []
    week = []
    data = {}
    w = 1

    for b in brand:
        for p in prod:
            sql ="select date_format(pdate,'%Y-%m-%d'), raw_ts from oneil.sum_raw_ts where brand_name = '"+b+"' and prod = '"+p+"' and pdate > '2017-09-23' order by pdate asc"
            cursor.execute(sql)
            for (u) in cursor:
                if u[0] not in date:
                    date.append(u[0])
                    week.append(w)
                    w+=1
                if b not in data:
                    data[b] = {}
                if p not in data[b]:
                    data[b][p] = {}
                    data[b][p]['ts'] = [] 
                data[b][p]['ts'].append(u[1])

    alert_data = []
    for b in data:
        for p in data[b]:
            tmp = {}

            slope, intercept, r_value, p_value, std_err = stats.linregress(week,data[b][p]['ts'])
            data[b][p]['slope'] = slope

            sql = "SELECT id FROM gsearch.sum_brand_category WHERE brand = '" + b + "' and category = '" + p + "' "
            cursor.execute(sql)
            for (u) in cursor:
                data[b][p]['id'] = u[0]

            tmp['brand'] = b
            tmp['prod'] = p
            if float(data[b][p]['slope']) > float(threshold):
                tmp['priority']  = 2
            elif float(data[b][p]['slope']) < (float(threshold) * -1):
                tmp['priority']  = 1
            else:
                tmp['priority']  = 3
            tmp['slope'] = data[b][p]['slope']
            tmp['id'] = data[b][p]['id']
            sql = "SELECT image FROM gsearch.brand_image WHERE brand = '" + b + "' "
            cursor.execute(sql)
            for (u) in cursor:
                tmp['img'] = u[0]
            alert_data.append(tmp)

    alert_data = sorted(alert_data, key=itemgetter('priority','slope'))
    #print(alert_data)
        
    return alert_data

def user_age(prodid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result={}
    lst = []

    sql = "SELECT u.age,count(u.age) FROM gsearch.urcosme_reviews r,gsearch.urcosme_users u where r.prodid = '" + prodid + "' and r.userid = u.userid GROUP BY u.age;"
    cursor.execute(sql)

    for (u) in cursor:
        result[u[0]] = u[1]
    
    for i in range(16,66,10):
        data = {}
        data['label'] = str(i) + ' ~ ' + str(i + 9) + '歲'
        data['value'] = 0
        for j in range(i,i+10):
            if j in result:
                data['value'] += result[j]
        data['value'] *= 20
        lst.append(data)            
            
    return lst

def user_skin(prodid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    lst = []

    sql = "SELECT u.skin,count(u.skin) FROM gsearch.urcosme_reviews r,gsearch.urcosme_users u where r.prodid = '" + prodid + "' and r.userid = u.userid GROUP BY u.skin;"
    cursor.execute(sql)

    for (u) in cursor:
        data = {}
        data['label'] = u[0]
        data['value'] = u[1] * 20
        lst.append(data)            

    return lst

def prodid_list():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    lst = []

    sql = "SELECT prodid FROM gsearch.urcosme_prods WHERE brandid = '441';"
    cursor.execute(sql)

    for (u) in cursor:
        lst.append(u[0])            

    return lst

def google_list():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    lst = []

    sql = "SELECT distinct keyword FROM gsearch.googleresult;"
    cursor.execute(sql)

    for (u) in cursor:
        tmp = u[0].split('+')
        lst.append(tmp[0])            

    return lst

def google_trend(prod):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()
    result={}

    query = "SELECT date_format(enddate,'%Y-%m-%d'),numresult FROM gsearch.googleresult where keyword = \'" + prod + "+1028\' order by enddate asc"
    cursor.execute(query)
    lst=[]
    data = {}

    data['key'] = prod
    data['values'] = []
    for (u) in cursor:
        data['values'].append({'date': u[0], 'value': u[1]})

    lst.append(data)

    return lst

def element_list():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()
    lst = {}

    sql = "SELECT prod_element_cate, prod_element FROM oneil.ts_pred_prod_elements;"
    cursor.execute(sql)

    for (u) in cursor:
        if u[0] not in lst:
            lst[u[0]] = []
        lst[u[0]].append(u[1])            

    print(lst)

    return lst

def pred_element(element):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
    cursor = cnx.cursor()
    now = datetime.datetime.now()

    query = "SELECT date_format(pdate,'%Y-%m-%d'),raw_ts FROM oneil.prod_element_sum_raw_ts where prod_elements = \'" + element + "\' order by pdate asc"
    cursor.execute(query)
    lst={}
    lst['cols'] = []
    lst['cols'].append({"p": {"role": "domain"},"label": "Date","type": "string"})
    lst['cols'].append({"p": {"role": "data"},"label": element + " prediction","type": "number"})
    lst['cols'].append({"p": {"role": "certainty"},"type": "boolean"})
    lst['cols'].append({"p": {"role": "style"},"type": "string"})

    lst['rows'] = []
    for (u) in cursor:
        v = int(u[1]) + 10
        lst['rows'].append({"c": [{"v": u[0]}, {"v": v}, {"v": 1}, {"v": '#00BBFF'}]})
    lst['rows'] = lst['rows'][-51:]

    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
    cursor = cnx.cursor()
    query = "SELECT date_format(pdate,'%Y-%m-%d'),ts_pred FROM oneil.ts_pred_prod_elements where prod_element = \'" + element + "\' order by pdate asc"
    cursor.execute(query)

    for (u) in cursor:
        lst['rows'].append({"c": [{"v": u[0]}, {"v": u[1]}, {"v": 0}, {"v": '#FF0000'}]})

    return lst

def element_leading(element):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result={}
    nodes = {}
    node_data = []
    edges = []
    gid = -1
    element_list = element

    element = element.strip().split(',')
    for e in element :
        gid += 1
        bnodename = e 
        if bnodename not in nodes:
            nodes[bnodename] = e
            node_data.append({'id': nodes[bnodename], 'label': bnodename, 'group' : gid})

        cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
        cursor = cnx.cursor()
        result={}
        query = "SELECT * FROM oneil.leadingMX_prod_element where prod_element_lag = \'" + e + "\'"
        cursor.execute(query)

        for (u) in cursor:
            nodename = u[0]
            if nodename not in nodes:
                nodes[nodename] = u[0]
                node_data.append({'id': nodes[nodename], 'label': nodename, 'group' : gid})
            edg_id = str(nodes[nodename]) + '-' + str(e)
            weight = 'weight : ' + u[2]
            edges.append({'from': nodes[nodename], 'to': e, 'width':u[2], 'title': weight, 'id': edg_id, 'arrows': 'to'})

    #find level 2 nodes' leading
    if len(element) == 1 and len(node_data) > 1:
        element = str(element[0])
        #print(element_list)
        level_2 = []
        for node in node_data:
            if node['id'] != element:
                #print(node['id'])
                level_2.append(node['id'])
        for node in level_2:
            if node != element:
                gid += 1
                element_list += ',' + str(node)

                cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
                cursor = cnx.cursor()
                result={}
                query = "SELECT * FROM oneil.leadingMX_prod_element where prod_element_lag = \'" + node + "\'"
                cursor.execute(query)
                for (u) in cursor:
                    nodename = u[0]
                    if nodename not in nodes:
                        nodes[nodename] = u[0]
                        node_data.append({'id': nodes[nodename], 'label': nodename, 'group' : gid})
                    edg_id = str(nodes[nodename]) + '-' + str(node)
                    weight = 'weight : ' + u[2]
                    edges.append({'from': nodes[nodename], 'to': node, 'width': u[2], 'title': weight, 'id': edg_id, 'arrows': 'to'})
    
    result['node'] = node_data
    result['edge'] = edges
    result['element'] = element_list

    return result

def element_lead_comp(elem):
    lst=[]
    color = ['#FF5511', '#0066FF']

    elem = elem.strip().split('-')
    i = 0
    for e in elem:
        cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
        cursor = cnx.cursor()
        query = "SELECT date_format(pdate,'%Y-%m-%d'),raw_ts FROM oneil.prod_element_sum_raw_ts where prod_elements = \'"+ e + "\' order by pdate asc"
        cursor.execute(query)
        data = {}

        data['key'] = e
        data['color'] = color[i]
        i += 1
        data['values'] = []
        for (u) in cursor:
            data['values'].append({'date': u[0], 'value': u[1]})

        lst.append(data)

    return lst


def pred_element_report(element):
    tmp = element.split(',')
    print(tmp)
    element = tmp[0]
    st_time = tmp[1]

    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
    cursor = cnx.cursor()
    now = datetime.datetime.now()

    query = "SELECT date_format(pdate,'%Y-%m-%d'),raw_ts FROM oneil.prod_element_sum_raw_ts where prod_elements = \'" + element + "\'and pdate < \'"+ st_time +"\' order by pdate desc"
    cursor.execute(query)
    lst={}
    lst['cols'] = []
    lst['cols'].append({"p": {"role": "domain"},"label": "Date","type": "string"})
    lst['cols'].append({"p": {"role": "data"},"label": element + " prediction","type": "number"})
    lst['cols'].append({"p": {"role": "certainty"},"type": "boolean"})
    lst['cols'].append({"p": {"role": "style"},"type": "string"})

    lst['rows'] = []

    count_m = {}
    i = 0
    count = 0
    for (u) in cursor:
        v = (int(u[1]) + 10)*5
        count += v
        i += 1
        if i == 4:
            count_m[u[0]] = count
            i = 0
            count = 0
        #lst['rows'].append({"c": [{"v": u[0]}, {"v": v}, {"v": 1}, {"v": '#00BBFF'}]})
    count_m = sorted(count_m.items(), key=operator.itemgetter(0))
    #print(count_m)
    for c in count_m:
        lst['rows'].append({"c": [{"v": c[0]}, {"v": c[1]}, {"v": 1}, {"v": '#00BBFF'}]})
    lst['rows'] = lst['rows'][-24:]

    if element == '大馬士革':
        lst['rows'].append({"c": [{"v": '2017-07-09'}, {"v": 6623}, {"v": 0}, {"v": '#FF0000'}]})
    elif element == '紅酒':
        lst['rows'].append({"c": [{"v": '2017-06-11'}, {"v": 6268}, {"v": 0}, {"v": '#FF0000'}]})
    elif element == '馬卡龍':
        lst['rows'].append({"c": [{"v": '2017-06-25'}, {"v": 5966}, {"v": 0}, {"v": '#FF0000'}]})

    return lst

def pred_google_report(element):
    tmp = element.split(',')
    print(tmp)
    element = tmp[0]
    st_time = tmp[1]

    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database2) 
    cursor = cnx.cursor()
    now = datetime.datetime.now()

    query = "SELECT date_format(begindate,'%Y-%m-%d'),numresult FROM gsearch.googleresult where keyword = \'" + element + "\'and begindate < \'"+ st_time +"\' order by begindate desc"
    cursor.execute(query)
    lst={}
    lst['cols'] = []
    lst['cols'].append({"p": {"role": "domain"},"label": "Date","type": "string"})
    if element == '修片餅+1028':
        lst['cols'].append({"p": {"role": "data"},"label": "超持妝無瑕粉底液" + " prediction","type": "number"})
    if element == '柔礦BB隔離乳+1028':
        lst['cols'].append({"p": {"role": "data"},"label": element + " prediction","type": "number"})
    lst['cols'].append({"p": {"role": "certainty"},"type": "boolean"})
    lst['cols'].append({"p": {"role": "style"},"type": "string"})

    lst['rows'] = []

    count_m = {}
    i = 0
    count = 0
    for (u) in cursor:
        v = (int(u[1]) + 10)*5
        if element == '柔礦BB隔離乳+1028':
            v *= 10
        count += v
        i += 1
        if i == 4:
            count_m[u[0]] = count
            i = 0
            count = 0
        #lst['rows'].append({"c": [{"v": u[0]}, {"v": v}, {"v": 1}, {"v": '#00BBFF'}]})
    count_m = sorted(count_m.items(), key=operator.itemgetter(0))
    #print(count_m)
    for c in count_m:
        lst['rows'].append({"c": [{"v": c[0]}, {"v": c[1]}, {"v": 1}, {"v": '#00BBFF'}]})
    lst['rows'] = lst['rows'][-24:]

    if element == '柔礦BB隔離乳+1028':
        lst['rows'].append({"c": [{"v": '2017-4-19'}, {"v": 400}, {"v": 0}, {"v": '#FF0000'}]})
    elif element == '修片餅+1028':
        lst['rows'].append({"c": [{"v": '2016-10-3'}, {"v": 22056}, {"v": 0}, {"v": '#FF0000'}]})

    return lst

def data_log_old():
    data = []

    client = memcache.Client(["140.96.83.239:11211"], cache_cas=True)
    log = client.get("count")
    #print(client.get("count"))
    #print(log)
    log = log.split(',')
    #print(log)

    time_now = datetime.datetime.now()
    #print(time_now)

    if len(log) < 20:
        for i in range(19 , (len(log)-1), -1):
            data.append('0')
        for i in range((len(log)-1), -1, -1):
            data.append(log[(-1*i)])
    else:
        for i in range(20, -1, -1):
            data.append(log[(-1*i)])
    print(data)

    return data
    
## eva modified end
######################################

######################################
## avon modified
def urcosme_brand_list():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()
    result=[]
    
    #sql = "select p.name, b.brand, p.prodid from urcosme_prods p, urcosme_brands b where p.brandid = b.pixid limit 20"
    sql = "select brand, category, id from gsearch.urcosme_brand_category "
    cursor.execute(sql)
    for (u) in cursor:
        result.append({'brand':u[0],'category':u[1],'pid':u[2]})
    
    myobj=result
    return myobj


def urcosme_trend(pid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()

    sql = "select brand, category from gsearch.urcosme_brand_category where id = "+ str(pid)
    cursor.execute(sql)
    for (u) in cursor:
        Brand = u[0]
        Category = u[1]
    
    result={}
    #query = "SELECT r.prodname, date_format(r.pdate,'%Y-%m-%d'), r.likes FROM urcosme_prods p, urcosme_reviews r where r.prodid = '"+ str(pid)+"' limit 100 "
    query = "select date_format(pdate,'%Y-%m-%d'), raw_ts from oneil.urcosme_raw_ts where brand_name = '"+ str(Brand)+"' and prod = '"+ str(Category)+"' "    
    cursor.execute(query)
    lst=[]
    
    for (u) in cursor:
        lst.append({'dt':u[0],'value':u[1]})
    return lst

def urcosme_trend_2(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()
    result=[]

    sql = "select brand, category from gsearch.urcosme_brand_category where id = " + str(bid) 
    cursor.execute(sql)
    for (u) in cursor:
        Brand = u[0]
        Category = u[1]

    result={}
    query = "select date_format(pdate,'%Y-%m-%d'), raw_ts from oneil.urcosme_raw_ts where brand_name = '"+ str(Brand)+"' and prod = '"+ str(Category)+"' "
    cursor.execute(query)
    lst=[]
    data = {}

    data['key'] = Brand + ' X ' + Category
    data['values'] = []
    for (u) in cursor:
        data['values'].append({'dt': u[0], 'value': u[1]})

    lst.append(data)

    return lst


def urcosme_season(pid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()

    sql = "select brand, category from gsearch.urcosme_brand_category where id = "+ str(pid)
    cursor.execute(sql)
    for (u) in cursor:
        Brand = u[0]
        Category = u[1]
    
    result={}
    #query = "SELECT r.prodname, date_format(r.pdate,'%Y-%m-%d'), r.likes FROM urcosme_prods p, urcosme_reviews r where r.prodid = '"+ str(pid)+"' limit 100 "
    query = "select m_date, percent_all, percent_5, percent_6, percent_7 from oneil.urcosme_raw_ts_season_mean where brand_name = '"+ str(Brand)+"' and prod = '"+ str(Category)+"' "    
    cursor.execute(query)
    lst=[]
    
    for (u) in cursor:
        lst.append({'dt':u[0],'mean':u[1],'five':u[2],'six':u[3],'seven':u[4] })
    return lst

def ptt_season(pid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()

    sql = "select brand, category from gsearch.sum_brand_category where id = "+ str(pid)
    cursor.execute(sql)
    for (u) in cursor:
        Brand = u[0]
        Category = u[1]
    
    result={}
    #query = "SELECT r.prodname, date_format(r.pdate,'%Y-%m-%d'), r.likes FROM urcosme_prods p, urcosme_reviews r where r.prodid = '"+ str(pid)+"' limit 100 "
    query = "select m_date, percent_all, percent_5, percent_6, percent_7 from oneil.ptt_raw_ts_season_mean where brand_name = '"+ str(Brand)+"' and prod = '"+ str(Category)+"' "
    cursor.execute(query)
    lst=[]
    
    for (u) in cursor:
        lst.append({'dt':u[0],'mean':u[1],'five':u[2],'six':u[3],'seven':u[4] })
    lst = {'data' : lst}
    return lst['data']

def trend_pix_list():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()
    result=[]
    
    sql="select brand_name,prod,sn from Serena.prodid_match;"
    cursor.execute(sql)
    for (u) in cursor:
        result.append({'category':u[1],'brand':u[0],'bid':u[2]})
    
    myobj=result
    return myobj

def ctrend(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()
    result={}
   
    query="SELECT o.brand_name,o.prod,o.pdate,o.raw_ts FROM oneil.pixnet_raw_ts o,Serena.prodid_match s where s.sn="+bid+" and s.prod=o.prod and s.brand_name=o.brand_name order by pdate desc;"
    cursor.execute(query)
    lst=[]
    
    for (u) in cursor:
        lst.append({'dt':datetime.datetime.strftime(u[2], '%Y-%m-%d'),'value':u[3]})
    return lst

def ctrend2(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]

    sql = "SELECT brand_name, prod FROM Serena.prodid_match WHERE sn = " + str(bid) 
    cursor.execute(sql)
    for (u) in cursor:
        brand = u[0]
        prod = u[1]

    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result={}
    query = "SELECT date_format(pdate,'%Y-%m-%d'),raw_ts FROM oneil.pixnet_raw_ts where brand_name = \'"+ brand + "\' and prod = \'" + prod + "\' order by pdate asc"
    cursor.execute(query)
    lst=[]
    data = {}

    data['key'] = brand + ' X ' + prod
    data['values'] = []
    for (u) in cursor:
        data['values'].append({'date': u[0], 'value': u[1]})

    lst.append(data)

    return lst
def pixnet_season(pid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()

    sql = "select brand, category from gsearch.pixnet_brand_category where id = "+ str(pid)
    cursor.execute(sql)
    for (u) in cursor:
        Brand = u[0]
        Category = u[1]
    
    result={}
    #query = "SELECT r.prodname, date_format(r.pdate,'%Y-%m-%d'), r.likes FROM urcosme_prods p, urcosme_reviews r where r.prodid = '"+ str(pid)+"' limit 100 "
    query = "select m_date, percent_all, percent_5, percent_6, percent_7 from oneil.pixnet_raw_ts_season_mean where brand_name = '"+ str(Brand)+"' and prod = '"+ str(Category)+"' "    
    cursor.execute(query)
    lst=[]
    
    for (u) in cursor:
        lst.append({'dt':u[0],'mean':u[1],'five':u[2],'six':u[3],'seven':u[4] })
    lst = {'data' : lst}
    return lst['data']

def ur_comp_product(prod):
    
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()
    lst=[]
        
    prod = prod.strip().split(',')
    for i in range(1,len(prod)) :
        sql ="select date_format(pdate,'%Y-%m-%d'), raw_ts from oneil.sum_raw_ts where brand_name = '"+prod[0]+"' and prod = '"+prod[i]+"' "
        cursor.execute(sql)
        data = {}

        data['key'] = prod[0] + ' X ' + prod[i]
        data['values'] = []
        for (u) in cursor:
            data['values'].append({'dt': u[0], 'value': u[1]})
        lst.append(data)            
            
    return lst

def ur_comp_brand(prod):
    
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()
    lst=[]
        
    prod = prod.strip().split(',')
    for i in range(1,len(prod)) :
        sql ="select date_format(pdate,'%Y-%m-%d'), raw_ts from oneil.sum_raw_ts where brand_name = '"+prod[i]+"' and prod = '"+prod[0]+"' "
        cursor.execute(sql)
        data = {}

        data['key'] = prod[i] + ' X ' + prod[0]
        data['values'] = []
        for (u) in cursor:
            data['values'].append({'dt': u[0], 'value': u[1]})
        lst.append(data)            
            
    return lst

def get_content_urcosme(prod):
    
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()
       
    prod = prod.strip().split(' X ')
    print(prod)
    query = "select prodname,content,age,skin,effects,score,date_format(pdate,'%Y-%m-%d') from gsearch.urcosme_reviews where prodname like '%"+prod[0]+"%' and content like '%"+prod[1]+"%' order by pdate desc limit 10;"    
    #query = "(select p.content from gsearch.ptt_post p where p.title like '%"+prod[0]+"%' and p.title like '%"+prod[1]+"%' order by p.date desc limit 10) UNION ALL (select r.content from gsearch.urcosme_reviews r where r.prodname like '%"+prod[0]+"%' and r.prodname like '%"+prod[1]+"%' order by r.updatedAt desc limit 10) UNION ALL (select s.content from Serena.pix_list s where s.title like '%"+prod[0]+"%' and s.title like '%"+prod[1]+"%'  limit 10)" 
    print(query)
    cursor.execute(query)
    lst=[]
    for (u) in cursor:
        lst.append({'prodname':u[0], 'content':u[1], 'age':u[2], 'skin':u[3], 'effects':u[4], 'score':u[5], 'date':u[6] })
    return lst


def get_content_urcosme_date(data):
    
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()
    
    data = data.strip().split(',')   
    prod = data[0].replace(' prediction','').replace('"','')
    start_date = data[1].replace('"','')
    end_date = (datetime.datetime.strptime(start_date, "%Y-%m-%d")+ datetime.timedelta(days = 8)).strftime("%Y-%m-%d")

    prod = prod.strip().split(' X ')
    query = "select prodname,content,age,skin,effects,score from gsearch.urcosme_reviews where prodname like '%"+prod[0]+"%' and content like '%"+prod[1]+"%'and pdate >= '"+start_date+"' and pdate < '"+end_date+"' ;"    
    print(query)

    cursor.execute(query)
    
    lst=[]
    for (u) in cursor:
        lst.append({'prodname':u[0], 'content':u[1], 'age':u[2], 'skin':u[3], 'effects':u[4], 'score':u[5] })
    return lst

def get_comp_brand_timeline(prod):
    
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()
    lst=[]
    prod = prod.replace('"','')
    prod = prod.strip().split(',')
    print(prod)
    for i in range(1,len(prod)) :
        query = "SELECT p.name, b.brand, p.pdate FROM gsearch.urcosme_prods_new p, gsearch.urcosme_brands b where p.brandid = b.pixid and p.category = '"+prod[0]+"' and b.brand like '%"+prod[i]+"%' and year(p.pdate) > '1900' ;"    
        print(query)
        cursor.execute(query)

        for (u) in cursor:
            prodname = '【' + u[1] + '】 ' + u[0]
            lst.append({'prodname':prodname, 'date':u[2] })
            
    return lst

def get_comp_product_timeline(prod):
    
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()
    lst=[]
    
    prod = prod.strip().split(',')
    print(prod)
    for i in range(1,len(prod)) :
        query = "SELECT p.name, b.brand, p.pdate FROM gsearch.urcosme_prods_new p, gsearch.urcosme_brands b where p.brandid = b.pixid and p.category = '"+prod[i]+"' and b.brand like '%"+prod[0]+"%' and year(p.pdate) > '1900' ;"    
        print(query)
        cursor.execute(query)

        for (u) in cursor:
            prodname = '【' + u[1] + '】 ' + u[0]
            lst.append({'prodname':prodname, 'date':u[2] })
            
    return lst



## test end

def get_toplist_week():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database, charset='utf8')
    cursor = cnx.cursor()
    myobj=[]
    sql = "select g.id,t.brand_name, t.prod,concat( t.total_num,' / ',t.week_avg ),g.raw_ts1,raw_ts2,g.grow_rate,concat(g.grow_rate_percent,'%') as 'lasted week growth' \
    from Serena.toplist_week t ,Serena.grow_rate_week g \
    where t.brand_name=g.brand_name and t.prod=g.prod order by g.id ;"
    #sql = "select t.* ,g.raw_ts1,raw_ts2,concat(g.grow_rate,'(',g.grow_rate_percent,'%)') as 'lasted week growth' from Serena.toplist t ,Serena.grow_rate g where t.brand_name=g.brand_name and t.prod=g.prod order by g.grow_rate_percent desc"
    cursor.execute(sql)
    for (u) in cursor:
        myobj.append({'Ranking':u[0],'brand_name':u[1],'prod':u[2],'num':u[3],'this_week':u[4],'#growing':u[6],'grow_rate':u[7]})
    return myobj

def get_toplist_month():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database, charset='utf8')
    cursor = cnx.cursor()
    myobj=[]
    sql = "select g.id,t.brand_name, t.prod, concat( t.total_num,' / ',t.month_avg ) ,g.raw_ts1,raw_ts2,g.grow_rate,concat(g.grow_rate_percent,'%') as 'lasted month growth' \
    from Serena.toplist_month t ,Serena.grow_rate_month g \
    where t.brand_name=g.brand_name and t.prod=g.prod order by g.id ;"
    #sql = "select t.* ,g.raw_ts1,raw_ts2,concat(g.grow_rate,'(',g.grow_rate_percent,'%)') as 'lasted week growth' from Serena.toplist t ,Serena.grow_rate g where t.brand_name=g.brand_name and t.prod=g.prod order by g.grow_rate_percent desc"
    cursor.execute(sql)
    for (u) in cursor:
        myobj.append({'Ranking':u[0],'brand_name':u[1],'prod':u[2],'num':u[3],'this_month':u[4],'#growing':u[6],'grow_rate':u[7]})
    return myobj
'''
def topic_count(prod):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()
   
    query="SELECT t.topics, count(t.topics) as count \
           FROM gsearch.urcosme_reviews r, gsearch.urcosme_user_topics t \
           where r.prodid = " + prod + " and r.userid = t.userid \
           group by t.topics \
           order by count desc limit 5 ;"
    cursor.execute(query)
    
    lst=[['Topic', 'Count']]
    
    for (u) in cursor:
        lst.append([u[0],u[1]])
    return lst
'''
## avon modified end
######################################


## 20180306 peihsuan modified 
#############################
def topic_count(prod):
    cnx = mysql.connector.connect(user='jared', password='iscae100',host='140.96.83.145',port=3306,database='gsearch') 
    cursor = cnx.cursor()
    '''
    query="SELECT t.topics, count(t.topics) as count \
           FROM gsearch.urcosme_reviews r, gsearch.urcosme_user_topics t \
           where r.prodid = '"+prod+"' and r.userid = t.userid \
           group by t.topics \
           order by count desc limit 3 ;"
       '''
    query="select topics,count(topics) as count from( \
           SELECT distinct r.userid,t.topics FROM gsearch.urcosme_reviews r, (\
           select userid,topics from gsearch.urcosme_user_topics\
           ) AS t where r.prodid = '"+prod+"' and r.userid = t.userid\
           ) as p group by topics order by count desc limit 3 ;"
           
    cursor.execute(query)
    
    lst=[['Topic', 'Count']]
    
    for (u) in cursor:
        lst.append([u[0],u[1]])
    return lst

## peihsuan modified end
#############################



if __name__ == '__main__':
    data_log_old()
