from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass
    # @property
    # def upper_name(self):
    #     return self.username.upper()
    
    
