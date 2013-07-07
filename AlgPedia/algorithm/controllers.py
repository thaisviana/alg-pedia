import os
from algorithm.models import Classification, Implementation, Algorithm, ProgrammingLanguage, Interest, ProeficiencyScale, ProgrammingLanguageProeficiencyScale, ClassificationProeficiencyScale, Question,QuestionAnswer,UserQuestion,ImplementationQuestion,ImplementationQuestionAnswer,UserQuestionAnswer
from extractor.FileWriters import RDFWriter
from django.contrib.auth.models import User
from django.db import connection

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

#returns user interested classifications
def get_user_interested_classifications(username=None):
	if username == None:
		return []
	
	names = []
	links = []
	
	user = User.objects.get(username=username)
	user_interests = Interest.objects.filter(user=user).only("classification").order_by("classification__name")
	
	for interest in user_interests:
		names.append(interest.classification.name)
		links.append("http://localhost:8000/show/cat/id/" + str(interest.classification.id))
		#collection[classification.name] = "http://localhost:8000/show/cat/id/" + str(classification.id)
	
	classif = [{'name' : t[0], 'link' : t[1]} for t in zip(names, links)]
	
	return classif

#returns a tuple (names, links) of classifications
def get_all_classifications_name_link():
	#collection = dict()
	
	names = []
	links = []
	ids = []
	
	classifications = Classification.objects.order_by("name")
	
	for classification in classifications:
		names.append(classification.name)
		links.append("http://localhost:8000/show/cat/id/" + str(classification.id))
		ids.append(classification.id)
		#collection[classification.name] = "http://localhost:8000/show/cat/id/" + str(classification.id)
	
	classif = [{'name' : t[0], 'link' : t[1], 'id': t[2]} for t in zip(names, links, ids)]
	
	return classif
	
def get_all_classifications_ordered_name_link(username=None):
	all_classifications = get_all_classifications_name_link()
	user_interested_classifications = get_user_interested_classifications(username)
	#ordered_classifications = list(user_interested_classifications)
	ordered_classifications = []
	for classification in all_classifications:
		if classification not in ordered_classifications:
			ordered_classifications.append(classification)
			
	return ordered_classifications

# returns a	classification object
def get_classification_by_id(c_id):
	try:
		classification = Classification.objects.get(id=c_id)
		return classification
	except Classification.DoesNotExist:
		return []
		
# returns a	user question answer by question
def get_questionaswer_by_question_id(question_id):
	try:
		questionaswer = QuestionAnswer.objects.filter(question__id=question_id)
		return questionaswer
	except QuestionAnswer.DoesNotExist:
		return []

def get_userquestionanswer_by_question_id_and_user(username, question_id):
	try:
		user_question_answer = UserQuestionAnswer.objects.get(user__username=username, user_question__id=question_id)
		return user_question_answer.question_answer
	except:
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

def get_all_userquestions():
	return UserQuestion.objects.order_by("text")

def insert_user_question_answer(username, question_id, question_answer_id):
	user = User.objects.get(username=username)
	
	try:
		question = UserQuestion.objects.get(id=question_id)
		existing_question_answer = UserQuestionAnswer.objects.get(user=user, user_question=question)
		
		if question_answer_id and existing_question_answer.question_answer.id != question_answer_id:
				question_answer = QuestionAnswer.objects.get(id=question_answer_id)
				existing_question_answer.question_answer = question_answer
				existing_question_answer.save()
	except UserQuestionAnswer.DoesNotExist:
		question_answer = QuestionAnswer.objects.get(id=question_answer_id)
		UserQuestionAnswer.objects.create(user=user, user_question=question, question_answer=question_answer)

def delete_user_question_answer(username, question_id):
	try:
		existing_question_answer = UserQuestionAnswer.objects.get(user__username=username, user_question__id=question_id)
		existing_question_answer.delete()
	except UserQuestionAnswer.DoesNotExist:
		pass

def exec_sp_update_user_evaluation_contribution(implementation_id, user_id):
	cursor = connection.cursor()
	cursor.callproc('calculate_user_evaluation_contribution', (implementation_id, user_id))
	cursor.close()

