#!/usr/bin/python  
import redis

#Author:hjkyoyo
#date:2017-11-03

def auth(host,port,list):
	result = redis.Redis(host, port, db = 0)
	try:
		response = result.ping() 
	except redis.exceptions.ResponseError:
		print "     It's need a password."
		return True
	except redis.exceptions.ConnectionError:
		print "     Can't connecting to %s:%s."%(host,port)
		return False
	else:
		if response == True:
			print "     %s:%s has no password, and we record it in result.txt"%(host,port)
			label ="%s:%s\n"%(host,port)
			list.append(label)
			return True

def listfromtxt(filename):
	list = []
	with open(filename,"r+") as fo:
		while 1:
			line =fo.readline()
			if not line:
				return list
			line = line.strip('\n')
			list.append(line)
			
def writetotxt(filename,list):
	with open(filename,"w+") as fo:
		for line in list:
			fo.write(line)
			
def Scan(h_file,p_file,r_file):
	hosts = listfromtxt(h_file)
	ports = listfromtxt(p_file)
	
	foods = []
	
	foods.append("The following machines could be unauthorized access!\n")
	
	for host in hosts:
		print host
		for port in ports:
			result = auth(host,port,foods)
			if result == True:
				break
	#with open(r_file,"w+") as fo:
		#for food in foods:
			#fo.write(food)
	writetotxt(r_file,foods)

Scan("hosts.txt","ports.txt","result.txt")
		
			
