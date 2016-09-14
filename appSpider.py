# -*- coding: UTF-8 -*-
# Created on 2016-08-01 
# Project: app download

from bs4 import BeautifulSoup
import requests
import urllib
import sys  
reload(sys)  
sys.setdefaultencoding('utf8') 
def yingyonghui_crawler(name):
	url = 'http://www.appchina.com/sou/' + name
	web_data = requests.get(url)
	soup = BeautifulSoup(web_data.text, 'lxml')
	title = soup.select(' ul > li > div.app-info > h1 > a')[0].get_text()
	times = soup.select(' ul > li > div.app-info > span.download-count')[0].get_text()[:-2]
	print u'在应用汇上，' + title + '下载量为：' + times

def zhushou_crawler(name):
	url = 'http://zhushou.360.cn/search/index/?kw=' + name
	web_data = requests.get(url)
	soup = BeautifulSoup(web_data.text, 'lxml')
	title = soup.select(' body > div.warp > div.main > div > ul > li > dl > dd > h3 > a > span')[0].get_text()
	times = soup.select(' body > div.warp > div.main > div > ul > li > div > div.sdlft > p.downNum')[0].get_text()[:-3]
	print '在360手机助手上，' + title + '下载量为：' + times

def anzhuoshichang_crawler(name):
	url = 'http://apk.hiapk.com/search?key=' + name
	web_data = requests.get(url)
	soup = BeautifulSoup(web_data.text, 'lxml')
	title = soup.select('  div.soft_list_box > ul > li > div > dl > dt > span.list_title.font12 > a')[0].get_text()
	times = soup.select(' div.soft_list_box > ul > li > div > div.right > div.s_dnum')[0].get_text().replace(' ','').replace('\n', '')[:-2]
	print '在安卓市场上，' + title + '下载量为：' + times 

def kuan_crawler(name):
	url = 'http://www.coolapk.com/search?q=' + name
	web_data = requests.get(url)
	soup = BeautifulSoup(web_data.text, 'lxml')
	title = soup.select('  div > h4 > a')[0].get_text()
	times = soup.select('  div > div.media-info > span.hidden-xs')[0].get_text()
	comma_location = times.find('，')
	times_tidy = times[int(comma_location) + 1:-5]
	print('在酷安网上，' + title + '下载量为：' + times_tidy)

def baidu_crawler(name):
	url='http://shouji.baidu.com/s?wd=' +name
	web_data=requests.get(url)
	soup=BeautifulSoup(web_data.text,'lxml')
	title=soup.select(' div.yui3-g > div > div > div > div.app > div.info > div.top > a')[0].get_text().strip()
	times=soup.select(' div.yui3-g > div > div > div > div.app > div.info > div.middle > span.down-num')[0].get_text().strip()[0:4]
	print '在百度手机助手上，' +title +'下载量为' +times

def huawei_crawler(name):
	name=urllib.quote(name)
	name=urllib.quote(name)
	url='http://appstore.huawei.com/search/' +name
	web_data=requests.get(url)
	soup=BeautifulSoup(web_data.text,'lxml')
	title=soup.select('  div.lay-main > div.lay-left.corner > div.unit.nofloat > div.unit-main > div.list-game-app.dotline-btn.nofloat > div.game-info.whole > h4 > a ')[0].get_text()
	times=soup.select('  div.lay-main > div.lay-left.corner > div.unit.nofloat > div.unit-main > div.list-game-app.dotline-btn.nofloat > div.game-info.whole > div.app-btn > span  ')[0].get_text()[3:]
	print '在华为应用市场上，' +title +'下载量为' +times

def wandoujia_crawler(name):
	url='http://www.wandoujia.com/search?key=' +name
	web_data=requests.get(url)
	soup=BeautifulSoup(web_data.text,'lxml')
	title=soup.select(' #j-search-list > li > div.app-desc > h2 > a > em')[0].get_text().strip()
	times=soup.select(' #j-search-list > li > div.app-desc > div.meta > span.install-count')[0].get_text()[:5]
	print '在豌豆荚上，' +title +'下载量为' +times
	
def anzhuo_crawler(name):
	url='http://apk.hiapk.com/search?key='+ name + '&pid=0' 
	web_data=requests.get(url)
	soup=BeautifulSoup(web_data.text,'lxml')
	title=soup.select(' #SoftSearchAllList > div.soft_list_box > ul > li > div > dl > dt > span.list_title.font12 > a')[0].get_text().strip()
	times=soup.select(' #SoftSearchAllList > div.soft_list_box > ul > li > div > div.right > div.s_dnum')[0].get_text().strip()[:6]
	print '在安卓市场上，' +title +'下载量为' +times
	
def anzhi_crawler(name):
	url='http://www.anzhi.com/search.php?keyword='+ name 
	web_data=requests.get(url)
	soup=BeautifulSoup(web_data.text,'lxml')
	title=soup.select(' body > div.content > div.content_left > div.app_list.border_three > ul > li > div.app_info > span > a')[0].get_text().strip()
	times=soup.select(' body > div.content > div.content_left > div.app_list.border_three > ul > li > div.app_info > div > span.app_downnum.l')[0].get_text()[3:]
	print '在安智市场上，' +title +'下载量为' +times

def pp_crawler(name):
	url='http://www.25pp.com/ios/search/app/0/'+ name + '/' 
	web_data=requests.get(url)
	soup=BeautifulSoup(web_data.text,'lxml')
	title=soup.select(' body > div.wrap.clearfix.mb30 > div > div.block-tabs > ul > li > div > a')[0].get_text().strip()[:2]
	times=soup.select(' body > div.wrap.clearfix.mb30 > div > div.block-tabs > ul > li > div > p')[0].get_text().strip()[:5]
	print '在PP助手上，' +title +'下载量为' +times

def yingyongbao_crawler(name):
	name=urllib.quote(name)
	url='http://android.myapp.com/myapp/search.htm?kw='+ name 
	web_data=requests.get(url)
	soup=BeautifulSoup(web_data.text,'lxml')
	# title=soup.select('J_SearchDefaultListBox > li > div.search-boutique-data > div.data-box > div.name-line > div.name > a')
	# times=soup.select('   li > div > div > div.down-line')
	# print '在应用宝上，' +title +'下载量为' +times
	# title=soup.find_all('div',class_='down-line')
	print title
	#
if __name__=='__main__':
	name = '汽车之家'
	# yingyonghui_crawler(name)
	# zhushou_crawler(name)
	# anzhuoshichang_crawler(name)
	# kuan_crawler(name)
	# baidu_crawler(name)
	# huawei_crawler(name)
	# wandoujia_crawler(name)
	# anzhuo_crawler(name)
	# anzhi_crawler(name)
	# pp_crawler(name)
	yingyongbao_crawler(name)
	
