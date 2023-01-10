from django.shortcuts import render, redirect
from blog.models import Post, Category, Tag
from django.conf import settings
from blog.forms import PostForm, CategoryForm, TagForm
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView 
from django.urls import reverse_lazy

# Create your views here.

class createPost(CreateView):
	form_class = PostForm
	template_name = 'post/create.html'	
	extra_context = {'categories':Category.objects.all(), 'tags':Tag.objects.all()}

	def form_valid(self, form):
		post = form.save(commit=False)
		post.author = self.request.user
		category_value = self.request.POST.get('category',None)
		if category_value :
			Category.objects.filter(title=category_value)
			post.post_category = Category.objects.filter(title=category_value)[0]
		else:
			category_value = self.request.POST['category1']
			if category_value:
				Category.objects.create(title=category_value)
				post.post_category = Category.objects.filter(title=category_value)[0]
		post.save()
		tag = self.request.POST['checkvalue']
		tags = tag.split(',')
		if '' in tags:
			tags.remove('')
		for tag in tags:
			if Tag.objects.filter(title=tag):
				post.tags.add(Tag.objects.filter(title=tag)[0])
			else:
				post.tags.create(title=tag)		
		return redirect('blog:post_list')

class listPost(ListView):
	model = Post
	template_name = 'post/list.html'
	context_object_name = 'post_list'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			context['post_list'] = Post.objects.filter(author=self.request.user)
		else:
			context['post_list'] = Post.objects.filter(status='2')
		return context


class allListPost(ListView):
	model = Post
	template_name = 'post/list.html'
	context_object_name = 'post_list'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context['post_list'] = Post.objects.filter(status='2')


class detailPost(DetailView):
	model = Post
	template_name = 'post/detail.html'
	context_object_name = 'post'

class updatePost(UpdateView):
	form_class = PostForm
	model = Post
	template_name = 'post/update.html'
	success_url = reverse_lazy('blog:post_list')
	extra_context = {'categories':Category.objects.all(), 'tags': Tag.objects.all()}

	def form_valid(self, form):
		post = form.save(commit=False)
		post.author = self.request.user
		category_value = self.request.POST.get('category', None)
		if category_value:
			post.post_category = Category.objects.filter(title=category_value)[0]
		else:
			category_value = self.request.POST('category1')
			Category.objects.create(title=category_value)
			post.post_category = Category.objects.filter(title=category_value)
		post.save()
		tag = self.request.POST['tag_value']
		tags = tag.split(',')
		if '' in tags:
			tags.remove('')
		for item in post.tags.all():
			if item not in tags:
				post.tags.remove(item)	
		for tag in tags:
			tag_value = Tag.objects.filter(title=tag)															
			if tag_value in post.tags.all():
				continue
			else:
				if tag_value:
					post.tags.add(tag_value[0])
				else:
					post.tags.create(title=tag)		
		return redirect('blog:post_list')



class deletePost(DeleteView):
	model = Post
	pk_url_kwarg = 'pk'
	template_name = 'post/delete.html'
	success_url = reverse_lazy('blog:post_list')
