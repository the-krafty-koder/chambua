from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

# Create your models here.

class UsersManager(BaseUserManager):
    def create_user(self,name,email,institution_id,password):
        if not institution_id:
            raise ValueError( "Institution ID must be entered")

        user = self.model(
            name = name,
            email = self.normalize_email(email),
            institution_id = institution_id
        )

        user.set_password(password)
        user.save(using = self._db)
        return user


    def create_superuser(self,name,email,institution_id,password):
        user = self.create_user(
            name = name,
            email = email,
            institution_id = institution_id,
        )
        user.set_password(password)
        is_admin = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    name = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    institution_id = models.IntegerField()


    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UsersManager()
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['institution_id']

    def __str__(self):
        return  self.name

    @property
    def is_staff(self):
        return self.is_admin


