from bs4 import BeautifulSoup
import re
import parse

# Extracting URLs from Leafly sitemap using BeautifulSoup to parse
soup = BeautifulSoup(open("./LeaflySitemap.xml", "r"), "lxml-xml")
urls  = [a.text for a in (urls.find("loc") for urls in soup.find_all("url")) if a]

# Extracting only strain URLs from the complete list
# Required URLs have format https://www.leafly.com/{sativa|indica|hybrid}/{strain_name}
regexExp = "https?:\/\/(www\.)?(leafly\.com)\/(hybrid|sativa|indica)\/+[^\/]+[-a-zA-Z0-9@:%._\+~#=]$"
regex = re.compile(regexExp)
strain_URLs = list(filter(regex.search, urls))

i = 0
siz = len(strain_URLs)
for url in strain_URLs:
    parse.get_data(url)
    print('\r' + str(100 * i / siz),end='')
    i+=1
