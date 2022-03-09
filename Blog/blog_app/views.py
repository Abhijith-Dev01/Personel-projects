from django.contrib.auth.models import User
from django.shortcuts import render,get_object_or_404
from django.views.generic import (ListView,UpdateView,
								  DeleteView,DetailView,
								  CreateView)
from urllib3 import Retry
from .models import Posts
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

# Create your views here.
def home(request):
	context={
				'posts':Posts.objects.all()
			}
	return render(request,'blog_app/home.html',context)

def about(request):
	return render(request,'blog_app/about.html' ,{'title':'about'})
class PostListView(ListView):
	model = Posts
	template_name = 'blog_app/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 3

class UserPostListView(ListView):
	model = Posts
	template_name = 'blog_app/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 3

	def get_queryset(self):
		user = get_object_or_404(User,username=self.kwargs.get('username'))
		return Posts.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
	model = Posts
	
class PostCreateView(LoginRequiredMixin,CreateView):
	model  = Posts
	fields = ['title','content']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model  = Posts
	fields = ['title','content']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		
		return False


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Posts
	success_url = '/' 

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		
		return False