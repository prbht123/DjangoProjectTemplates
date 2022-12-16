import uuid
from django.db import models
from django_fsm import FSMIntegerField
from modules.contrib.ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.conf import settings



# Create your models here.
class Industry(models.Model):
	title = models.CharField(max_length=250, null=True, blank=True)

	def __str__(self):
		return self.title

class Organization(models.Model):
	"""
	Organization model description.
	"""
	WORLD_WIDE = 'WW'
	NATIONAL_WIDE = 'NW'
	STATE_WIDE = 'SW'
	AREA_SERVED = (
		(WORLD_WIDE, 'world wide'),
		(NATIONAL_WIDE, 'national wide'),
		(STATE_WIDE, 'state wide'),
		)
	PRIVATE_COMPANY = 'PRIVATE'
	PUBLIC_COMPANY = 'PUBLIC'
	GOVERNMENT_COMPANY = 'GOVERNMENT'
	FOREIGN_COMPANY = 'FOREIGN'
	CHARITABLE_COMPANY = 'CHARITABLE'
	COMPANY_OF_SHARES = 'SHARE'
	ONE_PERSON_COMPANY = 'ONE_OWNER'
	TYPE_CHOICE = (
		(PRIVATE_COMPANY, 'private'),
		(PUBLIC_COMPANY, 'public'),
		(GOVERNMENT_COMPANY, 'government'),
		(FOREIGN_COMPANY, 'foreign'),
		(CHARITABLE_COMPANY, 'charitable'),
		(COMPANY_OF_SHARES, 'shared'),
		(ONE_PERSON_COMPANY, 'one owner'),
		)
	name = models.CharField(max_length=250, null=True, blank=True)
	gid = models.UUIDField(max_length=32, unique=True, default=uuid.uuid4, editable=False)
	slug = models.SlugField(max_length=100, unique=True)
	website = models.CharField(max_length=250, unique=True)
	organization_type = models.CharField(max_length=50, choices=TYPE_CHOICE, default=PRIVATE_COMPANY, blank=True, null=True)
	founded = models.DateField(null=True)
	founder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organization_founder')
	headquarter = models.CharField(max_length=250, null=True, blank=True)
	industry = models.ManyToManyField(Industry, related_name='organization_industry')
	description = RichTextUploadingField(blank=True, null=True)
	area_served = models.CharField(max_length=50, choices=AREA_SERVED, default=STATE_WIDE, blank=True, null=True)
	image = models.ImageField(upload_to='auctions/organization',null=True, blank=True)
	created_at = models.DateTimeField(_('Date created'), auto_now_add=True)
	updated_at = models.DateTimeField(_('Date updated'), auto_now=True)
	deleted_at = models.DateTimeField(_('Date deleted'), auto_now=True)

	def __str__(self):
		return '{}:{}'.format(self.name, self.organization_type)

	class Meta:
		verbose_name_plural = 'Organizations'
		ordering = ('founded',)

	def _get_unique_slug(self):
		"""
		Generates unique slug for each organization instance.
		"""
		slug = slugify(self.name)
		unique_slug = slug
		num = 1
		while Organization.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num = num + 1
		return unique_slug

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self._get_unique_slug()
		super(Organization, self).save(*args, **kwargs)



