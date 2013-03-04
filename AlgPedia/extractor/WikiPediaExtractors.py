import re
import urllib2
import StringIO, gzip
from bs4 import BeautifulSoup

class ExtractionError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class WikiPediaAbstractExtractor:
	def __init__(self, user_agent='Mozilla/5.0'):
		self.headers = {'User-Agent' : user_agent, 'Accept-Encoding' : 'gzip, defalte' }
	
	def search_page(self, url):
		self.url = url
		
		request = urllib2.Request(self.url, None, self.headers)
		try:
			response = urllib2.urlopen(request)
		except Exception, e:
			raise ExtractionError("Error retreiving: " + str(url))
		
		data = self.decode(response)
		
		self.pool = BeautifulSoup(data)
		print "Fetched : " + str(self.url)
	
	def get_alg_name(self):
		page_name = re.split('/', self.url)[-1]
		words = re.split('[-_]', page_name)
		words = map(lambda x: x.capitalize(), words)
	
		beautiful_name = ' '.join(words)
		
		return beautiful_name
	
	def get_alg_about(self):
		#div = self.pool.find("div", {"id" : 'mw-content-text' })
		div = self.pool.find("div", {"class" : "mw-content-ltr" })
		about = div.find('p')
		return about.text
			
	def decode(self, page):
		encoding = page.info().get("Content-Encoding")    
		if encoding in ('gzip', 'x-gzip', 'deflate'):
			content = page.read()
			if encoding == 'deflate':
				data = StringIO.StringIO(zlib.decompress(content))
			else:
				data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(content))
		page = data.read()

		return page