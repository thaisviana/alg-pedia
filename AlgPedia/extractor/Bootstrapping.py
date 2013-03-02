'''
Created on 01/03/2013

@author: Pericolo
'''

import os
from extractor.FileWriters import TXTWriter
from extractor.Extractor import ColumnExtractor
from extractor.DBPediaQueryFetcher import QueryFetcher
from algorithm.models import Classification

class Bootstrapper():
	def __init__(self):
		pass
	
	
	def doDatabaseImporting(self):
		query_fetcher = QueryFetcher('csv')
		dbpedia_master_query = '''select * where{
			?classification skos:broader <http://dbpedia.org/resource/Category:Algorithms>.
			?algorithm dcterms:subject ?classification.
			?algorithm foaf:isPrimaryTopicOf ?wikipedia
			}'''

		filename = query_fetcher.fetchResult(dbpedia_master_query)
		
		# always 0-based, baby
		#self.insertClassifications(filename, 0)
		
		# second parameter is a list of columns that will be used create the classification object
		self.insert_classifications(filename, [0])
		
	def insert_classifications(self, filename, cols):
		col_extractor = ColumnExtractor(filename)
		
		col_classification = col_extractor.extractColumn(cols[0])
		
		(names, uris) = self.extract_names(col_classification)
		
		names, uris = (list(t) for t in zip(*sorted(zip(names,uris))))
		
		classifications = [{'name' : t[0], 'uris' : t[1]} for t in zip(names, uris)]
		
		for classification in classifications:
			aux_classification = Classification(name=classification['name'], uri=classification['uris'])
			aux_classification.save()
		
		
	def extract_names(self, classif_list):

		beautiful_names = dict()
		
		names = map(lambda x: x.split(':')[-1], classif_list)
		names = map(lambda x: x.replace('_', ' ').title(), names)
		
		for i in range(0, len(names)):
			#print "Key: " + str(names[i]) + " Value: " + classif_list[i]
			
			if(names[i] not in beautiful_names):
				beautiful_names[names[i]] = classif_list[i]	
		return (beautiful_names.keys(), beautiful_names.values())		
	
	def insertClassifications(self, filename, col_number):
	
		col_extractor = ColumnExtractor(filename)
		
		col_classification = col_extractor.extractColumn(col_number)
		
		classif_names = self.extractNames(col_classification)
			
		txt_Writer = TXTWriter()
		
		file_name = txt_Writer.writeDictKeysToFile(classif_names, 'classifications')
		
		for key, val in classif_names.iteritems():
			#print str(key) + ': ' + str(val)
			aux_classification = Classification(name=key, uri=val)
			aux_classification.save()
	
	# returns a list of beautiful names.	
	# each name only appears once in this list.
	def extractNames(self, classif_list):

		beautiful_names = dict()
		
		names = map(lambda x: x.split(':')[-1], classif_list)
		names = map(lambda x: x.replace('_', ' ').title(), names)
		
		for i in range(0, len(names)):
			#print "Key: " + str(names[i]) + " Value: " + classif_list[i]
			
			if(names[i] not in beautiful_names):
				beautiful_names[names[i]] = classif_list[i]	
		return beautiful_names
		#return (beautiful_names.keys(), beautiful_names.values())
		