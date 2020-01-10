from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View, generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms
from .models import SignUpForm

class IndexView(View):
	def get(self, request, *args, **kwargs):
		return render(request, template_name='index.html', context=None)

class HomeView(LoginRequiredMixin, View):
	template_name = "home.html"
	def get(self, request, *args, **kwargs):
		print(request)
		num_visits = request.session.get('num_visits', 0)
		request.session['num_visits'] = num_visits + 1
		numcontext = {
			'count': num_visits,
		}
		return render(request, template_name='home.html', context=numcontext)
class RegisterView(View):
	def get(self, request, *args, **kwargs):
		form = SignUpForm()
		return render(request, 'registration/register.html', {'form': form})
	def post(self, request, *args, **kwargs):
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('home')
		else:
			return render(request, 'registration/register.html', {'form': form})