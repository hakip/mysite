from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

class IndexView(View):
	def get(self, request, *args, **kwargs):
		return render(request, template_name='home.html', context=None)