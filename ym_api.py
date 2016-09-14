# -*- coding: UTF-8 -*-
# Created on 2016-07-29 
# Project: yiche.baojia&yiche.mm
import re
import urllib
import urllib2
import os
import json
from datetime import datetime,timedelta
import pymysql
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8') 

# auth_token='Orc3WNOtTXC9B3Z3W6xA'
# yiche_iphone = '4d33bb443ea7a32413072aaa'
# yiche_wp7    = '4f86496c52701575f4000001'
# yiche_android= '50b5c2085270153e9d00001e'
# yiche_ipad   = '4d38e6db3ea7a365a8029e2a'
# yiche_win8   = '512ae268527015465700001b'
# yiche_hd     = '52c0e3bd56240b11410d18aa'

def post_token():
	values = {"email":"wangbin10@yiche.com","password":"wangbin2188"}
	data = urllib.urlencode(values) 
	url = "http://api.umeng.com/authorize"
	request = urllib2.Request(url,data)
	response = urllib2.urlopen(request)
	js=json.loads(response.read())
	# with open('E:\log\ymtoken.txt','a+') as ff:
		# ff.write(js['auth_token'])
	return js['auth_token']

def get_apps():
	umengUrl='http://api.umeng.com'
	eventurl='/apps'
	values={}
	values['per_page'] = 10
	values['page']=1
	values['q']="易车"
	values['auth_token']=post_token()
	data = urllib.urlencode(values) 
	url=umengUrl + eventurl
	geturl = url + "?"+data
	request = urllib2.Request(geturl)
	response = urllib2.urlopen(request)
	js=json.loads(response.read())
	for item in js:
		print item['name'],item['appkey']

def get_group():
	umengUrl='http://api.umeng.com'
	eventurl='/events/group_list'
	values={}
	values['per_page'] = 2000
	values['page']=1
	values['appkey'] = "4d33bb443ea7a32413072aaa"
	values['start_date']="2016-09-01"
	values['end_date']="2016-09-01"
	values['period_type']="daily"
	values['auth_token']=post_token()
	data = urllib.urlencode(values) 
	url=umengUrl + eventurl
	geturl = url + "?"+data
	request = urllib2.Request(geturl)
	response = urllib2.urlopen(request)
	js=json.loads(response.read())
	with open('E:\log\ymtoken.txt','a+') as ff:
		for item in js:
			ff.write(item['display_name'])
			ff.write(':')
			ff.write(item['name'])
			ff.write(':')
			ff.write(item['group_id'])
			ff.write('\n')

def get_base_data(appkey,date,auth_token='Orc3WNOtTXC9B3Z3W6xA'):
	umengUrl='http://api.umeng.com'
	eventurl='/base_data'
	values={}
	values['appkey'] = appkey
	values['date']=date
	values['auth_token']=auth_token
	data = urllib.urlencode(values) 
	url=umengUrl + eventurl
	geturl = url + "?"+data
	request = urllib2.Request(geturl)
	response = urllib2.urlopen(request)
	js=json.loads(response.read())
	return js

def get_retain_data(appkey,start_date,end_date,auth_token='Orc3WNOtTXC9B3Z3W6xA'):
	umengUrl='http://api.umeng.com'
	eventurl='/retentions'
	values={}
	values['appkey'] = appkey
	values['start_date']=start_date
	values['end_date']=end_date
	values['period_type']="daily"
	values['auth_token']=auth_token
	data = urllib.urlencode(values) 
	url=umengUrl + eventurl
	geturl = url + "?"+data
	request = urllib2.Request(geturl)
	response = urllib2.urlopen(request)
	js=json.loads(response.read())
	return js

def get_group_data(appkey,start_date,end_date,group_id):
	umengUrl='http://api.umeng.com'
	eventurl='/events/daily_data'
	values={}
	values['appkey'] = appkey
	values['start_date']=start_date
	values['end_date']=end_date
	values['period_type']="daily"
	values['group_id']=group_id
	values['type']="count"
	values['auth_token']=post_token()
	data = urllib.urlencode(values) 
	url=umengUrl + eventurl
	geturl = url + "?"+data
	request = urllib2.Request(geturl)
	response = urllib2.urlopen(request)
	js=json.loads(response.read())
	return  js['data']['all'][0]


