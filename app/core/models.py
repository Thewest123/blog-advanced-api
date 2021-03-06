from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.contrib.gis.db import models as locationModels
from django.contrib.gis.geos import Point


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError("User must have an email adress!")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model, supports email instead of username, geolocation"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(blank=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    address = models.CharField(blank=True, max_length=255)
    location_point = locationModels.PointField(
        blank=True, null=False, geography=True, default=Point(0, 0))

    def lat(self):
        return self.location_point.y
    lat.short_description = "Latitude"

    def lng(self):
        return self.location_point.x
    lng.short_description = "Longitude"

    objects = UserManager()

    USERNAME_FIELD = 'email'
