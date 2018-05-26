# -*- coding: utf-8 -*
import urllib3
import datetime
import io
import time
import threading
import pymysql
from apscheduler.schedulers.background import BackgroundScheduler


class db(object):
	def __init__(self, host, user, passwd, db, port=3306, charset='utf8'):
		self.host = host
		self.user = user
		self.passwd = passwd
		self.db = db
		self.port = port
		self.charset = charset
		self.connect()
		self.refresh()

	async def get(self, sql):
		self.cursor.execute(sql)
		return self.cursor.fetchone()

	async def query(self, sql):
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	async def execute(self, sql):
		try:
			self.cursor.execute(sql)
			self.conn.commit()
		except Exception as e:
			self.conn.rollback()

	def connect(self):
		self.conn = pymysql.connect(
						host = self.host, 
						port = self.port, 
						user = self.user,
						passwd = self.passwd,
						db = self.db,
						charset = self.charset
						)
		self.cursor = self.conn.cursor()

	# 每隔28000s，自动刷新连接（针对IPCIS_DNS_DB库）
	def refresh(self):
		s = BackgroundScheduler()
		s.add_job(self.close, 'interval', seconds=28000)
		s.add_job(self.connect, 'interval', seconds=28000)

		s.start()

	def close(self):
		self.cursor.close()
		self.conn.close()


#定义ip转数字的方法
ip2num = lambda x:sum([256**j*int(i) for j,i in enumerate(x.split('.')[::-1])])

#定义数字转ip的方法
num2ip = lambda x: '.'.join([str(x/(256**i)%256) for i in range(3,-1,-1)])

#定义读取域名IP字典的方法
def readIpdt(addr):
    content = None
    with io.open(addr, 'r', encoding='utf-8') as file:
        content = eval(file.read())
        return content

#定义查询流记录的方法
def search_ip_activity(ip,date):
	#传入参数为IP的字符串形式，返回出记录和入记录

	#通过url抓取Ip活动记录
	url ="http://211.65.197.210:8080/IPCIS/activityDatabase/?IpSets="+ip+":32&TableName="+str(date)+"&Mode=2" 

	#time.strftime("%y-%m-%d")+ 
	response = urllib3s.urlopen(url)   
	html = response.read()  
	response.close()

	ip_act_dic=eval(html)
	outact=inact=[]

	for k,v in ip_act_dic.items():
		outact = v[0]
		inact = v[1]
	return outact,inact

#定义插入IP活动的方法				
async def insert_ip_activity_record(ip1,ip2,msqlink,date):
	#按条插入IP活动记录
	#传入ip的字符串形式 和数据库链接
	
	numofip1=ip2num(ip1)
	numofip2=ip2num(ip2)
	
	#查询是否存在该记录
	sql="SELECT 1 FROM known_malicious.ip_activity_record  WHERE ip_1=%s AND ip_2=%s  LIMIT 1;"%(numofip1,numofip2)  
	result=await msqlink.query(sql,1)


	if result==None :
	#若不存在，插入ip1 ip2活动数据
		sql="INSERT INTO known_malicious.ip_activity_record(ip_1,ip_2,date) values(%s,%s,'%s');"%(numofip1,numofip2,str(date))           
		await msqlink.execute(sql)
	#查询IP2的，经纬度并填入	
		sql="SELECT longitude,latitude FROM center_ipcis.IP2Location WHERE ipStart<=%s AND ipEnd>=%s;"%(numofip2,numofip2)
		result=await msqlink.query(sql,1)

		sql="UPDATE known_malicious.ip_activity_record set ip_2_lnglat ='%s' WHERE ip_2=%s "%(str(round(result[0],2))+','+str(round(result[1],2)),numofip2)
		await msqlink.execute(sql)
    
	#若存在，更新count和date
	else :
		sql="UPDATE known_malicious.ip_activity_record set count=count+1,date='%s' WHERE ip_1=%s AND ip_2=%s;"%(str(date),numofip1,numofip2)           
		await msqlink.execute(sql)
	        
	        
#定义填写ip_activity_record表格的方法
async def ip_activity_record(msqlink,outrecord,inrecord,date):	
#按流记录批量写入数据库
	if outrecord != []:
		for item in outrecord:
			outrecord_split=item.split( )
			
			ip1=outrecord_split[0]
			ip2=outrecord_split[1]
			await insert_ip_activity_record(ip1,ip2,msqlink,date)

	if inrecord != []:
		for item in inrecord:
			inrecord_split=item.split( )
			
			ip1=inrecord_split[1]
			ip2=inrecord_split[0]
			await insert_ip_activity_record(ip1,ip2,msqlink,date)

#定义domain2ip表格的填写		
async def domain2ip(msqlink,domain,ip):
	#传入IP的字符串形式,流记录
	
	#插入域名IP数据
	sql="INSERT into known_malicious.domain2ip (domain_name,ip_1) values ('%s',%s)"%(domain,ip2num(ip))
	await msqlink.execute(sql)

	#查询位置数据
	sql="SELECT country,region,city,longitude,latitude from center_ipcis.IP2Location where ipStart<=%s and ipEnd>=%s"%(ip2num(ip),ip2num(ip))
	result=await msqlink.query(sql,1)

	#更新位置数据
	if result:
		#更新location
		sql="UPDATE known_malicious.domain2ip set ip_1_location ='%s' where ip_1=%s "%(result[0]+"-"+result[1]+"-"+result[2],ip2num(ip))
		await msqlink.execute(sql)

		#更新lnglat
		sql="UPDATE known_malicious.domain2ip set ip_1_lnglat ='%s' where ip_1=%s "%(str(round(result[3],2))+','+str(round(result[4],2)),ip2num(ip))
		await msqlink.execute(sql)

