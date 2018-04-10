#!/usr/bin/python3
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import Markup
from py import datasetprofile
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
import esutil
import jconfig2
import mysql.connector

app = Flask(__name__, static_url_path='')
@app.route('/')
def mainform():
#    return "Hello! :)"
    return render_template('main.html')


@app.context_processor
def utility_processor():
    def execsql(sqlstmt):
        cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
        cursor = cnx.cursor()
        cursor.execute(sqlstmt)
        result=None
        for (u) in cursor:
            result=u[0]
            break
        return result
    return dict(execsql=execsql)


@app.route('/test')
def hello():
    return render_template('c.html')


@app.route('/vis')
def vis():
    r=esutil.get_result()
#    return render_template('gexf.html',nodes=r[0],relations=r[1])
    return render_template('vis.html',nodes=r[0],relations=r[1])



@app.route('/simple')
def simpleLine():
    fig=figure(title="Sensor data")
    fig.line([1,2,3,4],[2,4,6,8])
    script,div=components(fig)
    return render_template('simpleline.html',div=div,script=script)

@app.route('/trigger/<cmd>')
def trigger(cmd):
    from py import trigger
    from flask import Flask,redirect
    trigger.call(cmd)
    return redirect('/dash')






@app.route('/t2')
def t2():
    import py.jtrend
    lst=py.jtrend.get_list()
    
    return render_template('test.html',parent_dict=lst)


@app.route('/btrend')
def btrend():
#    import py.jtrend
    return render_template('brandtrend.html')


@app.route('/tsgroup')
def btrend2():
#    import py.jtrend
    return render_template('tsgroup.html')


@app.route('/gtrend/<bid>')
def gtrend(bid):
    import py.jtrend
    return jsonify( py.jtrend.gtrend(bid) )

@app.route('/gtrend2/<bid>')
def gtrend2(bid):
    import py.jtrend
    return jsonify( py.jtrend.gtrend2(bid) )

@app.route('/gtrend3/<bid>')
def gtrend3(bid):
    import py.jtrend
    return jsonify( py.jtrend.gtrend3(bid) )


@app.route('/trend_brand_list')
def trendblist():
    import py.jtrend
    return jsonify( py.jtrend.trend_brand_list() )

@app.route('/trend_brand_list2')
def trendblist2():
    import py.jtrend
    return jsonify( py.jtrend.trend_brand_list2() )




@app.route('/reviews')
def reviews():
    import py.jtrend
    lst=py.jtrend.get_list()
    comments=datasetprofile.get_comments()

    return render_template('reviews.html',comments=comments)


@app.route('/table')
def tbl():
    return render_template('table.html')

@app.route('/dash')
def dash():
    pf=datasetprofile.get_dataset_profile()
    cstatus=datasetprofile.get_crawler_status()
    comments=datasetprofile.get_comments()
    return render_template('dashboard.html',profile=pf,cstatus=cstatus,comments=comments)



@app.template_filter()
def myfunc(data):
    return Markup("<h1>H1</h1>")

@app.route('/dummy')
def dummy():
    return render_template('dummy.html',test=[{'name':'a'},{'name':'b'},{'name':'c'}])



@app.route('/myjs')
def summary():
    d = [{'a':'b','c':'d'}]
    return jsonify(d)

######################################
## eva modified
@app.route('/ptt')
def ptt():
    import py.jtrend
    return render_template('pttchart.html')

@app.route('/ptt_trend/<bid>')
def ptt_trend(bid):
    import py.jtrend
    return jsonify( py.jtrend.ptt_trend(bid) )

@app.route('/ptt_trend2/<bid>')
def ptt_trend2(bid):
    import py.jtrend
    return jsonify( py.jtrend.ptt_trend2(bid) )

@app.route('/ptt_trend3/<bid>')
def ptt_trend3(bid):
    import py.jtrend
    return jsonify( py.jtrend.ptt_trend3(bid) )

@app.route('/ptt_brand_list')
def pttblist():
    import py.jtrend
    return jsonify( py.jtrend.ptt_brand_list() )

@app.route('/ptt_season/<bid>')
def ptt_season(bid):
    import py.jtrend
    return jsonify( py.jtrend.ptt_season(bid) )

@app.route('/all')
def all():
    import py.jtrend
    return render_template('allchart.html')

@app.route('/all_trend/<bid>')
def all_trend(bid):
    import py.jtrend
    return jsonify( py.jtrend.all_trend(bid) )

@app.route('/all_trend2/<bid>')
def all_trend2(bid):
    import py.jtrend
    return jsonify( py.jtrend.all_trend2(bid) )

@app.route('/all_brand_list')
def allblist():
    import py.jtrend
    return jsonify( py.jtrend.all_brand_list() )

