import calendar

from django.db import models
from django.db.models import OneToOneField
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from sorl.thumbnail import get_thumbnail
from sorl.thumbnail import ImageField

import watson

from app.core.fields import UUIDField

# Create your models here.

class BaseModel(models.Model):
    """
    abstract model that holds common information for every model
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


def upload_to(instance, filename):
    """Create filepath for the image to be uploaded to"""
    return '%s/originals/%s' % (instance.user.id, slugify(filename))


class Photo(BaseModel):
    """
    holds user uploaded images.

    - Upload Photos to Profile
    - Set already-uploaded photo as Profile Picture
    """

    uuid = UUIDField(auto=True, db_index=True)
    user = models.ForeignKey('auth.User', related_name='profile_pictures')
    original_image = ImageField(upload_to=upload_to)
    original_filename = models.CharField(max_length=128, null=True)
    original_filesize = models.IntegerField(null=True) 
    profile_pic = models.BooleanField(default=False)


    def get_created(self):
        return calendar.timegm(self.created.timetuple()),

    def get_updated(self):
        return calendar.timegm(self.updated.timetuple()),

    def spec_160px(self):
        return self.thumbnail

    @property
    def thumbnail(self):
        return get_thumbnail(self.original_image, '160x160', crop='center')

    class Meta:
        db_table = 'photos'

    def __unicode__(self):
        return 'Photo: %s-%s' % (self.uuid, self.original_filename)


class UserProfile(models.Model):
    """
    - Personal "Profiles" where you can set information about yourself
    """

    user = models.OneToOneField('auth.User', related_name='user_profile')
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    work = models.CharField(max_length=100, blank=True, null=True)
    education = models.CharField(max_length=100, blank=True, null=True)

    @property
    def profile_picture(self):
        p_pic = self.user.profile_pictures.filter(profile_pic=True)

        if p_pic:
            return p_pic[0]
        return p_pic
        return 

    @property
    def is_filled_up(self):
        # return true if one of the field was already filled

        if self.address or self.phone or self.work or self.education:
            return True

        return False

    class Meta:
        db_table = 'user_profile'


    def __unicode__(self):
        return 'UserProfile: %s' % self.user.email


class WallItem(BaseModel):
    """
    - Post to your own Wall
    - Post to another profile's wall

    """
    uuid = UUIDField(auto=True, db_index=True, primary_key=True)
    receiver = models.ForeignKey('auth.User', related_name='wall_receiver')
    author = models.ForeignKey('auth.User', related_name='wall_author')
    content = models.TextField()


    class Meta:
        db_table = 'wall_posts'

    def __unicode__(self):
        return 'Wall: %s-%s' % (self.receiver.email, self.author.email)



watson.register(User)
watson.register(UserProfile)