#更新活动记录次数
async def update_ip_activiy_count(msqlink,ip,record):
	activity_count=len(record)

	sql="select ip_activity from domain2ip where ip_1=%s;"%(ip2num(ip))

	ip_activity=eval(await msqlink.query(sql,1)[0])

	if len(ip_activity)==14:
		del ip_activity[0]

	ip_activity.append(activity_count)

	#更新活动次数数据
	sql="UPDATE known_malicious.domain2ip set ip_activity ='%s' where ip_1=%s "%(str(ip_activity),ip2num(ip))

	await msqlink.execute(sql)


#定义primary2name表格的填写
async def primary2name(msqlink1,msqlink2,domain):
	
	sql="select domain_id from resolved_ip where domain_name = '%s'"%(domain)
	domain_id=await msqlink2.query(sql,1)
	sql="select primary_domain from domain_name where domain_id = '%s'"%(domain_id[0])
	primary_domain=await msqlink2.query(sql,1)
	sql=("INSERT INTO primary2name (domain_id,primary_domain,domain_name) values('%s','%s','%s')")%(domain_id[0],primary_domain[0],domain)
	await msqlink1.execute(sql)



# 添加domain_static表的is_dga,ttl字段
async def add_static(msqlink1,msqlink2,domain):
	sql = ("SELECT primary_domain, is_dga, ttl FROM domain_name "
			"WHERE primary_domain = '%s';" % domain)
	rs = await msqlink2.query(sql)

	for item in rs:
		sql1 = ("INSERT INTO domain_static (primary_domain, is_dga, ttl) "
				"VALUES (%s, %s, %s)" % item)
		await msqlink1.execute(sql)


# 添加domain_static表的register_year字段
async def add_register_years(msqlink1,msqlink2,domain):
	times = ()
	time_diff = ""
	sql_get = ("SELECT register_date, expire_date FROM domain_whois "
	"WHERE primary_domain = '%s';") % domain
	rs = await msqlink2.query(sql_get,1)
	if rs != None:
		times = rs

	try:	
		temp = datetime.standard2timestamp(rs[1]) - datetime.standard2timestamp(rs[0])
		time_diff = datetime.timestamp2diff(temp)
	except:
		pass

	sql_set = ("UPDATE domain_static SET register_years = '%s' "
	"WHERE primary_domain = '%s';") % (time_diff, domain)
	await msqlink1.execute(sql_set)

# 添加domain_static表的credit字段
async def add_credit(msqlink1,msqlink2,domain):
	ret = None
	scoreDict = {"safe": 100, "unsure": 70}
	sql = "SELECT evidence FROM domain_name WHERE primary_domain='%s';" % domain
	rs = await msqlink2.query(sql,1)
	if rs != None:
		arr = rs.split("\"")[2:]
		temp = None
		for item in arr:
			if item == "safe" or item == "unsure":
				temp = scoreDict[item]
		ret = temp

	if ret == None:
		sql_update = "UPDATE domain_static SET credit=NULL WHERE primary_domain='%s';" % domain
	else:
		sql_update = "UPDATE domain_static SET credit=%d WHERE primary_domain='%s';" % (ret, domain)

	await msqlink1.execute(sql_update)


async def domain_static(msqlink1,msqlink2,domain):
	await add_static(msqlink1,msqlink2,domain)
	await add_register_years(msqlink1,msqlink2,domain)
	await add_credit(msqlink1,msqlink2,domain)


async def newip(addr):
	try:
		#建立数据库连接
		known_m = db(host="211.65.193.23", user="root", passwd="admin246531",  db="known_malicious",port=3306)
		dns_db = db(host="211.65.193.193", user="ipcis", passwd="", db="IPCIS_DNS_DB",port=3307)

		#读取域名IP字典
		domain2ip_contact=readIpdt(addr)

		#遍历字典
		for domaindata,ipdata in domain2ip_contact.items(): 	
		
			#填入域名IP记录
			await domain2ip(known_m,domaindata,ipdata[0])	
			#填入域名主域名对应关系
			await primary2name(known_m,dns_db,domaindata)

			#填domain_static
			await domain_static(known_m,dns_db,domaindata)

			today = datetime.date.today()
			for d in range(14):

				date = today - datetime.timedelta(days=13-d)
				#查询活动记录
				outrec,inrec=search_ip_activity(ipdata[0],date)
				rec=outrec+inrec
				
				#填入活动记录
				await ip_activity_record(known_m,outrec,inrec,date)
				
				#填活动记录次数
				await update_ip_activiy_count(known_m,ipdata[0],rec,date)

		known_m.close()
		dns_db.close()

	except Exception as e:
		return False
	else:
		return True


async def update_ip_activiy_record():
	#建立数据库连接
	known_m = db(host="211.65.193.23", user="root", passwd="admin246531",  db="known_malicious",port=3306)
	dns_db = db(host="211.65.193.193", user="ipcis", passwd="", db="IPCIS_DNS_DB",port=3307)

	sql="select ip_1 from domain2ip;"
	iplist=await known_m.query(sql)

	for ip in iplist:
		today = datetime.date.today()
		#查询活动记录
		outrec,inrec=await search_ip_activity(num2ip(ip[0]),today)
		rec=outrec+inrec
		
		#填入活动记录
		await ip_activity_record(known_m,outrec,inrec,today)
		
		#填活动记录次数
		await update_ip_activiy_count(known_m,num2ip(ip[0]),rec)

	known_m.close()
	dns_db.close()
	#自动化，每隔10S运行一次
	global timer
	timer=threading.Timer(10,update_ip_activiy_record)
	timer.start()
