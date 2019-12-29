import argparse

class Argparse(object):

	def __init__(self):
		self.msg = '''  python mysql.py logfile --option
                                example: python mysql.py mysql-slow.log --top-slack
			   '''
		self.parser = argparse.ArgumentParser(prog='MySQLslow', description='MySQL slow query Analyzer', usage=self.msg)
		self.parser._optionals.title = "OPTIONS"

	def arg_options(self):
		parser = self.parser
		parser.add_argument('file', help = "MySQL slow queries file")
		parser.add_argument('--top-slack', dest='topslack', action='store_true', help = "Send top slow queries to Slack channel")
		return parser.parse_args()

