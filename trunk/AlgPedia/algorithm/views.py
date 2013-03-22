# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template

from algorithm.models import Classification, Implementation, Author, Algorithm, ProgrammingLanguage
from algorithm.controllers import *
#get_all_classifications_name_link, wipe_database, is_database_empty, get_classification_by_id
from extractor.Bootstrapping import Bootstrapper

def show_main_page(request):	
	t = get_template('default_debug.html')
	ctx = Context({'message' : 'Welcome to AlgPedia - the free encyclopedia that anyone can edit.', 'text':'OI'})
	html = t.render(ctx)
			
	return HttpResponse(html)

def sync_database(request):
	sync_message = ''
	# do this check for all the 
	if(is_database_empty()):
		boot_strapper = Bootstrapper()
		boot_strapper.doDatabaseImporting()
		sync_message = 'Synched!'
	else:
		sync_message = 'Nothing to synch here!'
	
	
	t = get_template('default_debug.html')
	ctx = Context({'message' : sync_message})
	html = t.render(ctx)
			
	return HttpResponse(html)
		
def clear_database(request):
	wipe_database()
	
	t = get_template('default_debug.html')
	ctx = Context({'message' : 'Database Clean!'})
	html = t.render(ctx)
			
	return HttpResponse(html)
	
def show_all_classifications(request):
	classifications = get_all_classifications_name_link()
	
	t = get_template('display_all_classifications.html')
	ctx = Context({'classifications' : classifications})
	html = t.render(ctx)
			
	return HttpResponse(html)

def show_all_algorithms(request):
	algorithms = get_all_algorithms()
	
	t = get_template('display_all_algorithms.html')
	
	ctx_variables = {}
	
	algs = [ (alg.get_show_url(), alg.name) for alg in algorithms]
	
	
	algorithms = [{'link' : a[0], 'name' : a[1]} for a in algs]
	
	ctx_variables['algorithms'] = algorithms
	
	ctx = Context(ctx_variables)
	
	html = t.render(ctx)
	
	return HttpResponse(html)
	
def show_algorithm_by_id(request, id):
	alg = get_algorithm_by_id(int(id))
	
	classification = alg.classification
	implementations = get_implementations_by_alg_id(int(id))
	
	# Try and create an rdf file for the required algorithm
	# returns the name of the file so we can show it later
	rdf_path = try_create_algorithm_rdf(int(id))
	
	
	t = get_template('display_algorithm_by_id.html')
	
	ctx_variables = {}
	
	ctx_variables['algorithm_name'] = alg.name
	ctx_variables['algorithm_id'] = alg.id
	ctx_variables['algorithm_classification'] = classification.name
	ctx_variables['algorithm_about'] = alg.description
	ctx_variables['classification_algp_url'] = classification.get_show_url() 
	#make_classification_link(classification.id)
	ctx_variables['classification_dbp_url'] = classification.uri
	ctx_variables['rdf_path'] = rdf_path
	
	
	
	
	
	ctx_variables['implementations'] = implementations
	
	ctx = Context(ctx_variables)
	
	html = t.render(ctx)
	
	
			
	return HttpResponse(html)
	
def display_add_implementation(request, id):
	t = get_template('add_algorithm_implementation.html')
	p_langs = get_all_programming_languages()
	alg = get_algorithm_by_id(int(id))
	ctx = Context({'programming_languages' : p_langs, 'algorithm' : alg})
	html = t.render(ctx)
	return HttpResponse(html)
	
def add_implementation_by_algorithm(request, alg_id, lang_id, code):
	# adds an implementation to an algorithm and redirects to the alg display code
	
	alg = get_algorithm_by_id(int(alg_id))
	p_lang = get_programming_language_by_id(int(lang_id))
	
	implementation =  insert_implementation_alg_p_lang(alg, p_lang, code)	
	
	return HttpResponseRedirect(alg.get_show_url())
	
	
def show_classification_by_id(request, id):		
	classification = get_classification_by_id(int(id))
	
	algs = get_algorithms_by_classification(classification)
	
	alg_display_url = get_algorithm_display_url()
	
	
	ids = map(lambda alg: alg.id, algs)
	algs = map(lambda alg: alg.name, algs)
	
	urls = [alg_display_url.replace('#',str(id)) for id in ids]
	
	
	algs = [{'name' : t[0], 'link' : t[1]} for t in zip(algs, urls)]
	
	t = get_template('display_classification.html')
	ctx = Context({'classif' : classification, 'algorithms' : algs})
	html = t.render(ctx)
			
	return HttpResponse(html)


def display_add_algorithm(request, id):		
	classification = get_classification_by_id(int(id))
	programming_languages = get_all_programming_languages()	
	t = get_template('add_algorithm.html')
	ctx = Context({'classif' : classification, 'programming_languages' : programming_languages})
	html = t.render(ctx)
			
	return HttpResponse(html)
	
	
def add_algorithm_by_category(request, id, alg_name, author_name, alg_about):

	#redirect to show alg by id
	
	alg_author = insert_author_by_name(author_name)
	
	alg_classification = get_classification_by_id(int(id))
	
	algorithm = insert_algorithm_with_author(alg_name, alg_about, alg_author, alg_classification)
	
	return HttpResponseRedirect(algorithm.get_show_url())
	
	