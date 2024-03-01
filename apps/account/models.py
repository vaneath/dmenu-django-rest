from django.contrib.auth.models import (AbstractUser, BaseUserManager,
                                        PermissionsMixin, UserManager)
from django.db import models


class UserManagerDecorator(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('User must have an email address.')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
        


class UserDecorator(AbstractUser):
    GENDER_CHOICES = (
        (1, 'male'),
        (2, 'female'),
        (3, 'other'),
    )
    
    email = models.EmailField('email address', unique=True)
    gender = models.SmallIntegerField('gender', choices=GENDER_CHOICES, default=3)
    first_name = models.CharField('first name', max_length=150)
    last_name = models.CharField('last name', max_length=150,)

    objects = UserManagerDecorator()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'gender', 'first_name', 'last_name']

    def __str__(self):
        return self.email
