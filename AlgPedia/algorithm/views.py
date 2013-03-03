# Create your views here.

from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

from algorithm.models import Classification, Implementation, Author, Algorithm, ProgrammingLanguage
from algorithm.controllers import *
#get_all_classifications_name_link, wipe_database, is_database_empty, get_classification_by_id
from extractor.Bootstrapping import Bootstrapper

def show_main_page(request):
	html = "<html> Main Page </html>"
	
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
	
def show_classification_by_id(request, id):		
	classification = get_classification_by_id(int(id))
	
	t = get_template('display_classification.html')
	ctx = Context({'classif' : classification})
	html = t.render(ctx)
			
	return HttpResponse(html)
	
def add_by_category(request, id):		
	
	t = get_template('add_form.html')
	ctx = Context({'classif' : classification})
	html = t.render(ctx)
			
	return HttpResponse(html)