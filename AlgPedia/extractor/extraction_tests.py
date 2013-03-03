from bs4 import BeautifulSoup
import urllib2
import gzip
import StringIO

from Extractor import ColumnExtractor
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
		
	def handle_data(self, d):
		self.fed.append(d)
		
	def get_data(self):
		return ''.join(self.fed)

	def strip_tags(self, html):
		self.feed(html)
		return self.get_data() 


class ExtractionError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
		
class UserAgentHtmlScraper:
	def __init__(self, user_agent='Mozilla/5.0'):
		self.headers = {'User-Agent' : user_agent, 'Accept-Encoding' : 'gzip, defalte' }
	
	def search_page(self, url):
		self.url = url
		
		request = urllib2.Request(self.url, None, self.headers)
		try:
			response = urllib2.urlopen(request)
		#except urllib2.HTTPError, e:
		except Exception, e:
			raise ExtractionError("Error retreiving: " + str(url))
		
		data = self.decode(response)
		
		#self.pool = BeautifulSoup(response.read())
		self.pool = BeautifulSoup(data)
		print "Fetched : " + str(self.url)
		
	def search_for_div_id(self, id, tag=None):
		match_dict = {"id" : id}
		if tag:
			div_tag = tag.find("div", match_dict)
		else:
			div_tag = self.pool.find("div", match_dict)
			
		return div_tag
		
	def search_for_p(self, tag=None):
		if tag != None:
			div_tag = tag.find("p")
		else:
			div_tag = self.pool.find("p")
		
		return div_tag	
	
	def search_for_id_expression(self, expression, ids):
		tags = expression.split('.')
		div_count = 0
		aux_tag = ''
		
		for tag in tags:
			if(tag.upper() == 'DIV'):
				aux_tag = self.search_for_div_id(ids[div_count])
				div_count += 1
			elif(tag.upper() == 'P'):
				aux_tag = self.search_for_p(aux_tag)

	
	def get_alg_about(self):
		#div = self.pool.find("div", {"id" : 'mw-content-text' })
		div = self.pool.find("div", {"class" : "mw-content-ltr" })
		about = div.find('p')
		return about
			
			
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

def doMain():
	file_name = './temp/dbpedia_fetch_0.csv'
	col_extractor = ColumnExtractor(file_name)
	
	# wiki links are the 3rd (2 in 0-based) column in the .csv
	wiki_links = col_extractor.extractColumn(2)
	
	html_scraper = UserAgentHtmlScraper()
	
	# div  id="mw-content-text" achar primeiro <p> dentro dessa div
	
	# div id="p-lang" -> procurar um ul dentro de um div com class=body
	# dentro desse ul tem que ter uma li com id "interwiki-pt"
	# dentro desse li tem o link
	
	#link = "http://en.wikipedia.org/wiki/Alpha_algorithm"
	
	#html_scraper.search_page(link)
	#about = html_scraper.get_alg_about()
	#try:
		#print about.text
	#except Exception:
		#print "Error retreiving: " + str(link)
	
	#stripper = MLStripper()
	#print stripper.strip_tags(it.text)
	#it = html_scraper.search_for_div_id('mw-content-text')

	
	file = open('./temp/abouts.txt', 'w')
	
	for link in wiki_links:
		try:
			html_scraper.search_page(link)
			about = html_scraper.get_alg_about()
			line = about.text
			file.write('\n')
			file.write(line.encode(encoding="UTF-8"))
			file.write('\n')
		except Exception, e:
			print e
			file.write(str(e))
		
	
	file.close()
		

doMain()