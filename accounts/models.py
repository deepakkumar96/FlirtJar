# from __future__ import unicode_literals

from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from .managers import AccountManager
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from . import choices


class Account(AbstractBaseUser):

    # Fields

    email = models.EmailField(
        verbose_name='email address',
        max_length=100,
        unique=False
    )
    oauth_id = models.CharField(max_length=100, unique=True)

    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    gender = models.CharField(max_length=2, blank=True, choices=choices.USER_GENDER)
    dob = models.DateField(blank=True, null=True)
    phone_no = models.CharField(max_length=15, blank=True)
    tagline = models.TextField(max_length=200, blank=True)
    looking_for = models.CharField(max_length=2, choices=choices.USER_GENDER, blank=True)
    language = ArrayField(models.CharField(max_length=30, blank=True), blank=True, null=True)
    relationship_status = models.CharField(max_length=2, choices=choices.RELATIONSHIP_STATUS, blank=True)
    status = models.CharField(max_length=20, blank=True, choices=choices.STATUS)
    tags = ArrayField(models.CharField(max_length=50, blank=True), blank=True, null=True)  # Tags

    # Profile Information
    height = models.FloatField(blank=True, null=True)
    salary = models.FloatField(blank=True, null=True)
    country = models.CharField(max_length=30, blank=True)
    hair_color = models.CharField(max_length=4, choices=choices.HAIR_COLORS, blank=True)
    eye_color = models.CharField(max_length=4, choices=choices.EYE_COLORS, blank=True)
    occupation = models.CharField(max_length=40, blank=True)
    drink = models.NullBooleanField()
    smoking = models.NullBooleanField()
    weed = models.NullBooleanField()
    aquarius = models.CharField(max_length=4, blank=True, choices=choices.AQUARIUS)

    # profile_picture = models.ImageField(upload_to='profile_images', blank=True)
    profile_picture = models.CharField(max_length=300, blank=True)

    """"
    wallpaper = models.ImageField(
        upload_to='profile_wallpapers_images',
        blank=True
    ) """

    location = models.PointField(geography=True, null=True, blank=True)  # User's Current Location3

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    likes = models.IntegerField(default=0)
    skipped = models.IntegerField(default=0)
    superlikes = models.IntegerField(default=0)
    is_instagram_activated = models.BooleanField()

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'oauth_id'
    REQUIRED_FIELDS = []

    # Manager
    objects = AccountManager()
    gis = models.GeoManager()

    # Methods
    def __str__(self):
        return self.first_name + ' : ' + self.oauth_id

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def score(self):
        return (self.likes + (self.superlikes*2))

    @property
    def is_staff(self):
        return self.is_admin





