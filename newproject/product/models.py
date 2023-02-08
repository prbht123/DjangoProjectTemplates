import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMIntegerField, transition
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class CrudConstrained(models.Model):
	created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
	updated_at = models.DateTimeField(_("Date updated"), auto_now=True)

	class Meta:
		abstract = True

class Company(CrudConstrained):
	gid = models.UUIDField(max_length=32, unique=True, default=uuid.uuid4, editable=False)
	slug = models.SlugField(max_length=100, unique=True)
	name = models.CharField(max_length=244, null=True, blank=True)
	description = models.TextField(blank=True, null=True)

	class Meta:
		verbose_name_plural = 'Companies'
		ordering = ('name',)

	def __str__(self):
		return self.name

	def _get_unique_slug(self):
		slug = slugify(self.name)
		unique_slug = slug
		num = 1
		while Company.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self._get_unique_slug()
		super(Company, self).save(*args, **kwargs)

class Category(CrudConstrained):
	gid = models.UUIDField(max_length=32, unique=True, default=uuid.uuid4, editable=False)
	slug = models.SlugField(max_length=100, unique=True)
	name = models.CharField(max_length=244, null=True, blank=True)
	description = models.TextField(blank=True, null=True)

	class Meta:
		verbose_name_plural = 'Categories'
		ordering = ('name',)

	def __str__(self):
		return self.name 

	def _get_unique_slug(self):
		slug = slugify(self.name)
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
	slug = models.SlugField(max_length=100, unique=True)
	name = models.CharField(max_length=244, null=True, blank=True)
	description = models.TextField(blank=True, null=True)

	class Meta:
		verbose_name_plural = 'Tags'
		ordering = ('name',)

	def __str__(self):
		return self.name

	def _get_unique_slug(self):
		slug = slugify(self.name)
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

class Product(CrudConstrained):
	DRAFT = 0
	VERIFIED = 1
	REJECTED = 2
	STATUS = (
		(DRAFT,'draft'),
		(VERIFIED, 'verified'),
		(REJECTED, 'rejected'),
		)
	gid = models.UUIDField(max_length=32, unique=True, default=uuid.uuid4, editable=False)
	slug = models.SlugField(max_length=100, unique=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_author')
	name = models.CharField(max_length=250, null=True, blank=True)
	price = models.FloatField(blank=True, null=True)
	company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='product_company')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
	tags = models.ManyToManyField(Tag, related_name='product_tags')
	manufacturing_date = models.DateField(blank=True, null=True)
	expiry_date = models.DateField(blank=True, null=True)
	image = models.ImageField(upload_to='product_images/', blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	iso_verification_status = FSMIntegerField(choices=STATUS, default= DRAFT)

	class Meta:
		verbose_name_plural = "Products"
		ordering = ('name',)

	def __str__(self):
		return self.name

	def _get_unique_slug(self):
		slug = slugify(self.name)
		unique_slug = slug
		num = 1
		while Product.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self._get_unique_slug()
		super(Product, self).save(*args, **kwargs)

class Address(models.Model):
	HOME = 'Home'
	WORK = 'Work'
	ADDRESS_TYPE = (
		(HOME, 'home'),
		(WORK, 'work'),
		)
	house_no = models.CharField(max_length=255, null=True, blank=True)
	street = models.CharField(max_length=255, null=True, blank=True)
	area = models.CharField(max_length=255, null=True, blank=True)
	zipcode = models.IntegerField(null=True, blank=True)
	city = models.CharField(max_length=244, null=True, blank=True)
	state = models.CharField(max_length=244, null=True, blank=True)
	country = models.CharField(max_length=244, null=True, blank=True)
	address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE, default=HOME)


class Stock(CrudConstrained):
	gid = models.UUIDField(max_length=32, unique=True, default=uuid.uuid4, editable=False)
	slug = models.SlugField(max_length=100, unique=True)
	company = models.ForeignKey(Company, on_delete=models.CASCADE)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField(blank=True, null=True)
	address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
	image = models.ImageField(upload_to='stock_images', null=True, blank=True)

	def __str__(self):
		return self.company.name

	def _get_unique_slug(self):
		slug = slugify(self.company.name)
		unique_slug = slug
		num = 1
		while Stock.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self._get_unique_slug()
		super(Stock, self).save(*args, **kwargs)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_customer_profile(sender, instance, **kwargs):
    instance.customer.save()

class Customer(CrudConstrained):
	MALE = 'M'
	FEMALE = 'F'
	GENDER_CHOICE = (
		(MALE, 'male'),
		(FEMALE, 'female'),
		)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')
	name = models.CharField(max_length=244, null=True, blank=True)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICE, default='M')
	email = models.CharField(max_length=250, null=True, blank=True)
	contact_no = models.IntegerField(null=True, blank=True)
	address = models.ManyToManyField(Address, related_name='customer_address')
	image = models.ImageField(upload_to='customer_profile_pictures/', blank=True, null=True)
	def __str__(self):
		return self.user.username

class Cart(CrudConstrained):
	customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
	product = models.ManyToManyField(Product, related_name='carted_products')







