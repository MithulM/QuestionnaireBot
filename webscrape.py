# getting the data
import requests
from urllib.request import urlopen
from lxml import etree

# get html from site and write to local file
url = 'https://www.starwars.com/news/15-star-wars-quotes-to-use-in-everyday-life'
headers = {'Content-Type': 'text/html', }
response = requests.get(url, headers=headers)
html = response.text
with open('star_wars_html', 'w') as f:
    f.write(html)

# read local html file and set up lxml html parser
local = 'insert_browser_file_path_here'
response = urlopen(local)
htmlparser = etree.HTMLParser()
tree = etree.parse(response, htmlparser)
tree.xpath('//p/strong/text()')