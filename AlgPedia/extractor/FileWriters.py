'''
Created on 26/02/2013

@author: Pericolo
'''

#encoding: utf-8

import os
from bs4 import BeautifulSoup

class FileWriter():
    def __init__(self,params):
        pass

    def writeFile(self, text, file_name):
        pass

class HTMLWriter(FileWriter):
    def __init__(self, output_folder='./extractor/temp'):
        self.base_path = output_folder
        self.file_extension = 'html'

    def writeFile(self, text, file_name):
        file_path = os.path.join(self.base_path, file_name + '.' + self.file_extension)

        F_HANDLE = open(file_path, 'w')

        F_HANDLE.write(text)

        F_HANDLE.close()

        return file_path

    def updateOutputFolderPath(self, new_folder_path):
        self.base_path = new_folder_path

class CSVWriter(FileWriter):
    def __init__(self, output_folder='./extractor/temp'):
        self.base_path = os.path.abspath(output_folder)
        self.file_extension = 'csv'

    def writeFile(self, html, file_name):
		file_path = os.path.join(self.base_path, file_name + '.' + self.file_extension)

		file_converter = HTMLToCSV(html)

		#print file_path
		
		F_HANDLE = open(file_path, 'w')
		
		iterator = iter(file_converter.convert())
		
		F_HANDLE.write(iterator.next())
		
		for item in iterator:
			F_HANDLE.write('\n')
			F_HANDLE.write(item)

		F_HANDLE.close()

		return file_path

class TXTWriter(FileWriter):
	def __init__(self, output_folder='./extractor/temp'):
		self.base_path = os.path.abspath(output_folder)
		self.file_extension = 'txt' 
				
	def writeLinesToFile(self, list, file_name):
		file_path = os.path.join(self.base_path, file_name + '.' + self.file_extension)

		F_HANDLE = open(file_path, 'w')
		
		list.sort()
		iterator = iter(list)

		F_HANDLE.write(iterator.next())

		for item in iterator:
			F_HANDLE.write('\n')
			F_HANDLE.write(item)

		F_HANDLE.close()

		return file_path
		
	def writeDictKeysToFile(self, dict, file_name):
		file_path = os.path.join(self.base_path, file_name + '.' + self.file_extension)

		F_HANDLE = open(file_path, 'w')

		keys = dict.keys()
		keys.sort()
		
		iterator = iter(keys)

		F_HANDLE.write(iterator.next())

		for item in iterator:
			F_HANDLE.write('\n')
			F_HANDLE.write(item)

		F_HANDLE.close()

		return file_path
		
	def writeDictValuesToFile(self, dict, file_name):
		file_path = os.path.join(self.base_path, file_name + '.' + self.file_extension)

		F_HANDLE = open(file_path, 'w')

		vals = dict.values()
		vals.sort()
		
		iterator = iter(vals)

		F_HANDLE.write(iterator.next())

		for item in iterator:
			F_HANDLE.write('\n')
			F_HANDLE.write(item)

		F_HANDLE.close()

		return file_path
	
class XMLWriter(FileWriter):
    def __init__(self, params):
        pass

class JSONWriter(FileWriter):
    def __init__(self, params):
        pass

# testar
class RDFWriter(FileWriter):
	def __init__(self, algorithm, implementations):
		self.algorithm = algorithm
		self.RDF_variables = {'ALG_NAME': '', 'ALG_URI': '', 'CAT_NAME': '', 'CAT_URI': '', 'IMPLEMENTATION_URIS' : []}
	
	def generate_RDF_text(self):
		path = os.path.join(os.path.dirname(__file__), '../algorithm/rdf/rdf_modelo.xml').replace('/','\\')
		
		self.RDF_variables['ALG_NAME'] = algorithm.name 
		self.RDF_variables['ALG_URI'] =  algorithm.get_show_url()
		self.RDF_variables['CAT_NAME'] = algorithm.classification.name
		self.RDF_variables['CAT_URI'] = algorithm.classification.get_show_url()
		
		for implementation in implementations:
			self.RDF_variables['IMPLEMENTATION_URI'].append(implementation.get_show_url())
		
		alg_rdf_text = self.replace_vars_in_template(self.RDF_variables)
		
		print alg_rdf_text
		return alg_rdf_text
		
	def replace_vars_in_template(self, variables):
		template_path = os.path.join(os.path.dirname(__file__), '../algorithm/rdf/rdf_modelo.xml').replace('/','\\')
		
		rdf_template = open(template_path)
		lines = rdf_model.readlines()
		rdf_template.close()
		
		text = '\n'.join(lines)
		
		implementation_uri_template = "<algpedia-owl:implementation rdf:resource=\"IMPLEMENTATION_URI\" />"
		
		variables['IMPLEMENTATION_URIS'] = map(lambda uri: "<algpedia-owl:implementation rdf:resource=" + URI + " />", variables['IMPLEMENTATION_URIS'])
		
		variables['IMPLEMENTATION_URIS'] = '\n'.join(variables['IMPLEMENTATION_URIS'])
		
		for variable, value in variables.iteritems():
			text.replace(variable, value)
		
		return text
		
# HTMLToXXX converter Classes
class HTMLToCSV:
    def __init__(self, html):
        self.html = html

    def convert(self):
        table = BeautifulSoup(self.html)
        converted = list()

        for row in table.findAll('tr'):
            aux = list()
            for col in row.findAll('td'):
                aux.append(col.string)
            line = ';'.join(aux)
            if(line != ''):
				converted.append(line.encode(encoding='UTF-8'))

        return converted
				
class HTMLToXML:
	pass

class HTMLToJSON:
	pass
