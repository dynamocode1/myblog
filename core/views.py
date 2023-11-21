from django.shortcuts import render,redirect,get_object_or_404
from django.views import generic
from .forms import *
from django.http import HttpResponse
from django.contrib.auth import login ,authenticate,logout
from .utils import UserMixin
from .models import Post
from .models import Profile as UserProfile
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.urls import reverse_lazy
class Home(UserMixin,generic.TemplateView):
	template_name = 'index.html'

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		post = Post.objects.order_by('-date')
		items_per_page = 6
		paginator = Paginator(post,items_per_page)
		page = self.request.GET.get('page',1)
		try:
			posts = paginator.page(page)
		except PageNotAnInteger:
			posts = paginator.page(1)
		except EmptyPage:
			posts = paginator.page(paginator.num_page)

		context['post'] = posts
		context['data'] = 'hello'
		return context

class UserSignIn(generic.View):
	template_name = 'signup.html'
	context = {}
	def get(self,request,*args,**kwargs):
		form = UserSiginForm()

		self.context['form'] = form

		return render(request,self.template_name,self.context)
	def post(self,request,*args,**kwargs):
		form = UserSiginForm(request.POST)
		self.context['form'] = form

		if form.is_valid():
			form.save()

			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username,password=password)
			if user:
				login(request,user)
				return redirect('home')


		return render(request,self.template_name,self.context)
class LoginUser(generic.View):
	template_name = 'login.html'
	context = {}
	def get(self,request,*args,**kwargs):
		form = UserLoginForm()
		self.context['form'] = form
		return render(request,self.template_name,self.context)
	def post(self,request,*args,**kwargs):
		form = UserLoginForm(request,request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request,user)
			return redirect('home')
		return render(request,self.template_name,self.context)


class Profile(UserMixin,generic.View):
	template_name = 'profile.html'
	context = {}
	def get(self,request,*args,**kwargs):
		user= request.user
		#user = UserProfile.objects.filter(user = user).first()
		posts  = request.user.profile.posts.all()
		items_per_page = 3
		paginator = Paginator(posts,items_per_page)
		page = self.request.GET.get('page',None)
		try:
			posts = paginator.page(page)
		except PageNotAnInteger:
			posts = paginator.page(1)
		except EmptyPage:
			posts = paginator.page(paginator.num_page)

		self.context['posts'] = posts
		self.context['user'] = user
		return render(request,self.template_name,self.context)




def logut_user(request):
	logout(request)
	return redirect('home')

class NewPost(UserMixin,generic.View):
	template_name = 'newpost.html'
	context = {}
	def get(self,request,*args,**kwargs):
		user = request.user
		form = NewPosts()
		print(form)

		self.context['username'] = user
		self.context['form'] = form

		return render(request,self.template_name,self.context)
	def post(self,request,*args,**kwargs):
		form = NewPosts(request.POST)
		#print(dir(form))

		if form.is_valid():
			post = form.save(commit = False)
			post.profile = request.user.profile
			post.save()

			return redirect('profile')
		return render(request,self.template_name,self.context)
class ReadMore(UserMixin,generic.TemplateView):
	template_name = 'readpost.html'
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		post_id = self.kwargs.get('id')
		post = Post.objects.get(id=post_id)
		context['post'] = post
		return context

class ViewProfile(UserMixin,generic.View):
	template_name = 'viewprofile.html'
	context = {}
	def get(self,request,*args,**kwargs):
		username = request.GET.get('user')
		user = User.objects.filter(username = username).first()

		self.context['user'] = user
		posts  = user.profile.posts.all()

		items_per_page = 3
		paginator = Paginator(posts,items_per_page)
		page = self.request.GET.get('page',None)
		print(page)
		try:
			posts = paginator.page(page)
		except PageNotAnInteger:
			posts = paginator.page(1)
		except EmptyPage:
			posts = paginator.page(paginator.num_page)

		self.context['posts'] = posts
		self.context['user'] = user

		return render(request,self.template_name,self.context)
def delete_post(request,id):
	post = Post.objects.get(id = id)
	if post.profile.user != request.user:
		return HttpResponse('This is not your post')
	else:
		post.delete()
		return redirect('profile')




class EditPost(UserMixin,generic.View):
	template_name = 'editpost.html'
	context = {}


	def get(self,request,id,*args,**kwargs):
		post = get_object_or_404(Post,pk = id)
		if post.profile.user != request.user:
			return HttpResponse('This is not your post')
		else:
		

			form = NewPosts(instance = post)
			self.context['form'] = form
			return render(request,self.template_name,self.context)
	def post(self,request,id,*args,**kwargs):
		post = get_object_or_404(Post,pk = id)
		form = NewPosts(request.POST,instance = post)
		self.context['form'] = form
		if form.is_valid():
			post = form.save()
			return redirect('profile')
		return render(request,self.template_name,self.context)
class EditProfile(UserMixin,generic.UpdateView):
	template_name = 'editprofile.html'
	model =  User
	form_class  = EditProfileForm
	success_url = reverse_lazy('profile')
	def get_object(self,queryset = None):
		return self.request.user.profile
	def form_valid(self,form):
		user= form.save(commit = False)
		user.save()
		profile = user
		profile.save()
		return super().form_valid(form)