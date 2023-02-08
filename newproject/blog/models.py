import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMIntegerField, transition
from django.utils import timezone

# Create your models here.
class CrudConstrained(models.Model):
	date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
	date_updated = models.DateTimeField(_("Date updated"), auto_now=True)
	

	class Meta:
		abstract = True

def blog_media_path(instance, filename):
	if instance.__class__.__name__ is "Category":
		return "blog/category_{}/images/{}".format(instance.pk, filename)
	elif instance.__class__.__name__ is "Post":
		return "blog/post_{}/images/{}".format(instance.pk, filename)
	else:
		return "blog/images/{}".format(filename)

class Category(CrudConstrained):
	gid = models.UUIDField(max_length=32, unique=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=255, null=True, blank=True)
	slug = models.SlugField(max_length=200, unique=True)
	content = models.TextField(null=True, blank=True)
	cover_image = models.ImageField(upload_to=blog_media_path, blank=True, null=True)
	

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural = "Categories"
		ordering = ('title',)

	def _get_unique_slug(self):
		slug = slugify(self.title)
		unique_slug = slug
		num = 1
		while Category.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self._get_unique_slug()
		super(Category, self).save(*args, **kwargs)

class Tag(CrudConstrained):
	gid = models.UUIDField(max_length=32, unique=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=255, null=True, blank=True)
	slug = models.SlugField(max_length=200, unique=True)
	description = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural = "Tags"
		ordering = ('title',)

	def _get_unique_slug(self):
		slug = slugify(self.title)
		unique_slug = slug
		num = 1
		while Tag.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self._get_unique_slug()
		super(Tag, self).save(*args, **kwargs)

class PostManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(status='0')

class Post(CrudConstrained):
	SIMPLE = 0
	HTML = 1
	SIMPLE_IMAGE = 2
	GALLERY = 3
	VIDEO = 4
	POST_TYPE = (
		(SIMPLE, 'simple'),
		(HTML, 'html'),
		(SIMPLE_IMAGE, 'image'),
		(GALLERY, 'gallery'),
		(VIDEO, 'video'),
		)
	STATUS_CREATED = 0
	STATUS_DRAFT = 1
	STATUS_PUBLISHED = 2
	STATUS_UNPUBLISHED = 3 
	STATUS_CHOICES = (
		(STATUS_CREATED,'created'),
		(STATUS_DRAFT, 'draft'),
		(STATUS_PUBLISHED, 'published'),
		(STATUS_UNPUBLISHED, 'unpublished'),
		)
	gid = models.UUIDField(max_length=32, unique=True, default=uuid.uuid4, editable=False)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=255, null=True, blank=True)
	slug = models.SlugField(max_length=200, unique=True)
	featured_image = models.ImageField(upload_to=blog_media_path, blank=True, null=True)
	content = models.TextField(null=True, blank=True)
	post_category = models.ForeignKey(Category, blank=False, null=True, on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag, blank=True)
	published_date = models.DateTimeField(blank=True, null=True)
	post_type = FSMIntegerField(choices=POST_TYPE, default=HTML)
	status = FSMIntegerField(choices=STATUS_CHOICES, default=STATUS_CREATED, protected=True)
	

	objects = PostManager()
	

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural = "Posts"
		ordering = ('date_created',)

	@transition(field=status, source=STATUS_CREATED, target=STATUS_DRAFT)
	def draft(self):
		print('The post is in draft.')

	@transition(field=status, source=STATUS_DRAFT, target=STATUS_PUBLISHED)
	def publish(self):
		self.published_date = timezone.now()
		print('The post is published.')

	@transition(field=status, source=[STATUS_DRAFT,STATUS_PUBLISHED], target=STATUS_UNPUBLISHED)
	def unpublish(self):
		print('The post is unpublished.')

	def _get_unique_slug(self):
		slug = slugify(self.title)
		unique_slug = slug
		num = 1
		while Post.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self._get_unique_slug()
		super(Post, self).save(*args, **kwargs)

class Likes(models.Model):
	likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_like', null=True, blank=True)
	dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_dislike', null=True, blank=True)
	post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='post_like')

class Comment(CrudConstrained):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_user')
	comment = models.TextField(null=True, blank=True)

	def __str__(self):
		return str(self.user)

class PostComment(models.Model):	
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
	post_comment = models.ManyToManyField(Comment, related_name='post_comment')

	def __str__(self):
		return str(self.post)

class CommentLike(models.Model):
	comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name='comment_like')
	like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comment')
	dislike = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislike_comment')

