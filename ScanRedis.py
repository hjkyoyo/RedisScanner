#!/usr/bin/python  
import redis

#Author:hjkyoyo
#date:2017-11-03


def Connect(host,port):
	result = redis.Redis(host, port, db = 0)
	try:
		response = result.ping() 
	except redis.exceptions.ResponseError:
		print "     It's need a password."
		return 0
	except redis.exceptions.ConnectionError:
		print "     Can't connecting to %s:%d."%(host,port)
		return -1
	else:
		if response == True:
			print "     %s:%d has no password, and we record it in result.txt"%(host,port)
			return 1
			
def Scan(h_file, p_file, r_file):
	#open files of host and result
	h_f = open(h_file, "r+")
	r_f = open(r_file, "w+")
	#Initialization
	port = 6379
	host = "localhost"
	#Write title of result
	r_f.write("The following machines could be unauthorized access!\n")
	#Enter the loop of host
	while 1:
		line_h = h_f.readline()
		#if file end, break loop of host
		if not line_h:
			break
		#else get values of hosts
		host = line_h.strip('\n')
		#print host
		#open the file of port
		p_f = open(p_file, "r+")
		#enter the loop of port
		while 1:
			line_p = p_f.readline()
			# if file end, break loop of port
			if not line_p:
				break
			#else get values of ports
			port = int(line_p.strip('\n'))
			print ("%s:%d")%(host,port)
			#try to access the redis without password			
			result =Connect(host,port)
			#if redis has no password, record its host and port
			if result == 1:
				label = "%s:%d\n"%(host,port)
				r_f.write(label)
				break
			#if  this redis has password, scan next host	
			elif result == 0:
				break
		
		p_f.close()
				
	h_f.close()
	r_f.close()

Scan("hosts.txt","ports.txt","result.txt")
		
			
