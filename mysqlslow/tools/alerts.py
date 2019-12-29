import slack
from configparser import ConfigParser

parser = ConfigParser()
parser.read('./conf/setup.ini')

class SlackAlerter(object):

	def __init__(self):
		self.slack_webhook_url = None
		self.slack_api_token   = parser.get('Slack', 'slack_api_token')
		self.client = slack.WebClient(token=self.slack_api_token)
		self.slack_channels = parser.get('Slack', 'slack_channels')

	def file_upload(self, _file, _title):
		# Add files:write:user to OAuth scopes 'https://api.slack.com/scopes' 
		upload = self.client.files_upload(channels=self.slack_channels, file=_file, title=_title) 
		return upload
			

