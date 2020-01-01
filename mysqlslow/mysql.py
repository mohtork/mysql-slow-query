import re
import sqlparse
import logging
from heapq import nsmallest
from sqlparse.sql import Where, Comparison, Parenthesis

from tools.arg_parse import Argparse
from tools.alerts import SlackAlerter

class SlowQuery(object):
	def __init__(self):
		#self.date reges support both "180708 11:01:11" and "2019-12-23T15:46:47.441141Z" date formats for mysql 5.7 & earlier
		self.date = r"([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])[A-Za-z])(
		            [01]?[0-9]|2[0-3]):[0-5][0-9]|\d{6}\s+\d{1,2}:\d{2}:\d{2}"
		self.host = re.compile(r"#\s+User@Host:\s+"
                         r"(?:([\w\d]+))?\s*"
                         r"\[\s*([\w\d]+)\s*\]\s*"
                         r"@\s*"
                         r"([\w\d]*)\s*"
                         r"\[\s*([\d.]*)\s*\]")
		self.time = re.compile(r"#\s+Time:\s+(" + self.date + r")")
		self.query_time = re.compile('Query_time:\s(\d+.\d+)\s+')
		self.lock_time = re.compile('Lock_time:\s(\d+.\d+)\s')
		self.rows_sent = re.compile('Rows_sent:\s(\d+)\s+')
		self.rows_examined = re.compile('Rows_examined:\s(\d+)')
		self.query = re.compile('((SELECT|INSERT|UPDATE)(?s).+?;)')
		self.parser = Argparse()
		self.args = self.parser.arg_options()
		self.Slack = SlackAlerter()
		

	def LogFile(self, file):
		with open(file) as f:
			mystr = '\t'.join([l.strip() for l in f])
			self.time = re.findall(self.time, mystr)
			self.host = re.findall(self.host, mystr)
			self.query_time = re.findall(self.query_time, mystr)
			self.lock_time = re.findall(self.lock_time, mystr)
			self.rows_sent = re.findall(self.rows_sent, mystr)
			self.rows_examined = re.findall(self.rows_examined, mystr)
			self.query = re.findall(self.query, mystr)
		return True

	def SlowDic(self):
		slow_q = [{'Time': self.time,
			  'Host': self.host,
			  'Query Time': self.query_time,
			  'Lock Time': self.lock_time,
			  'Rows Sent': self.rows_sent,
			  'Row Examined': self.rows_examined,
			  'Query': self.query
			 } for self.time, self.host, self.query_time, self.lock_time, self.rows_sent, self.rows_examined, self.query in zip(self.time,
			 self.host, self.query_time, self.lock_time, self.rows_sent, self.rows_examined, self.query)]
		return slow_q

	def Occurr(self):
		list = s.SlowDic()
		d = {}
		l = []
		f = open('slow-query.report', 'w')
		for dict in list:
			for i in dict['Query']:
				if i in d:
					d[i] = d[i]+1
				else:
					d[i] = 1
		for ref, occurnum in nsmallest(10, d.items(), key=lambda kv: (-kv[1], kv[0])):
			f.write(sqlparse.format(ref, reindent=True, keyword_case='upper'))
		f.close()
		return f

	def SlackUpload(self):
		Slack = self.Slack
		return Slack.file_upload('slow-query.report', 'Top slow queries')
		
	def main(self):
		if self.args.topslack:
			s.SlackUpload()

p = Argparse()
s = SlowQuery()
arg = p.arg_options()
if __name__=="__main__":
	s.LogFile(arg.file)
	s.Occurr()
	s.main()
