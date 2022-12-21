import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django_fsm import FSMIntegerField, transition
from modules.contrib.ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Information(models.Model):
	created_at = models.DateTimeField(_('Date created'), auto_now_add=True)
	updated_at = models.DateTimeField(_('Date updated'), auto_now=True)
	deleted_at = models.DateTimeField(_('Date deleted'), auto_now=True)

	class Meta:
		abstract = True

class Category(Information):
	name = models.CharField(max_length=250, blank=True, null=True)

	def __str__(self):
		return self.name

class Tag(Information):
	name = models.CharField(max_length=250, blank=True, null=True)

	def __str__(self):
		return self.name

class Company(Information):
	name = models.CharField(max_length=250, blank=True, null=True)

	def __str__(self):
		return self.name

class Product(Information):
	"""
	Product model description.
	"""
	DRAFT = 0
	VERIFIED = 1 
	REJECTED = 2
	VERIFICATION = (
		(DRAFT, 'draft'),
		(VERIFIED, 'verified'),
		(REJECTED, 'rejected'),
		)
	gid = models.UUIDField(max_length=32, unique=True, default=uuid.uuid4, editable=False)
	slug = models.SlugField(max_length=100, unique=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	name = models.CharField(max_length=250, blank=True, null=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category', blank=True, null=True)
	company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='product_company', blank=True, null=True)
	image = models.ImageField(upload_to='inventory/', blank=True, null=True)
	tags = models.ManyToManyField(Tag, related_name='product_tags')
	price = models.FloatField(max_length=50, blank=True, null=True)
	manufacturing_date = models.DateField(blank=True, null=True)
	expiry_date = models.DateField(blank=True, null=True)
	quantity = models.IntegerField(blank=True, null=True)
	description = RichTextUploadingField(blank=True, null=True)
	iso_verification = FSMIntegerField(choices=VERIFICATION, default=DRAFT)
	
	
	class Meta:
		verbose_name_plural = 'Products'
		ordering = ('manufacturing_date',)

	def __str__(self):
		return self.name

	@transition(field=iso_verification, source=DRAFT, target=VERIFIED)
	def verify(self):
		print('The product is iso-verified.')

	@transition(field=iso_verification, source=DRAFT, target=REJECTED)
	def reject(self):
		print('The product is iso-rejected.')

	def _get_unique_slug(self):
		"""
		Generates unique slug for each product object.
		"""
		slug = slugify(self.name)
		unique_slug = slug
		num = 1 
		while Product.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num = num + 1
		return unique_slug

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self._get_unique_slug
		super(Product, self).save(*args, **kwargs)