@app.route('/bptrend')
def bptrend():
    import py.jtrend
    return render_template('bptrendchart.html')

@app.route('/bp_trend/<bid>')
def bp_trend(bid):
    import py.jtrend
    return jsonify( py.jtrend.bp_trend(bid) )

@app.route('/bp_trend2/<bid>')
def bp_trend2(bid):
    import py.jtrend
    return jsonify( py.jtrend.bp_trend2(bid) )

@app.route('/bp_trend3/<bid>')
def bp_trend3(bid):
    import py.jtrend
    return jsonify( py.jtrend.bp_trend3(bid) )

@app.route('/bp_brand_list')
def bplist():
    import py.jtrend
    return jsonify( py.jtrend.bp_brand_list() )

@app.route('/pred_comp')
def pred_comp():
    import py.jtrend
    return render_template('pred_deom.html')

@app.route('/pred')
def pred():
    import py.jtrend
    return render_template('predchart.html')

@app.route('/pred_trend/<bid>')
def pred_trend(bid):
    import py.jtrend
    return jsonify( py.jtrend.pred_trend(bid) )

@app.route('/pred_calendar/<bid>')
def pred_calendar(bid):
    import py.jtrend
    return jsonify( py.jtrend.pred_calendar(bid) )

@app.route('/pred_leading/<bid>')
def pred_leading(bid):
    import py.jtrend
    return jsonify( py.jtrend.pred_leading(bid) )

@app.route('/pred_lead_comp/<bid>')
def pred_lead_comp(bid):
    import py.jtrend
    return jsonify( py.jtrend.pred_lead_comp(bid))

@app.route('/pred_brand_list')
def predblist():
    import py.jtrend
    return jsonify( py.jtrend.pred_brand_list() )

@app.route('/comp')
def comp():
    lists=datasetprofile.get_brand_prod_list() 
    return render_template('comp_prod.html',lists = lists)

@app.route('/comp_trend/<comp_list>')
def comp_trend(comp_list):
    import py.jtrend
    return jsonify( py.jtrend.comp_trend(comp_list) )

@app.route('/ur_comp_brand2/<prod>')
def ur_comp_brand2(prod):
    import py.jtrend
    return jsonify( py.jtrend.ur_comp_brand2(prod))

@app.route('/ur_comp_product2/<prod>')
def ur_comp_product2(prod):
    import py.jtrend
    return jsonify( py.jtrend.ur_comp_product2(prod))

@app.route('/alert_table')
def alert_table():
    brand = datasetprofile.get_brand_sum_raw_ts()
    product = datasetprofile.get_product_sum_raw_ts()
    return render_template('parser.html', brand = brand, product = product)

@app.route('/get_alert_table/<table_list>')
def get_alert_table(table_list):
    import py.jtrend
    return jsonify( py.jtrend.get_alert_table(table_list))

@app.route('/pred_alert/<bid>')
def pred_alert(bid):
    import py.jtrend
    return render_template('predalert.html',bid = bid)

@app.route('/user_data')
def user_data():
    import py.jtrend
    prodid = py.jtrend.prodid_list()
    return render_template('users_data.html', prodid = prodid)

@app.route('/user_age/<prodid>')
def user_age(prodid):
    import py.jtrend
    return jsonify( py.jtrend.user_age(prodid))

@app.route('/user_skin/<prodid>')
def user_skin(prodid):
    import py.jtrend
    return jsonify( py.jtrend.user_skin(prodid))

@app.route('/google')
def google():
    import py.jtrend
    prods = py.jtrend.google_list()
    return render_template('google.html', prods = prods)

@app.route('/google_trend/<prod>')
def google_trend(prod):
    import py.jtrend
    return jsonify( py.jtrend.google_trend(prod) )

@app.route('/pred_element')
def pred_element():
    import py.jtrend
    element = py.jtrend.element_list()
    return render_template('pred_element.html', element = element)

@app.route('/pred_element_st/<element>')
def pred_element_st(element):
    import py.jtrend
    return jsonify( py.jtrend.pred_element(element) )

@app.route('/pred_element_leading/<element>')
def pred_element_leading(element):
    import py.jtrend
    return jsonify( py.jtrend.element_leading(element) )

@app.route('/element_lead_comp/<elem>')
def element_lead_comp(elem):
    import py.jtrend
    return jsonify( py.jtrend.element_lead_comp(elem))

@app.route('/report')
def report():
    import py.jtrend
    return render_template('report.html')

@app.route('/pred_element_report/<element>')
def pred_element_report(element):
    import py.jtrend
    return jsonify( py.jtrend.pred_element_report(element) )

