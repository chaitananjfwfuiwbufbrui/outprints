from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import datetime
import random
from django.conf import settings

# Get the custom user model
CustomUser = settings.AUTH_USER_MODEL

def unique_user_number(instance, new_id=None):
    ct = datetime.datetime.now().date()
    number = 1
    if new_id is not None:
        id = new_id
    else:
        id = f'f{ct}{number}'
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(user_id=id).exists()
    if qs_exists:
        new_id = f'f{ct}{number+1}{random.randrange(0, 100000)}'
        return unique_user_number(instance, new_id=new_id)
    return id

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        print(extra_fields)
        referral_code = extra_fields.get('referral_code')
        referred_user = self.model.objects.filter(user_id=referral_code).first()
        print(referred_user,referral_code)
        if referred_user:
            referred_user.referals.add(*referred_user.referals.all())
            
            # Add the referred user itself as a referral
            referred_user.referals.add(user)
            
            # Save the changes to the user's referrals
            referred_user.save()
            # Assuming you have access to the request object
            # request.session['referral_user_id'] = referred_user.id
        
        return user

ACCOUNT_TYPEE = (
    ("CONSULTANT", "consultant"),
    ("HR", "hr"),
    ("ACCOUNTANT", "accountant"),
    ("PROJECT MANAGER", "project manager"),
)
class UserAccount(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=255, default="S")
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    referals = models.ManyToManyField("self", verbose_name="referal")
    referral_code = models.CharField( max_length=50,default = "..")
    type_of_account = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPEE,  # Ensure ACCOUNT_TYPEE is defined
        default='CONSULTANT'
    )
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','referral_code']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email

def user_number_generator(sender, instance, *args, **kwargs):
    if instance.user_id:
        instance.user_id = unique_user_number(instance)

pre_save.connect(user_number_generator, sender=UserAccount)
