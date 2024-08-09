from django.core.mail import EmailMessage
import os
from django.core.signing import Signer

class Util:
  @staticmethod
  def send_email(data):
    email = EmailMessage(
      subject=data['subject'],
      body=data['body'],
      from_email=os.environ.get('EMAIL_FROM'),
      to=[data['to_email']]
    )
    email.send()


def generate_signed_url(file_id):
    signer = Signer()
    signed_value = signer.sign(file_id)
    return signed_value


import requests

def fetch_book_data(query, api_key):
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
