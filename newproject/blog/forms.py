from django import forms
from blog.models import Post, Category, Tag

class PostForm(forms.ModelForm):
	class Meta:
		model = Post 
		fields = ['title','featured_image','content']

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ['title', 'content']

class TagForm(forms.ModelForm):
	class Meta:
		model = Tag
		fields = ['title', 'description']