from django.core.mail import EmailMessage

from google.oauth2 import id_token
from google.auth.transport import requests

class Util:
	@staticmethod
	def send_email(data):
		email = EmailMessage(subject = data['subject'], body = data['email_body'], to = [data['to']])
		email.send()
		

class Google:
	@staticmethod
	def validate(auth_token):
		idinfo = id_token.verify_oauth2_token(auth_token,requests.Request())
		if 'accounts.google.com' in idinfo['iss']:
			return idinfo


