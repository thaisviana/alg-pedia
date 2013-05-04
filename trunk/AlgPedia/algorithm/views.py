# Create your views here.
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template

from algorithm.models import Classification, Implementation,Algorithm, ProgrammingLanguage
from algorithm.controllers import *
#get_all_classifications_name_link, wipe_database, is_database_empty, get_classification_by_id
from extractor.Bootstrapping import Bootstrapper
from django.template import RequestContext
from algorithm.userForm import UserForm
from algorithm.algorithmForm import AlgorithmForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response


def show_main_page(request):	
	return HttpResponse(get_template('default_debug.html').render(Context({'logged':  request.user.is_authenticated(),'message' : 'Welcome to AlgPedia - the free encyclopedia that anyone can edit.'})))

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
	

def signin(request):
	
	if request.method == 'POST':
		form =  UserForm(request.POST)
		print("post")
		if form.is_valid():
			new_user = form.save()
		c = dict(form=UserForm())
		c.update(csrf(request))
		return render_to_response("accounts/signin.html", c)
	else:
		c = dict(form=UserForm())
		c.update(csrf(request))
		return render_to_response("accounts/signin.html", c)


def logout(request):
	auth.logout(request)
	return HttpResponse(get_template('default_debug.html').render(Context({'logged':  request.user.is_authenticated(),'logout': True})))

def about(request):
	return HttpResponse(get_template('about.html').render(Context({'logged':  request.user.is_authenticated()})))

def contact(request):
	return HttpResponse(get_template('contact.html').render(Context({'logged':  request.user.is_authenticated()})))
	
@login_required
def profile(request):
	return HttpResponse(get_template('accounts/profile.html').render(Context({'logged':  request.user.is_authenticated()})))

def show_all_classifications(request):
	return render_to_response('display_all_classifications.html', {'classifications' : get_all_classifications_name_link(), 
	'logged':  request.user.is_authenticated()},context_instance=RequestContext(request))

def show_all_algorithms(request):
	algorithms = get_all_algorithms()
	ctx_variables = {}
	algs = [ (alg.get_show_url(), alg.name) for alg in algorithms]
	algorithms = [{'link' : a[0], 'name' : a[1]} for a in algs]
	ctx_variables['algorithms'] = algorithms
	ctx_variables['logged'] = request.user.is_authenticated()
	return HttpResponse(get_template('display_all_algorithms.html').render(Context(ctx_variables)))

def show_algorithm_by_id(request, id):
	alg = get_algorithm_by_id(int(id))
	
	classification = alg.classification
	
	# Try and create an rdf file for the required algorithm
	# returns the name of the file so we can show it later
	rdf_path = try_create_algorithm_rdf(int(id))
	
	ctx_variables = {}
	
	ctx_variables['algorithm_name'] = alg.name
	ctx_variables['algorithm_id'] = alg.id
	ctx_variables['algorithm_classification'] = classification.name
	ctx_variables['algorithm_about'] = alg.description
	ctx_variables['classification_algp_url'] = classification.get_show_url() 
	#make_classification_link(classification.id)
	ctx_variables['classification_dbp_url'] = classification.uri
	ctx_variables['rdf_path'] = rdf_path
	ctx_variables['implementations'] = get_implementations_by_alg_id(int(id))
	ctx_variables['logged'] = request.user.is_authenticated()
	
	return HttpResponse(get_template('display_algorithm_by_id.html').render(Context(ctx_variables)))

@login_required	
def display_add_implementation(request, id):
	return HttpResponse(get_template('add_algorithm_implementation.html').render(Context({'programming_languages' : get_all_programming_languages(), 'algorithm' : get_algorithm_by_id(int(id)),
	'logged':  request.user.is_authenticated()})))

@login_required
def add_implementation_by_algorithm(request, alg_id, lang_id, code):
	# adds an implementation to an algorithm and redirects to the alg display code
	
	alg = get_algorithm_by_id(int(alg_id))
	p_lang = get_programming_language_by_id(int(lang_id))
	
	implementation =  insert_implementation_alg_p_lang(alg, p_lang, code)	
	
	return HttpResponseRedirect(alg.get_show_url())
	
def show_classification_by_id(request, id):	
	classification = get_classification_by_id(int(id))
	algs = get_algorithms_by_classification(classification)
	algs_names = map(lambda alg: alg.name, algs)
	
	algs = [{'name' : t[0], 'link' : t[1]} for t in zip(algs_names, [get_algorithm_display_url().replace('#',str(id)) for id in map(lambda alg: alg.id, algs)])]
			
	return HttpResponse(get_template('display_classification.html').render(Context({'classif' : classification, 
	'algorithms' : algs,
	'logged':  request.user.is_authenticated()})))

@login_required
def display_add_algorithm(request, id):
	
	if request.method == 'POST':
		form =  AlgorithmForm(request.POST)
		algorithm = insert_algorithm(request.POST['name'], request.POST['description'], get_classification_by_id(int(request.POST['classification'])))
		return HttpResponseRedirect(algorithm.get_show_url())
	else:
		c = {'form' : AlgorithmForm(), 
		'classif' : get_classification_by_id(int(id)), 
		'programming_languages' : get_all_programming_languages(),
		'logged':  request.user.is_authenticated()}
		c.update(csrf(request))
		return render_to_response("add_algorithm.html", c)	