from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.conf import settings
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from PIL import Image


USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username= username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user



class MyUser(AbstractBaseUser):
    username = models.CharField(
                max_length=120, 
                validators=[
                    RegexValidator(
                        regex = USERNAME_REGEX,
                        message = 'Username must be Alphanumeric or contain any of the following: " . @ + -"',
                        code = 'invalid_username'
                    )],
                unique=True
            )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    # photo = models.ImageField(upload_to='accounts', blank=True, default= "profilepic.jpg")
    photo = ResizedImageField(size=[300, 300], quality=75, upload_to="accounts/", force_format='WEBP', blank=True, default= "profilepic.jpg")
    date_naissance = models.DateField(blank=True, null=True)
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    signup_confirmation = models.BooleanField(default=False)

   
    def __str__(self):
        return str(self.user.username)

    def __unicode__(self):
        return str(self.user.username)


    def get_absolute_url(self):
        return reverse('accounts:create_profile')
    
    
@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)