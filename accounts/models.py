from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


#Custom user model for SuperAdmin
class MyAccountManager(BaseUserManager):
    #This fxn for creating normal user
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('User must have an email addreess')

        if not username:
            raise ValueError('User must have username')

        user = self.model(
            #normalize will change the input capital words to all small words
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        #set_password inbuilt fxn top set the password
        user.set_password(password)
        user.save(using=self._db)
        return user

    #This fxn for creating super user
    def create_superuser(self,first_name,last_name,email,username,password):
        user = self.create_user(
            #normalize will change the input capital words to all small words
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name
        )        
        
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
        
#Custom user Model For Users
class Account(AbstractBaseUser):
    #Names
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)    
    #Contact
    email = models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=50)
    #Joined, Login session Date Time
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    #permission - mandatory when creating custom user model
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    #Main Field For Authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # class Meta: 
    #     ordering = ('-created_at', '-updated_at',)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=200)
    address_line_2 = models.CharField(blank=True, max_length=200)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')
    city = models.CharField(blank=True, max_length=50)
    state = models.CharField(blank=True, max_length=50)
    country = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.user.first_name 
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'