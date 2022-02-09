from requests import Request, Session
import json
import logging, sys
import requests

def send_mailContent(mailContent):
    headers = { 'Content-type': 'application/json', 'Accept': 'text/plain' }
    r = requests.post('https://swgtracker.com/import_mailcontent.php', data=mailContent, headers=headers)
    return r

