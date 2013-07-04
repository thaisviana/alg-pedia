# Create your views here.
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template

from algorithm.models import Classification, Implementation,Algorithm, ProgrammingLanguage
from algorithm.controllers import *
#get_all_classifications_name_link, wipe_database, is_database_empty, get_classification_by_id
from extractor.Bootstrapping import Bootstrapper
from django.template import RequestContext
from algorithm.UserCreateForm import UserCreateForm
from algorithm.ContactForm import ContactForm
from algorithm.algorithmForm import AlgorithmForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, render
from django.core.mail import send_mail

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
		form =  UserCreateForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponse(get_template('default_debug.html').render(Context({'logged':  request.user.is_authenticated()})))
		else:
			c = {'logged':  request.user.is_authenticated(), 'form' : form}
			c.update(csrf(request))
			return render_to_response("accounts/signin.html", c)
	else:
		c = {'logged':  request.user.is_authenticated(), 'form' : UserCreateForm()}
		c.update(csrf(request))
		return render_to_response("accounts/signin.html", c)

def logout(request):
	auth.logout(request)
	return HttpResponse(get_template('default_debug.html').render(Context({'logged':  request.user.is_authenticated(),'logout': True})))

def about(request):
	return HttpResponse(get_template('about.html').render(Context({'logged':  request.user.is_authenticated()})))

def contact(request):
	if request.method == 'POST':
		print("Aqui")
		recipients = ['thaisnviana@gmail.com']
		print(request.POST['subject'])
		print(request.POST['message'])
		print(request.POST['sender'])
		print(recipients)
		try:
			send_mail(request.POST['subject'], request.POST['message'], request.POST['sender'], recipients, fail_silently=False)
		except BadHeaderError:
			return HttpResponse(get_template('about.html').render(Context({'logged':  request.user.is_authenticated()})))
		return HttpResponse(get_template('default_debug.html').render(Context({'logged':  request.user.is_authenticated()})))
	else:
		c = {'logged':  request.user.is_authenticated(), 'form' : ContactForm()}
		c.update(csrf(request))
		return render_to_response("contact.html", c)

@login_required
def profile(request):
	user_questions = get_all_userquestions()
	question_answers = []
	username = request.user.username
	classifications = get_all_classifications_name_link()
	programming_languages = get_all_programming_languages()
	
	for user_question in user_questions :
		question_answers.append({"q": user_question, "qa" : get_questionaswer_by_question_id(user_question.id), "u_qa": get_userquestionanswer_by_question_id_and_user(username, user_question.id)})
	
	u_c_p = get_user_classifications_proeficiencies_ids(username)
	u_c_i = get_user_classifications_interests_ids(username)
	u_p_l_p = get_user_programming_languages_proeficiencies_ids(username)
	
	print u_c_p
	
	if request.method == "POST":
		
		#insere as respostas para as perguntas
		for q in user_questions:
			q_data = request.POST["profile_" + str(q.id)]
			
			if q_data and q_data.isdigit():
				int_q_answer_id = int(q_data)
				insert_user_question_answer(username, q.id, int_q_answer_id)
		
		
		data = request.POST.getlist("classifications_interest")
		ids = []
		
		for classification_id in data:
			if classification_id.isdigit():
				int_c = int(classification_id)
				ids.append(int_c)
		
		#insere as classificacoes de interesse
		insert_classifications_interests(username, ids)
		
		data = request.POST.getlist("classifications_knowledge")
		ids = []
		
		for classification_id in data:
			if classification_id.isdigit():
				int_c = int(classification_id)
				ids.append(int_c)
		
		insert_classifications_proeficiencies(username, ids)
		
		data = request.POST.getlist("programming_languages")
		ids = []
		
		for programming_language_id in data:
			if programming_language_id.isdigit():
				int_c = int(programming_language_id)
				ids.append(int_c)
		
		insert_programming_languages_proeficiencies(username, ids)
	
	c = Context({
		'logged':  request.user.is_authenticated(),
		'name' : request.user.username,
		'question_answers' :  question_answers,
		'classifications' : classifications,
		'user_classifications_interests': u_c_i,
		'user_classification_proeficiencies' : u_c_p,
		'user_programming_languages_proeficiencies' : u_p_l_p,
		'programming_languages' : programming_languages,
		'questions': get_all_userquestions()})
	
	c.update(csrf(request))
	
	return HttpResponse(get_template('accounts/profile.html').render(c))

def rules(request):
	return HttpResponse(get_template('rules.html').render(Context({'logged':  request.user.is_authenticated()})))

def show_all_classifications(request):
	username = str(request.user) if request.user.is_authenticated() else None
	ordered_classifications = get_all_classifications_ordered_name_link(username)
	
	return render_to_response('display_all_classifications.html', {'classifications' : ordered_classifications,#get_all_classifications_name_link(), 
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

	if request.method == 'POST':
		algorithm = get_algorithm_by_id(int(request.POST['algorithm_id']))
		p_lang = get_programming_language_by_id(int(request.POST['programming_languages']))
		implementation =  insert_implementation_alg_p_lang(algorithm, p_lang, request.POST['algorithm_code'], False)
		return HttpResponseRedirect(algorithm.get_show_url())
	else:
		c = {'logged':  request.user.is_authenticated(),'programming_languages' : get_all_programming_languages(), 'algorithm' : get_algorithm_by_id(int(id))}
		c.update(csrf(request))
		return render_to_response("add_algorithm_implementation.html", c)
	
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
		algorithm = insert_algorithm(request.POST['name'], request.POST['description'], get_classification_by_id(int(request.POST['classification'])), False)
		return HttpResponseRedirect(algorithm.get_show_url())
	else:
		c = {'form' : AlgorithmForm(), 
		'classif' : get_classification_by_id(int(id)), 
		'programming_languages' : get_all_programming_languages(),
		'logged':  request.user.is_authenticated()}
		c.update(csrf(request))
		return render_to_response("add_algorithm.html", c)	