# 把插入数据库的代码单独写出来是为了阅读方便，但实际上每次插入都提交，会影响效率
def data_mysql(sql,ls):
	db_params = {'host':'localhost', 'user':'root', 'passwd':'wangbin', 'db':'chart', 'charset':'utf8'}
	conn = pymysql.connect(**db_params)
	cursor = conn.cursor()
	cursor.execute(sql,ls)
	conn.commit()
	cursor.close()
	conn.close()

def insert_active(start_date,end_date):
	sql='''insert into chart.push_appactive(adr_active,ios_active,week,month,date) values(%s,%s,%s,%s,%s) '''
	appkey={'adr':'50b5c2085270153e9d00001e','ios':'4d33bb443ea7a32413072aaa','ipad':'4d38e6db3ea7a365a8029e2a'}
	start_date=start_date
	while start_date<end_date:
		week_start=start_date-timedelta(start_date.weekday())
		week_end=week_start+timedelta(days=6)
		week=week_start.strftime('%m/%d')+'~'+week_end.strftime('%m/%d')
		adr_js=get_base_data(appkey['adr'],start_date.strftime('%Y-%m-%d'))
		ios_js=get_base_data(appkey['ios'],start_date.strftime('%Y-%m-%d'))		
		ls= [adr_js['active_users'],ios_js['active_users'],week,start_date.strftime('%Y/%m'),adr_js['date']]
		cursor.execute(sql,ls)
		print start_date
		start_date=start_date+timedelta(days=1)	

def insert_newuser(start_date,end_date):
	sql='''insert into chart.push_appadd(adr_add,ios_add,week,month,date) values(%s,%s,%s,%s,%s) '''
	appkey={'adr':'50b5c2085270153e9d00001e','ios':'4d33bb443ea7a32413072aaa','ipad':'4d38e6db3ea7a365a8029e2a'}
	start_date=start_date
	while start_date<end_date:
		week_start=start_date-timedelta(start_date.weekday())
		week_end=week_start+timedelta(days=6)
		week=week_start.strftime('%m/%d')+'~'+week_end.strftime('%m/%d')
		adr_js=get_base_data(appkey['adr'],start_date.strftime('%Y-%m-%d'))
		ios_js=get_base_data(appkey['ios'],start_date.strftime('%Y-%m-%d'))		
		ls= [adr_js['new_users'],ios_js['new_users'],week,start_date.strftime('%Y/%m'),adr_js['date']]
		cursor.execute(sql,ls)
		print start_date
		start_date=start_date+timedelta(days=1)		

def insert_starts(start_date,end_date):
	sql='''insert into chart.push_appstarts(adr_starts,ios_starts,week,month,date) values(%s,%s,%s,%s,%s) '''
	appkey={'adr':'50b5c2085270153e9d00001e','ios':'4d33bb443ea7a32413072aaa','ipad':'4d38e6db3ea7a365a8029e2a'}
	start_date=start_date
	while start_date<end_date:
		week_start=start_date-timedelta(start_date.weekday())
		week_end=week_start+timedelta(days=6)
		week=week_start.strftime('%m/%d')+'~'+week_end.strftime('%m/%d')
		adr_js=get_base_data(appkey['adr'],start_date.strftime('%Y-%m-%d'))
		ios_js=get_base_data(appkey['ios'],start_date.strftime('%Y-%m-%d'))		
		ls= [adr_js['launches'],ios_js['launches'],week,start_date.strftime('%Y/%m'),adr_js['date']]
		cursor.execute(sql,ls)
		print start_date
		start_date=start_date+timedelta(days=1)

def insert_headlines(start_date,end_date):
	appkey={'adr':'50b5c2085270153e9d00001e','ios':'4d33bb443ea7a32413072aaa','ipad':'4d38e6db3ea7a365a8029e2a'}
	adr_group_id =['54b77b41fd98c56444000650','56ea7893e0f55a8453002a0d','54d1bc6afd98c566ef0009bb','56ea7893e0f55a8453002a0e','56ea7893e0f55a8453002a0c']
	ios_group_id =['54b39159fd98c5ac00000914','56ea783be0f55abe7a001edb','54d1ba07fd98c594980010eb','56ea783be0f55abe7a001edc','56ea783be0f55abe7a001eda']
	mid_data=[]
	for item in adr_group_id:
		mid_data.append(get_group_data(appkey['adr'],start_date,end_date,item))
	for item in ios_group_id:
		mid_data.append(get_group_data(appkey['ios'],start_date,end_date,item))
	print start_date,sum(mid_data)

