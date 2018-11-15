import json,os
from configparser import *
import codecs
import psycopg2
from ast import literal_eval

class dbConnect():
	''' DBConnect class for making connection with Database to provide Scalable data ingestion platform'''
	def __init__(self,param):
		self.user=param['user']
		self.password=param['password']
		self.database=param['database']
		self.host=param['host']
		self.port=int(param['port'])
		
	def isDigit(self,x):
		try:
			float(x)
			return True
		except ValueError:
			return False
	def returnValueFromDict(self,data,column,fact_columns):
		try:
			if self.isDigit(data[column]): 
				if str(data[column]).isdigit(): return int(data[column])
				else: return float(data[column])
			elif isinstance(data[column],(basestring,str,unicode)): return data[column].encode('utf-8')
		except KeyError:
			if column in fact_columns:
				return 0
			else: return ''
	def sqlIngestion(self,data,columns,tableName,fact_columns):
		columnBuilder = str(tuple(map(lambda column: str(column),columns)))
		valueBuilder=str(tuple(map(lambda column: self.returnValueFromDict(data,column,fact_columns),columns)))
		# Insert Query
		queryBuilder="INSERT INTO "+str(self.database)+"."+str(tableName)+" VALUES "+valueBuilder+";"
		conn = psycopg2.connect(dbname=self.database,host=self.host,port=self.port,user=self.user, password=self.password)
		cur = conn.cursor()
		try:
			print(queryBuilder)
			cur.execute(queryBuilder)
			print(cur.fetchone()[0])
		except psycopg2.ProgrammingError as e: print(e)
		finally: 
			cur.close();
			conn.close();
			
def main():
	dataJson=[]
	# Table and Columns properties from Config INI file
	config = ConfigParser()
	config.optionxform = str
	config.read('../config/config.ini')
	def config_grabber(section):
		temp = dict()
		for i in config.options(section): temp.update({i:config.get(section,i)})
		return temp
	print(config_grabber("dbConfig"))
	dbobj = dbConnect(config_grabber('dbConfig'))
	reader = codecs.getreader("utf-8")
	for each_section in config.sections():
		print(each_section)
	try:
		for line in open('../data/immobilienscout24_berlin_20181113.json', 'rb+'):
			data = json.loads(line.decode('utf8'))
			#dataJson.append(json.loads(reader(line)))
			for tableName in  literal_eval(config_grabber('tableConfig')['tableNames']):	
				columns=literal_eval(config_grabber(tableName)['columns'])
				dbobj.sqlIngestion(data['data'],columns,tableName,columns)
	except Exception as e:print("JSON Exception",e);exit()
if __name__ == "__main__":
	main()
		