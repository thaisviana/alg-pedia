from algorithm.models import Classification, Implementation, Author, Algorithm, ProgrammingLanguage

def is_database_empty():
	empty = 0
	
	empty += Classification.objects.count()
	empty += Implementation.objects.count()
	empty += Author.objects.count()
	empty += Algorithm.objects.count()
	empty += ProgrammingLanguage.objects.count()
	
	return False if empty > 0 else True
	
def wipe_database():
	Author.objects.all().delete()
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
	return Classification.objects.get(id=c_id)

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
		
def insert_algorithm_db(a_name, a_about, a_classif):
	try:
		alg = Algorithm.objects.get(name=a_name)
		return alg
	except Algorithm.DoesNotExist:
		aux = Algorithm(name=a_name, description=a_about, classification=a_classif)
		aux.save()
		return aux
		
		
def get_algorithm_by_id(a_id):
	try:
		alg = Algorithm.objects.get(id=a_id)
		return alg
	except Algorithm.DoesNotExist:
		return None
		
def make_classification_link(c_id):
	base_link = get_classification_display_url()
	return base_link.replace("#", c_id)

def make_algorithm_link(a_id):
	base_link = get_algorithm_display_url()
	return base_link.replace("#", c_id)

def get_classification_display_url():
	return "http://localhost:8000/show/cat/id/#"
	
def get_algorithm_display_url():
	return "http://localhost:8000/show/alg/id/#"