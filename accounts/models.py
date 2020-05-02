from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from questions.models import Question
from django.contrib.contenttypes.fields import GenericRelation
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
# from hitcount.models import HitCount, HitCountMixin


class User_data(models.Model):
	username = models.OneToOneField(User, on_delete = models.CASCADE)
	commented = models.IntegerField(default = 0)
	reputation = models.IntegerField(default = 0)
	verified = models.BooleanField(default = False)
	question = models.ManyToManyField(Question, blank = True)
	fav_question = models.ManyToManyField(Question, related_name='fav_question', blank = True)
	answers = models.IntegerField(default = 0)
	web_site = models.URLField(default = '', blank = True)
	github = models.URLField(default = '', blank =True)
	work_or_study = models.CharField(default = '', blank = True, max_length = 256)
	position = models.CharField(default = '', blank = True, max_length = 256)
	where = models.CharField(default = '', blank = True, max_length = 256)
	about = models.TextField(default = '', blank = True)
	image = models.ImageField(upload_to = 'profile_pic', default='default/profile_photo_default.jpg')

	def save(self):
		#Opening the uploaded image
		im = Image.open(self.image)

		output = BytesIO()
		w, h = im.size
		#Resize/modify the image
		if w > 1000 or h > 1000:
			if w >= h:
				d = w//1000
			else:
				d = h//1000
		else:
			d = 1
		im = im.resize((w//d, h//d))

		#after modifications, save it to the output
		im.save(output, format='JPEG', quality=100)
		output.seek(0)

		#change the imagefield value to be the newley modifed image value
		self.image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

		super(User_data,self).save()
	# hit_count_generic = GenericRelation(
 #        HitCount, object_id_field='object_pk',
 #        related_query_name='hit_count_generic_relation')

def create_profile(sender,**kwargs):
	if kwargs['created']:
		user_profile = User_data.objects.create(username = kwargs['instance'])

post_save.connect(create_profile,sender=User)

