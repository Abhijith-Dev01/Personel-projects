from django.shortcuts import render
from .models import Posts

# Create your views here.
def home(request):
	return render(request,'blog_app/home.html',context={'posts':Posts.objects.all()})

def about(request):
	return render(request,'blog_app/about.html' ,{'title':'about'})