import os
from algorithm.models import Classification, Implementation, Algorithm, ProgrammingLanguage
from extractor.FileWriters import RDFWriter
def is_database_empty():
	empty = 0
	
	empty += Classification.objects.count()
	empty += Implementation.objects.count()
	empty += Algorithm.objects.count()
	empty += ProgrammingLanguage.objects.count()
	
	return False if empty > 0 else True
	
def wipe_database():
	Algorithm.objects.all().delete()
	Classification.objects.all().delete()
	Implementation.objects.all().delete()
	ProgrammingLanguage.objects.all().delete()

#returns a tuple (names, links) of classifications
def get_all_classifications_name_link():
	collection = dict()
	
	names = []
	links = []
	
	classifications = Classification.objects.order_by("name")
	
	for classification in classifications:
		names.append(classification.name)
		links.append("http://localhost:8000/show/cat/id/" + str(classification.id))
		#collection[classification.name] = "http://localhost:8000/show/cat/id/" + str(classification.id)
	
	classif = [{'name' : t[0], 'link' : t[1]} for t in zip(names, links)]
	
	return classif
	
# returns a	classification object
def get_classification_by_id(c_id):
	try:
		classification = Classification.objects.get(id=c_id)
		return classification
	except Classification.DoesNotExist:
		return []
	

def get_algorithms_by_classification(a_classification):
	try:
		algs = Algorithm.objects.filter(classification=a_classification)
		return algs
	except Algorithm.DoesNotExist:
		return []
		
def insert_classification_db(c_name, c_uri):
	try:
		classif = Classification.objects.get(name=c_name)
		return classif
	except Classification.DoesNotExist:
		aux = Classification(name=c_name,  uri=c_uri)
		aux.save()
		return aux		

def delete_algorithm_db(alg):
	try:
		Algorithm.objects.filter(id=alg.id).delete()
	except Algorithm.DoesNotExist:
		return None
		
	return True

def insert_algorithm(alg_name, alg_about,alg_classification, alg_visible):
	algorithm = Algorithm(name=alg_name, description=alg_about, classification=alg_classification, visible=alg_visible)
	algorithm.save()
	
	return algorithm
	
def insert_algorithm_db(a_name, a_about, a_classif, a_uri, a_visible):
	
	alg, created = Algorithm.objects.get_or_create(name=a_name, description=a_about, classification=a_classif, uri=a_uri, visible=a_visible)
	return alg	
		
def insert_programming_langage_db(i_language):
	p_lang, created = ProgrammingLanguage.objects.get_or_create(name=i_language.upper())		
	return p_lang
		
def insert_implementation_db(i_alg, i_language_id, i_code, i_visible):
	p_lang = insert_programming_langage_db(i_language_id)
		
	implementation = Implementation(algorithm=i_alg, code=i_code, programming_language=p_lang, visible=i_visible)
	implementation.save()
	
	return implementation
	
def get_all_algorithms():
	return Algorithm.objects.order_by("name")
	
def get_algorithm_by_id(a_id):
	try:
		alg = Algorithm.objects.get(id=a_id)
		return alg
	except Algorithm.DoesNotExist:
		return None
		
def get_all_programming_languages():
	return ProgrammingLanguage.objects.order_by("name")

def insert_implementation_alg_p_lang(i_alg, i_p_lang, i_code, i_visible):
	imp = Implementation(algorithm=i_alg, programming_language=i_p_lang, code=i_code, visible=i_visible )
	imp.save()
	
	return imp
	
def get_programming_language_by_id(p_lang_id):
	try:
		p_lang = ProgrammingLanguage.objects.get(id=p_lang_id)
		return p_lang
	except ProgrammingLanguage.DoesNotExist:
		return None

def get_implementations_by_alg_id(a_id):
	try:
		alg = Algorithm.objects.get(id=a_id)
		implementations = Implementation.objects.filter(algorithm=alg)

		return implementations
		
	except Algorithm.DoesNotExist:
		return []

def try_create_algorithm_rdf(a_id):

	base_path = os.path.dirname(__file__)
	file_name = os.path.join(base_path, 'static/rdf/').replace('\\', '/')
	file_name = file_name+'rdf_alg_%i.xml' %a_id
	
	if not os.path.exists(file_name):	
		algorithm = get_algorithm_by_id(a_id)
		rdf_writer = RDFWriter(algorithm, file_name)
		
		rdf_name = rdf_writer.create_rdf_file()
		
		return rdf_name
	else:
		file_parts = file_name.split('/')
		file_name = '/'.join(file_parts[-2:])
		
	return file_name
		
def make_classification_link(c_id):
	#base_link = get_classification_display_url()
	#return base_link.replace("#", c_id)
	return ''

def make_algorithm_link(a_id):
	#base_link = get_algorithm_display_url()
	#return base_link.replace("#", c_id)
	return ''

def get_classification_display_url():
	return "http://localhost:8000/show/cat/id/#"
	
def get_algorithm_display_url():
	return "http://localhost:8000/show/alg/id/#"