@app.route('/pred_google_report/<element>')
def pred_google_report(element):
    import py.jtrend
    return jsonify( py.jtrend.pred_google_report(element) )

@app.route('/data_log')
def data_log():
    import py.jtrend
    return render_template('data_log.html')

@app.route('/data_log_old')
def data_log_old():
    import py.jtrend
    return jsonify( py.jtrend.data_log_old() )

## eva modified end
######################################

######################################
## avon modified
@app.route('/index.html')
def idx():
    from flask import Flask,redirect
    return redirect('/toplist')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/urcosme')
def urcosme_prod():
    return render_template('urcosme_prod.html')

@app.route('/urcosme_brand_list')
def urcosme_brand_list():
    import py.jtrend
    return jsonify( py.jtrend.urcosme_brand_list() )

@app.route('/urcosme_trend/<bid>')
def urcosme_trend(bid):
    import py.jtrend
    return jsonify( py.jtrend.urcosme_trend(bid) )

@app.route('/urcosme_trend_2/<bid>')
def urcosme_trend_2(bid):
    import py.jtrend
    return jsonify( py.jtrend.urcosme_trend_2(bid) )

@app.route('/urcosme_season/<bid>')
def urcosme_season(bid):
    import py.jtrend
    return jsonify( py.jtrend.urcosme_season(bid) )

@app.route('/pixnet_trends')
def pixnet_trends():    
    return render_template('pixnet_trends.html')

@app.route('/trend_pix_list')
def pixlist():
    import py.jtrend
    return jsonify( py.jtrend.trend_pix_list() )

@app.route('/ctrend/<bid>')
def ctrend(bid):
    import py.jtrend
    return jsonify( py.jtrend.ctrend(bid) )

@app.route('/ctrend2/<bid>')
def ctrend2(bid):
    import py.jtrend
    return jsonify( py.jtrend.ctrend2(bid) )

@app.route('/pixnet_season/<bid>')
def pixnet_season(bid):
    import py.jtrend
    return jsonify( py.jtrend.pixnet_season(bid) )

@app.route('/comp_product')
def comp_product():
    brand = datasetprofile.get_brand_sum_raw_ts()
    product = datasetprofile.get_product_sum_raw_ts()
    comments=datasetprofile.get_reviews()

    return render_template('ur_comp_product.html', brand = brand, product = product,comments=comments)


@app.route('/ur_comp_product/<prod>')
def ur_comp_product(prod):
    import py.jtrend
    return jsonify( py.jtrend.ur_comp_product(prod))

@app.route('/comp_brand')
def comp_brand():
    brand = datasetprofile.get_brand_sum_raw_ts()
    product = datasetprofile.get_product_sum_raw_ts()
    return render_template('ur_comp_brand.html', brand = brand, product = product)

@app.route('/ur_comp_brand/<prod>')
def ur_comp_brand(prod):
    import py.jtrend
    return jsonify( py.jtrend.ur_comp_brand(prod))

@app.route('/get_content_urcosme/<prod>')
def get_content_urcosme(prod):
    import py.jtrend
    return jsonify( py.jtrend.get_content_urcosme(prod))

@app.route('/get_content_urcosme_date/<prod>')
def get_content_urcosme_date(prod):
    import py.jtrend
    return jsonify( py.jtrend.get_content_urcosme_date(prod))

@app.route('/get_comp_brand_timeline/<prod>')
def get_comp_brand_timeline(prod):
    import py.jtrend
    return jsonify( py.jtrend.get_comp_brand_timeline(prod))

@app.route('/get_comp_product_timeline/<prod>')
def get_comp_product_timeline(prod):
    import py.jtrend
    return jsonify( py.jtrend.get_comp_product_timeline(prod))

@app.route('/toplist')
def sort():
    import py.jtrend
    comments = py.jtrend.get_toplist_week()
    comments2 = py.jtrend.get_toplist_month()
    return render_template('tab_tables.html',comments=comments,comments2=comments2)

@app.route('/topic_count/<prod>')
def topic_count(prod):
    import py.jtrend
    return jsonify( py.jtrend.topic_count(prod))

## avon modified end
######################################


###20180306 peihsuan modified
#########################################
@app.route('/profile')
def bubble():
    import py.jtrend
    #comments = py.jtrend.get_toplist_week()
    #comments2 = py.jtrend.get_toplist_month()
    #return render_template('bubblepop.html',comments=comments,comments2=comments2)
    return render_template('profile.html')

@app.route('/prod_1028')#data
def prod1028():
    from py import datasetprofile
    return jsonify( datasetprofile.get_prod_1028())



if __name__ == '__main__':
    app.run( 
        host="0.0.0.0",
        port=int("1234")
    )
