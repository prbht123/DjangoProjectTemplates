from django.shortcuts import render, redirect
from blog.models import Post, Category, Tag, Likes, PostComment, Comment, CommentLike
from django.conf import settings
from blog.forms import PostForm, CategoryForm, TagForm
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView 
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect


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
			category = Category.objects.filter(title=category_value)
			post.post_category = category[0]
		else:
			category_value = self.request.POST['category1']
			if category_value in Category.objects.all():
				category = Category.objects.filter(title=category_value)
				post.post_category = category[0]
			if category_value not in Category.objects.all():
				new_category = Category.objects.create(title=category_value)
				post.post_category = new_category
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
			context['post_list'] = Post.objects.filter(status='0')
		else:
			context['post_list'] = Post.objects.filter(status='0')
		return context


class allListPost(ListView):
	model = Post
	template_name = 'post/list.html'
	context_object_name = 'post_list'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context['post_list'] = Post.objects.filter(status='2')	
		return context


class detailPost(DetailView):
	model = Post
	template_name = 'post/detail.html'
	context_object_name = 'post'
	
	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		post = self.get_object()
		liked_post = Likes.objects.filter(post=post)
		if liked_post:
			context['all_liked_user'] = liked_post[0].likes.all()
			context['all_disliked_user'] = liked_post[0].dislikes.all()
			context['total_likes'] = liked_post[0].likes.all().count()
			context['total_dislikes'] = liked_post[0].dislikes.all().count()
		else:
			context['total_likes'] = '0'
			context['total_dislikes'] = '0'
		commented_post = PostComment.objects.filter(post=post)
		if commented_post:
			context['comments'] = commented_post[0].post_comment.all()
			context['total_comments'] = commented_post[0].post_comment.all().count()
		else:
			context['total_comments'] = '0'
		if commented_post:
			for comment in commented_post[0].post_comment.all():
				liked_comment = CommentLike.objects.filter(comment=comment)
				if liked_comment:
					context['comment_all_likes'] = liked_comment[0].like.all()
					context['comment_all_dislikes'] = liked_comment[0].dislike.all()
					context['total_comment_likes'] = liked_comment[0].like.all().count()
					context['total_comment_dislikes'] = liked_comment[0].dislike.all().count()
				else:
					context['total_comment_likes'] = '0'
					context['total_comment_dislikes'] = '0'		
		return context		
	

class updatePost(UpdateView):
	form_class = PostForm
	model = Post
	template_name = 'post/update.html'
	success_url = reverse_lazy('blog:post_list')
	extra_context = {'categories':Category.objects.all(), 'tags': Tag.objects.all()}

	def form_valid(self, form):
		post = form.save(commit=False)
		post.author = self.request.user
		category_value = self.request.POST['category1']
		if category_value:
			if category_value in Category.objects.all():
				category = Category.objects.filter(title=category_value)
				post.post_category = category[0]
			if category_value not in Category.objects.all():
				new_category = Category.objects.create(title=category_value)
				post.post_category = new_category							
		else:
			category_value = self.request.POST.get('category', None)
			category = Category.objects.filter(title=category_value)
			post.post_category = category[0]
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

def Like(request, pk):
	post = get_object_or_404(Post, id=pk)
	liked_post = Likes.objects.filter(post=post)
	if liked_post:
		if 'post_like' in request.POST:
			if request.user in liked_post[0].likes.all():
				liked_post[0].likes.remove(request.user)
			else:
				if request.user in liked_post[0].dislikes.all():
					liked_post[0].dislikes.remove(request.user)
				liked_post[0].likes.add(request.user)
		if 'post_dislike' in request.POST:
			if request.user in liked_post[0].dislikes.all():
				liked_post[0].dislikes.remove(request.user)
			else:
				if request.user in liked_post[0].likes.all():
					liked_post[0].likes.remove(request.user)
				liked_post[0].dislikes.add(request.user)
	else:
		new_post_liked = Likes.objects.create(post=post)
		if 'post_like' in request.POST:
			new_post_liked.likes.add(request.user)
		if 'post_dislike' in request.POST:
			new_post_liked.dislikes.add(request.user)
	return redirect('blog:post_detail', pk=pk)


def post_Comment(request, pk):
	post = get_object_or_404(Post, id=pk)
	commented_post = PostComment.objects.filter(post=post)
	if commented_post:
		commented_post[0].post_comment.create(user=request.user, comment=request.POST.get('comment'))
	else:
		new_commented_post = PostComment.objects.create(post=post)
		new_commented_post.post_comment.create(user=request.user, comment=request.POST.get('comment'))
	return redirect('blog:post_detail', pk=pk)

def commentLike(request, pk):
	comment_got = get_object_or_404(Comment, id=pk)
	liked_comment = CommentLike.objects.filter(comment=comment_got)
	if liked_comment:
		if 'comment_like' in request.POST:
			if request.user in liked_comment[0].like.all():
				liked_comment[0].like.remove(request.user)
			else:
				if request.user in liked_comment[0].dislike.all():
					liked_comment[0].dislike.remove(request.user)
				liked_comment[0].like.add(request.user)
		if 'comment_dislike' in request.POST:
			if request.user in liked_comment[0].dislike.all():
				liked_comment[0].dislike.remove(request.user)
			else:
				if request.user in liked_comment[0].like.all():
					liked_comment[0].like.remove(request.user)
				liked_comment[0].dislike.add(request.user)
	else:
		new_comment_liked = CommentLike.objects.create(comment=comment_got)
		if 'comment_like' in request.POST:
			new_comment_liked.like.add(request.user)
		if 'comment_dislike' in request.POST:
			new_comment_liked.dislike.add(request.user)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




