from django.shortcuts import render
from django.http import HttpResponse
from django.views import View, generic

class IndexView(View):
	def get(self, request, *args, **kwargs):
		return render(request, template_name='index.html', context=None)

class HomeView(View):
	template_name = "home.html"