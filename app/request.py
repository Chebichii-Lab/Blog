import urllib.request,json
import request,json

def get_quotes():
    response = request.get('http://quotes.stormconsultancy.co.uk/random.json')
    if response.status_code == 200:
        quote = response.json()
        return quote