def insert_user_impl_question_answer(username, impl_id, question_id, question_answer_id):
	user = User.objects.get(username=username)
	
	try:
		question = ImplementationQuestion.objects.get(id=question_id)
		existing_question_answer = ImplementationQuestionAnswer.objects.get(user=user, implementation__id=impl_id, implementation_question=question)
		
		if question_answer_id and existing_question_answer.question_answer.id != question_answer_id:
				question_answer = QuestionAnswer.objects.get(id=question_answer_id)
				existing_question_answer.question_answer = question_answer
				existing_question_answer.save()
	except ImplementationQuestionAnswer.DoesNotExist:
		implementation = Implementation.objects.get(id=impl_id)
		question_answer = QuestionAnswer.objects.get(id=question_answer_id)
		
		ImplementationQuestionAnswer.objects.create(user=user, implementation=implementation, implementation_question=question, question_answer=question_answer)
		
	exec_sp_update_user_evaluation_contribution(impl_id, user.id)

def get_user_programming_languages_proeficiencies_ids(username):
	try:
		pls = []
		
		for pl in ProgrammingLanguageProeficiencyScale.objects.filter(user__username=username).only("programming_language"):
			pls.append(pl.programming_language.id)
		
		return pls
	except ProgrammingLanguageProeficiencyScale.DoesNotExist:
		return []

def get_user_classifications_interests_ids(username):
	try:
		classifications = []
		
		for i in Interest.objects.filter(user__username=username).only("classification"):
			classifications.append(i.classification.id)
		
		return classifications
	except Interest.DoesNotExist:
		return []

def get_user_classifications_proeficiencies_ids(username):
	try:
		classifications = []
		
		for cps in ClassificationProeficiencyScale.objects.filter(user__username=username).only("classification"):
			classifications.append(cps.classification.id)
		
		return classifications
	except ClassificationProeficiencyScale.DoesNotExist:
		return []

def update_programming_languages_proeficiencies(username, programming_languages_ids):
	user_proeficiencies = set(get_user_programming_languages_proeficiencies_ids(username))
	programming_languages_ids = set(programming_languages_ids)
	
	#Vou remover todas as existentes menos as que ele selecionou
	to_remove = user_proeficiencies - programming_languages_ids
	to_insert = programming_languages_ids - user_proeficiencies
	
	ProgrammingLanguageProeficiencyScale.objects.filter(user__username=username, programming_language__id__in=to_remove).delete()
	
	#print "programming_language!"
	#print "to remove: ", to_remove
	#print "to_insert: ", to_insert
	
	if to_insert:
		insert_programming_languages_proeficiencies(username, to_insert)

def insert_programming_languages_proeficiencies(username, programming_languages_ids):
	user = User.objects.get(username=username)
	
	for programming_language_id in programming_languages_ids:
		programming_language = ProgrammingLanguage.objects.get(id=programming_language_id)
		ProgrammingLanguageProeficiencyScale.objects.get_or_create(user=user, programming_language=programming_language, value=1)

def update_classifications_proeficiencies(username, classifications_ids):
	user_proeficiencies = set(get_user_classifications_proeficiencies_ids(username))
	classifications_ids = set(classifications_ids)
	
	#Vou remover todas as existentes menos as que ele selecionou
	to_remove = user_proeficiencies - classifications_ids
	to_insert = classifications_ids - user_proeficiencies
	
	#print "proeficiencies!"
	#print "to remove: ", to_remove
	#print "to_insert: ", to_insert
	
	ClassificationProeficiencyScale.objects.filter(user__username=username, classification__id__in=to_remove).delete()
	
	if to_insert:
		insert_classifications_proeficiencies(username, to_insert)

def insert_classifications_proeficiencies(username, classifications_ids):
	user = User.objects.get(username=username)
	
	for classification_id in classifications_ids:
		classification = Classification.objects.get(id=classification_id)
		ClassificationProeficiencyScale.objects.get_or_create(user=user, classification=classification, value=1)

def update_classifications_interests(username, classifications_ids):
	user_interests = set(get_user_classifications_interests_ids(username))
	classifications_ids = set(classifications_ids)
	
	to_remove = user_interests - classifications_ids
	to_insert = classifications_ids - user_interests
	
	#print "interests!"
	#print "to remove: ", to_remove
	#print "to_insert: ", to_insert
	
	Interest.objects.filter(user__username=username, classification__id__in=to_remove).delete()
	
	if to_insert:
		insert_classifications_interests(username, to_insert)

def insert_classifications_interests(username, classifications_ids):
	user = User.objects.get(username=username)
	
	for classification_id in classifications_ids:
		classification = Classification.objects.get(id=classification_id)
		Interest.objects.get_or_create(user=user, classification=classification)

def get_all_implementationquestions():
	return ImplementationQuestion.objects.order_by("text")
	
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