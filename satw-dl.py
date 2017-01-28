import requests
from bs4 import BeautifulSoup
#~ import json
from urllib.parse import urlparse
import urllib.request


def satw_dl(url, max_pages):
	
	"""Pages"""
	
	urls = []
	
	urls.append(url)
	for page in list(range(2, max_pages+1)):
		urls.append(url + 'page' + str(page))
	#~ print(urls[1:])
	
	"""Clean up"""
	
	links = []
	
	for url in urls:
		
		opener = urllib.request.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		response = opener.open(url)
		page = response.read()
		soup = BeautifulSoup(page,'html5lib')
		
		for scrape in soup.find_all("div", class_="col-xs-6 col-sm-2"):
			full_link = [x.get("href") for x in scrape.find_all('a')]
			links.append(full_link[0])
			print(full_link)
	
	"""Extract comic urls"""
	
	actual_comics = []
	
	for link in links:

		opener = urllib.request.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		response = opener.open(link)
		page = response.read()
		soup = BeautifulSoup(page,'html5lib')
		
		comics = []
		
		for comic_link in soup.select('center > a > img'):
			comic = comic_link.get('src')
			comics.append(comic)
			print(comic)
		actual_comics.append(comics[1])
	actual_comics = actual_comics[::-1]
	
	#~ """Dump urls"""
	#~ with open ('satw.json', 'w') as file_object:
		#~ json.dump(actual_comics, file_object)
		#~ print('satw.json', 'exported!')
		
			
	"""Download comics"""	#indexed	
				
	for index, comic in enumerate(actual_comics): 
		
		parsed = urlparse(comic)
		filename = parsed.path.split('/')[-1]
		image_link = requests.get(comic)

		with open(str(index) + ' ' + filename, 'wb') as img_obj:
			img_obj.write(image_link.content)

		print("Download " + filename + " completed!")

satw_dl('https://satwcomic.com/the-world/', 12)
