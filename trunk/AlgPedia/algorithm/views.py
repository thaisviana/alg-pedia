# Create your views here.

from django.http import HttpResponse
from algorithm.models import Classification
from extractor.Bootstrapping import Bootstrapper

def showMainPage(request):

	


	html = "<html> Main Page </html>"
	
	return HttpResponse(html)

def syncDatabase(request):
	boot_strapper = Bootstrapper()
	boot_strapper.doDatabaseImporting()
	
	return HttpResponse('Synched!')