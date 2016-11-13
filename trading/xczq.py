# coding: utf-8
import requests
import random
import time
import Queue
import threading

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'

class xczq():
	def __init__(self,account,password):
		self.sess=requests.Session()
		self.account=account
		self.password=password
		headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding':'gzip, deflate, sdch, br','Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2','Host':'webtrade.xcsc.com','Referer':'https://www.xcsc.com/main/jnx/wsxd/index.shtml','Upgrade-Insecure-Requests':'1','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
		self.sess.headers.update(headers)
	
	def login(self):
		self.sess.get('https://webtrade.xcsc.com/winner/xcsc/',verify=False)
		#set cookies
		ts=random.random()
		self.sess.get('https://webtrade.xcsc.com/winner/xcsc/exchange.action?CSRF_Token=&timestamp=%s&function_id=20&login_type=stock'%ts)
		#get verify code
		vcode_page=self.sess.get('https://webtrade.xcsc.com/winner/xcsc/user/extraCode.jsp')
		with file('/home/yiwen/Desktop/vcode.gif','wb') as output:
			for chunk in vcode_page.iter_content(128):
				output.write(chunk)
		#read vcode from keyboard
		vcode=input('vcode:')
		#login in
		ts=random.random()
		data={'CSRF_Token':'','timestamp':'%s'%ts,'function_id':'200','loginPasswordType':'','content_type':'','version':'200','op_entrust_way':'7','identity_type':'','remember_me':'yes','input_content':'1','account_content':'%s'%self.account,'password':'%s'%self.password,'mac_addr':'undefined','validateCode':'%s'%vcode,'login_type':'stock'}
		login_page=self.sess.post('https://webtrade.xcsc.com/winner/xcsc/user/exchange.action',data=data)
		#find CSRF token
		i=login_page.content.find('CSRF_Token:')
		a=login_page.content[i:].find('\'')
		b=login_page.content[i+a+1:].find('\'')
		self.CSRF_token=login_page.content[i+a+1:i+a+1+b]
		print 'CSRF_token:%s'%self.CSRF_token
		return True

	#get stock infomation
	def quote_one(self,stock_code):
		t0=time.time()
		ts=random.random()
		quote_data={'CSRF_Token':'%s'%self.CSRF_token,'timestamp':'%s'%ts,'service_type':'stock','function_id':'Q0002','codeList':'%s'%stock_code}
		quote_page=self.sess.get('https://webtrade.xcsc.com/winner/xcsc/stock/quote.action',params=quote_data)
		t1=time.time()
		return ('quote:%s'%stock_code,quote_page.content,'time:%s'%((t1-t0)))

	#buy stock
	def buy_one(self,stock_code,price,amount):
		t0=time.time()
		ts=random.random()
		buy_data={'CSRF_Token':'%s'%self.CSRF_token,'timestamp':'%s'%ts,'request_id':'buystock_302','stock_account':'A147024339','exchange_type':'1','entrust_prop':'0','entrust_bs':'1','stock_code':'%s'%stock_code,'entrust_price':'%s'%price,'entrust_amount':'%s'%amount}
		buy_page=self.sess.get('https://webtrade.xcsc.com/winner/xcsc/stock/exchange.action',params=buy_data)
		t1=time.time()
		return ('buy:%s'%stock_code,buy_page.content,'time:%s'%((t1-t0)))

class BatchWorker(threading.Thread):
	def __init__(self,broker,action,args,queue):
		threading.Thread.__init__(self)
		self.broker=broker
		self.action=action
		self.args=args
		self.queue=queue
	
	def run(self):
		if self.action=='b':
			return self.queue.put(self.broker.buy_one(self.args[0],self.args[1],self.args[2]))
		else:
			return self.queue.put(self.broker.quote_one(self.args[0]))

class xczqbatch():
	def __init__(self,account,password):
		self.xczq=xczq(account,password)
		self.queue=Queue.Queue()

	def login(self):
		self.xczq.login()

	def quote_many(self,codes):
		t0=time.time()
		threads=[]
		for i in xrange(len(codes)):
			t=BatchWorker(self.xczq,'q',(codes[i],),self.queue)	
			t.start()
			threads.append(t)
		for t in threads:
			t.join()
		t1=time.time()
		return ('quote:%s'%','.join([str(s) for s in codes]),self.queue,'time:%s'%(t1-t0))