def insert_appretain(start_date,end_date):
	sql='''insert into chart.push_appretain(adr_retain,ios_retain,date) values(%s,%s,%s) '''
	adr_data=get_retain_data(appkey['adr'],start_date.strftime('%Y-%m-%d'),end_date.strftime('%Y-%m-%d'))
	ios_data=get_retain_data(appkey['ios'],start_date.strftime('%Y-%m-%d'),end_date.strftime('%Y-%m-%d'))
	date_data=[]
	mid_data1=[]
	mid_data2=[]
	for item in adr_data:
		date_data.append(item['install_period'])
		mid_data1.append(item['retention_rate'][0])
	for item in ios_data:
		mid_data2.append(item['retention_rate'][0])
	sql_data= map(list,zip(mid_data1,mid_data2,date_data))
	for item in sql_data:
		cursor.execute(sql,item)

def get_statics(start_date,end_date,group_id):
	umengUrl='http://appcms.op.bitauto.com/Elasticsearch/YcAppStatis'
	values={}
	values['key'] = 'ij8bbv1C3gRE0H6Ria3AyQ=='
	values['size']=365
	values['start']=start_date.strftime('%Y-%m-%d')
	values['end']=end_date.strftime('%Y-%m-%d')
	values['queryText']='statsName:\"'+group_id+'\"'
	data = urllib.urlencode(values) 
	url=umengUrl 
	geturl = url + "?"+data
	request = urllib2.Request(geturl)
	response = urllib2.urlopen(request)
	js=json.loads(response.read())
	return js['data']
	
def insert_appvideo(start_date,end_date):
	sql='''insert into chart.push_appvideo(adr_video,ios_video,week,month,date) values(%s,%s,%s,%s,%s) '''
	adr_group_id='AndroidVideoPlayCount'
	ios_group_id='IOSVideoPlayCount'
	adr_data= get_statics(start_date,end_date,adr_group_id)
	ios_data= get_statics(start_date,end_date,ios_group_id)
	date_data=[]
	mid_data1=[]
	mid_data2=[]
	for item in adr_data:
		date_data.append(item['statsDate'][:10])
		mid_data1.append(item['statsValue'])
	for item in ios_data:
		mid_data2.append(item['statsValue'])
	start_date=start_date
	ls_week=[]
	ls_month=[]
	while start_date<end_date:
		week_start=start_date-timedelta(start_date.weekday())
		week_end=week_start+timedelta(days=6)
		week=week_start.strftime('%m/%d')+'~'+week_end.strftime('%m/%d')	
		ls_week.append(week)
		ls_month.append(start_date.strftime('%Y/%m'))
		start_date=start_date+timedelta(days=1)
	sql_data= map(list,zip(mid_data1,mid_data2,ls_week,ls_month,date_data))
	for item in sql_data:
		cursor.execute(sql,item)
	
if  __name__=='__main__':
	appkey={'adr':'50b5c2085270153e9d00001e','ios':'4d33bb443ea7a32413072aaa','ipad':'4d38e6db3ea7a365a8029e2a'}
	db_params = {'host':'localhost', 'user':'root', 'passwd':'wangbin', 'db':'chart', 'charset':'utf8'}
	conn = pymysql.connect(**db_params)
	cursor = conn.cursor()
	start_date=datetime(2016,9,13)
	end_date=datetime(2016,9,14)
	insert_active(start_date,end_date)
	insert_newuser(start_date,end_date)
	insert_starts(start_date,end_date)
	# insert_appretain(start_date,end_date)	
	# insert_appvideo(start_date,end_date)
	# group_id='AdminDailyStats'
	# data=get_statics(start_date,end_date,group_id)

	conn.commit()
	cursor.close()
	conn.close()






