import elasticsearch
import jconfig2
import mysql.connector

globalpid=0
cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 

cursor = cnx.cursor()

def get_result():
    global cursor
    #sql = "SELECT c.id,c.title,c2.id,c2.title,sim.score FROM pix_docsim sim,pix_content c,pix_content c2  where sim.destid=c2.id and sim.srcid=c.id and sim.score > 10 order by sim.srcid,sim.score desc limit 20"
#    sql = "SELECT c.id,c2.id,sim.score,c.title,c2.title FROM pix_docsim sim,pix_content c,pix_content c2  where sim.destid=c2.id and sim.srcid=c.id order by sim.score desc limit 300"
#    sql = "SELECT c.id,c2.id,sim.score,c.title,c2.title FROM pix_docsim sim,pix_content c,pix_content c2  where sim.destid=c2.id and sim.srcid=c.id order by sim.score desc"
    sql="SELECT c.id,c2.id,sim.score,c.title,c2.title FROM pix_docsim sim,pix_content c,pix_content c2, (select srcid from pix_docsim order by score desc limit 400,100) sel  where c.id=sel.srcid and  sim.destid=c2.id and sim.srcid=c.id "
    nodes=[]
    relations=[]
    nodehash={}
    cursor.execute(sql)
    #    maxid=0
    for (u) in cursor:
        nodehash[u[0]]=u[3]
        nodehash[u[1]]=u[4]
        relations.append({'from': u[0], 'to': u[1]})
    for k,v in nodehash.items():
        nodes.append({'id':k,'label':v})
    return (nodes,relations)
#        globalpid+=1
#    get_likes(u[0])

#print(get_result())

