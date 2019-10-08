import requests
from bs4 import BeautifulSoup
from pathlib import Path
import urllib
import ctypes

request = requests.get('https://www.bing.com')
soup = BeautifulSoup(request.content, features="html.parser")
img_link = 'https://www.bing.com' + soup.find('link', {'id':'bgLink'})['href']
filename = str(Path.home()).replace('\\','/') + '/Pictures/Wallpapers/' + img_link.split('/')[-1].split('_')[0].split('.')[1] + '.jpeg'
urllib.request.urlretrieve(img_link, filename)
ctypes.windll.user32.SystemParametersInfoW(20, 0, filename , 0)