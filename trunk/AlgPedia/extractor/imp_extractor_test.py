from bs4 import BeautifulSoup	
import urllib2
import gzip, StringIO

def doMain():
	url = "http://pt.wikipedia.org/wiki/Bubble_sort"
	
	headers = {'User-Agent' : 'Mozilla/5.0', 'Accept-Encoding' : 'gzip, defalte' }
	request = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(request)
	#except urllib2.HTTPError, e:
	except Exception, e:
		raise ExtractionError("Error retreiving: " + str(url))
	
	data = decode(response)
	
	pool = BeautifulSoup(data)
	
	
	divs = pool.findAll("div", {"class" : "mw-geshi mw-code mw-content-ltr" })
	
	for div in divs:
		#print div
		language = div.find('div')
		#print language
		print language['class']
	
	#print pool
	
	
def decode(page):
	encoding = page.info().get("Content-Encoding")    
	if encoding in ('gzip', 'x-gzip', 'deflate'):
		content = page.read()
		if encoding == 'deflate':
			data = StringIO.StringIO(zlib.decompress(content))
		else:
			data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(content))
	page = data.read()

	return page
		
doMain()