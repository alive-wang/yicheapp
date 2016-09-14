# -*- coding: UTF-8 -*-
#把url解码分割后并存入字典,并插入MySQL数据库
# COALESCE


from datetime import datetime,timedelta
import urllib.parse
import pymysql
import json
import logging
import os


# 解析json存入文件
def json2_txt(dir1,dir2):
	os.chdir('E:\log')
	with open(dir1, "r",encoding='utf-8') as file: 
		start_date=datetime(2016,5,1)
		while True:
			line=file.readline()
			if line:				
				data=json.loads(line)
				with open(dir2, "a+",encoding='utf-8') as file2: 
					for item in  data['CheYouDetails']:
						file2.write(','.join(map(lambda x:str(x),[start_date.strftime('%Y-%m-%d'),item['TopicMode'],item['DailyTopicAdd'],item['DailyReplyAdd'],item['DailyLikeCount'],item['AppDailyTopicAdd'],\
						item['DailyGoodTopicCount'],item['DailyTopicUv']])))
						file2.write('\n')
					file2.write(','.join(map(lambda x:str(x),[start_date.strftime('%Y-%m-%d'),data['DailyUserCount'],data['DailyTopicAdd'],data['DailyReplyAdd'],data['DailyLikeCount'],data['DailyFollowCount'],\
					data['AppDailyTopicAdd'],data['DailyGoodTopicCount'],data['DailyTopicUv']])))
					file2.write('\n')
				start_date=start_date+timedelta(days=1)
			else:
				break
# 将&=日志转换成字典类型
def string_split(string):
	dict={}
	list=[]
	for key_value in string.split('&'):
		list=key_value.split('=')
		if len(list)<2:
			dict[list[0]]=''
		else:
			dict[list[0]]=list[1]
	return dict

# 将文件中的数据解析后存入数据库	
def data_save(dir,sql1,sql2):
	now=datetime.now()
	dt=now-timedelta(days=3)
	dt=dt.strftime('%Y-%m-%d')	
	file = open(dir, "r")
	db_params = {'host':'localhost', 'user':'root', 'passwd':'wangbin', 'db':'yiche', 'charset':'utf8'}
	conn = pymysql.connect(**db_params)
	cursor = conn.cursor()
	cursor.execute(sql1)
	conn.commit()
	while True:
		line=file.readline()
		if line:
			string=urllib.parse.unquote(line)
			data=string_split(string)
			if  data.get('deviceId')  :
				list=[]
				list.extend([data["deviceId"],dt])
				cursor.execute(sql2,list)
				conn.commit()
			elif data.get('deviceid'):
				list=[]
				list.extend([data["deviceid"],dt])
				cursor.execute(sql2,list)
				conn.commit()
		else:
			break
			
	cursor.close()
	conn.close()


# 将url编码的文件解码后存入文件
def urld2_txt(dir,dir2):
	with open(dir, "r",encoding='utf-8') as file:
		while True:
			line=file.readline()
			if line.strip('\n') =='_c0':
				continue
			if line.strip('\n') =='':
				break
			list=urllib.parse.unquote(line)
			list=urllib.parse.unquote(list)
			with open(dir2, "a+",encoding='utf-8') as file2:
				file2.write(list)
				file2.write('\n')

# 将清洗后的日志存入数据库
def clear2_db(dir,sql):
	with open(dir, "r",encoding='utf-8') as file:
		db_params = {'host':'localhost', 'user':'root', 'passwd':'wangbin', 'db':'yiche', 'charset':'utf8'}
		conn = pymysql.connect(**db_params)
		cursor = conn.cursor()			
		while True:
			line=file.readline()
			if line.strip('\n') =='_c0':
				continue
			if line.strip('\n') =='':
				break
			list=urllib.parse.unquote(line)
			list=list.replace('+',' ')
			js=json.loads(list)
			print(js)
			for itmes in js:
				if itmes.get('bn') and itmes.get('acty') :
					ls=[]
					ls.extend([itmes['dvid'],itmes['tm'],str(itmes['bn']),str(itmes['acty']),itmes['os'],itmes['uid'],itmes['tm'][0:10],str(itmes.setdefault('dk',{'id':''}).get('id',''))])
					cursor.execute(sql,ls)
					conn.commit()
		cursor.close()
		conn.close()

# 将清洗后的日志存入文件
def clear2_txt(dir,dir2,dir3):
	with open(dir, "r",encoding='utf-8') as file:
		while True:
			line=file.readline()
			if line.strip('\n') =='_c0':
				continue
			if line.strip('\n') =='':
				break
			list=urllib.parse.unquote(line)
			list=urllib.parse.unquote(list)
			list=list.replace('+',' ')
			list=list.replace('\\','')
			list=list.replace('\"{','{')
			list=list.replace('}\"','}')
			try:
				js=json.loads(list)
			except ValueError as e:
				logging.exception(e)
				print('list:',list)
				with open("E:/log/log.txt","a+",encoding='utf-8') as ff:
					ff.write(list)
			for itmes in js:
				if itmes.get('cha')  :
					ls=[itmes['dvid'],itmes['tm'],itmes['av'],itmes['cyid'],itmes['cha'],itmes['os'],itmes['uid'],itmes.get('pn','NULL'),itmes['fac'],str(itmes.get('na','NULL')),itmes['tm'][0:10]]
					data_start='\t'.join(ls)
					with open(dir2, "a+",encoding='utf-8') as file2:
						file2.write(data_start)
						file2.write('\n')
				elif itmes.get('bn') and itmes.get('acty') :
					ls=[itmes['dvid'],itmes['tm'],str(itmes['bn']),str(itmes['acty']),itmes['os'],itmes['uid'],str(itmes.setdefault('dk',{'id':''}).get('id','')),itmes['tm'][0:10]]
					data_act='\t'.join(ls)
					with open(dir3, "a+",encoding='utf-8') as file3:
						file3.write(data_act)
						file3.write('\n')

if  __name__=='__main__':
	dir1='cheyou_detail.txt'
	dir2='cheyou_data.txt'
	json2_txt(dir1,dir2)
	dir3='E:/log/decodev2.txt'
	# dt=dir[16:24]
	# dir2="E:/log/user_start_" + dt + ".txt"
	# dir3="E:/log/user_act_"   + dt + ".txt"
	# sql='''insert  into yiche.day_user_behavior (deviceid,time,business,acty,os,uid,dt,objectid) values(%s,%s,%s,%s,%s,%s,%s)'''	
	# clear2_db(dir,sql)
	# clear2_txt(dir,dir2,dir3)
	# dir ="E:/log/query_result.csv"
	# dir2="E:/log/decodev2.txt"
	# urld2_txt(dir,dir2)	
	# dir="E:/log/query_result3.csv"
	# sql='''delete from yiche.deviceid where dt='%s' '''%dt
	# sql1='''delete from yiche.deviceid where dt='%(dt)s' '''%{'dt':dt}
	# sql2='''insert  into yiche.deviceid (deviceId,dt) values(%s,%s)'''
	# data_save(dir,sql1,sql2)
	
