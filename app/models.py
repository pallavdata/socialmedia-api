from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from uuid import uuid4
from django.db.models.signals import post_delete
from django.dispatch import receiver
# Create your models here.

class MyManager(BaseUserManager):
    def create_user(self,email,first_name,last_name,username,password=None):
        if not email:
            raise ValueError("User must have an eamil address")
        if not username:
            raise ValueError("User must have an username")
        if not first_name or not last_name:
            raise ValueError("User must have an first and last name")
        
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,first_name,last_name,username,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User_access(AbstractBaseUser):
    username = models.CharField(max_length=30,unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(verbose_name="email",max_length=255,unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login",auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=16,default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name',]

    objects = MyManager()

    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,perm,obj=None):
        return True

class Following_model(models.Model):
    accid = models.ForeignKey(User_access,on_delete=models.CASCADE,null=False)
    following = models.ForeignKey(User_access,on_delete=models.CASCADE, related_name='following',null=False)

class Post_model(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    image = models.ImageField(upload_to='post/',default="", null=True)
    accid = models.ForeignKey(User_access,on_delete=models.CASCADE,null=False)
    title = models.CharField(max_length=255,null=False)
    description = models.CharField(max_length=1280,null=False)
    created = models.DateTimeField(auto_now_add=True,null=False)

@receiver(post_delete, sender=Post_model)
def post_save_image(sender, instance, *args, **kwargs):
    try:
        instance.image.delete(save=False)
    except:
        pass

class Likes_model(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    accid = models.ForeignKey(User_access,on_delete=models.CASCADE,null=False)
    postid = models.ForeignKey(Post_model,on_delete=models.CASCADE,null=False)
    liked = models.BooleanField(default=False,null=False)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    accid = models.ForeignKey(User_access,on_delete=models.CASCADE,null=False)
    postid = models.ForeignKey(Post_model,on_delete=models.CASCADE, related_name='comments',null=False)
    comment = models.CharField(max_length=255,null=False)
