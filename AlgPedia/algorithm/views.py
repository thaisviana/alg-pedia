# Create your views here.

from django.http import HttpResponse

def showMainPage(request):
	html = "<html> Main Page </html>"
	
	return HttpResponse(html)
