'''
Created on 26/02/2013

@author: Pericolo
'''
import os
import urllib
import urllib2
from FileWriters import HTMLWriter, CSVWriter

class QueryFetcher:
    
    def __init__(self, fetch_format, temp_folder=os.path.abspath('./extractor/temp')):
        
		self.n_fetch = 0
		self.temp_folder = temp_folder
		self.base_url = 'http://dbpedia.org/sparql'
            
		self.get_params = {
			  'query' : '',
			  'default-graph-uri' : 'http://dbpedia.org',
			  'format'  : 'text/html',
			  'timeout' : 0,
			  'debug' : 'on'
		}
		
		# Creating the appropriate type of writer
		if(fetch_format.upper() == 'HTML'):
			self.file_writer = HTMLWriter(self.temp_folder)
		elif(fetch_format.upper() == 'CSV'):
			self.file_writer = CSVWriter(self.temp_folder)
            
	# fetch the resource and delegate the writing of the file to the
	# appropriate instance of FileWriter
    def fetchResult(self, query_string):
        
        self.get_params['query'] = query_string
        
        query_url = self.base_url + '?' + urllib.urlencode(self.get_params)
        
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        response = opener.open(query_url)
        the_page = response.read()
        
        file_path = self.file_writer.writeFile(the_page, 'dbpedia_fetch_%d' % self.n_fetch)
        
        self.n_fetch += 1;
        
        return file_path
    
    # change the output path of the fetched resource
    def changeOutputFolder(self, new_folder_path):
        self.temp_folder = new_folder_path
        self.file_writer.updateOutputFolderPath(new_folder_path)
        
        