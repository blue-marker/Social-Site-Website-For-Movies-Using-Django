from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    
    #python manage.py createuser
# during the creation of new user in the admin
# this function is executed to create user
 

    def create_user(self, email, mobile, full_name, password=None,  is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not mobile:
            raise ValueError("Users must have a mobile number")
        if not full_name:
            raise ValueError("Users must have a full name")

        user_obj = self.model(
            email = self.normalize_email(email)
        ) #unsaved object
    # Normalizes email addresses by lowercasing the domain portion of the email address.

# self.model acts as a constructor which translates to "user = User(email = self.normalize_email(email))" 

# What we defined here is a UserManager class. This inherits from the BaseUserManager class which is a subclass of the Manager class. You actually use manager all the time. For example SomeModel.objects is a manager.

# A manager, if it is used,has a reference to the model it manages. So SomeModel.objects is a manager, but that manager has an attribute .model that actually refers back to the SomeModel class. 
# here 'User' is that 'SomeModel' class.
# in short self.model acts as a constructor to which we have passed an email attribute,
# and we get an unsaved User object which is saved in 'user_obj' variable

    

        user_obj.set_password(password) # change users password, i.e in a hashed form
# Sets the user’s password to the given raw string, taking care of the password hashing. Doesn’t save the AbstractBaseUser object.
# When the raw_password is None, the password will be set to an unusable password, as if set_unusable_password() were used.
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.mobile = mobile
        user_obj.full_name = full_name
        user_obj.save(using=self._db)

        return user_obj

    #python manage.py createstaffuser
#when the above command is used below function gets executed
    def create_staffuser(self, email, mobile, full_name, password=None):
        user = self.create_user(
                email=email,
                password=password,
                mobile=mobile,
                full_name=full_name,
                is_staff=True
        )
        return user

    #python manage.py createsuperuser
#when the above command is used below function gets executed
    def create_superuser(self, email, mobile, full_name, password=None):
        user = self.create_user(
                email=email,
                password=password,
                mobile=mobile,
                full_name = full_name,
                is_staff=True,
                is_admin=True
        )
        return user


# Instead of referring to User directly, you should reference the user model using django.contrib.auth.get_user_model(). This method will return the currently active user model – the custom user model if one is specified, or User otherwise.
class User(AbstractBaseUser):
    email       = models.EmailField( max_length=255, unique=True )
    full_name   = models.CharField( max_length=120 )
    mobile      = models.BigIntegerField()
    active      = models.BooleanField( default=True ) # can login 
    staff       = models.BooleanField( default=False ) # staff user non superuser
    admin       = models.BooleanField( default=False ) # superuser 
    timestamp   = models.DateTimeField( auto_now_add=True )

    USERNAME_FIELD  = 'email'
# A string describing the name of the field on the user model that is used as the unique identifier. This will usually be a username of some kind, but it can also be an email address, or any other unique identifier. The field must be unique (i.e., have unique=True set in its definition), unless you use a custom authentication backend that can support non-unique usernames.

    REQUIRED_FIELDS = ['full_name','mobile']
# A list of the field names that will be prompted for when creating a user via the createsuperuser management command. The user will be prompted to supply a value for each of these fields. It must include any field for which blank is False or undefined and may include additional fields you want prompted for when a user is created interactively.
# REQUIRED_FIELDS has no effect in other parts of Django, like creating a user in the admin.

# Note: REQUIRED_FIELDS must contain all required fields on your user model, but should not contain the USERNAME_FIELD or password " as these fields will always be prompted for. "


    objects = UserManager()
    
    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name
# Optional. A longer formal identifier for the user such as their full name. If implemented, this appears alongside the username in an object’s history in django.contrib.admin.


    def get_short_name(self):
        return self.email
# Optional. A short, informal identifier for the user such as their first name. If implemented, this replaces the username in the greeting to the user in the header of django.contrib.admin.

    @property
    def is_staff(self):
        "This will perform get of staff"
        return self.staff

    @property
    def is_admin(self):
        "This will perform get of admin"
        return self.admin

    @property
    def is_active(self):
        "This will perform get of admin"
        return self.active

    def has_perm(self, perm, obj=None):
        return True
# Returns True if the user has the named permission. If obj is provided, the permission needs to be checked against a specific object instance.
# Returns False if the user is not "is_active"

    def has_module_perms(self, app_label):
        return True
# Returns True if the user has permission to access models in the given app.
# Returns False if the user is not "is_active."





