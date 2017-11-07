#!/usr/bin/python  
import redis
import MySQLdb

#Author:hjkyoyo
#date:2017-11-07

def getdatafrommysql(datatype, table):
	db = MySQLdb.connect("localhost","root","","redis") # connect to database
	cursor = db.cursor() # handle database

	sql = "SELECT %s from %s" % (datatype, table) # get data
	try:                             #execute sql of getting data
		cursor.execute(sql)
		data = cursor.fetchall()

		return data
		
	except:
		print "Error: unable to fetch data"

	db.close() #close database
	
def writetomysql(host, port):
	db = MySQLdb.connect("localhost","root","","redis") #connect to database
	cursor = db.cursor() #handle database
	
	sql = "INSERT INTO redis(host,port) values ('%s', %d)" % (host, port)
	#print sql
	try:
		cursor.execute(sql)
		db.commit()
	except:
		print "database write error"
		db.rollback()
	db.close()

def auth(host,port):
	result = redis.Redis(host, port, db = 0)
	try:
		response = result.ping() 
	except redis.exceptions.ResponseError:
		print "     It's need a password."
		return True
	except redis.exceptions.ConnectionError:
		print "     Can't connecting to %s:%d."%(host,port)
		return False
	else:
		if response == True:
			print "     %s:%d has no password, and we record it in database"%(host,port)
			writetomysql(host,port)
			return True
			
def Scan():
	hosts = getdatafrommysql("host","hosts")
	ports = getdatafrommysql("port","ports")
	
	#print hosts
	#print ports
				
	for host in hosts:
		host = host[0]
		print host
		for port in ports:
			port=port[0]
			print "port:%d " % port
			result = auth(host,port)
			if result == True:
				break

Scan()

