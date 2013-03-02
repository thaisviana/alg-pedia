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