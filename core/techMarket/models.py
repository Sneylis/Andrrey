from django.db import models
from PIL import Image
from django.contrib.auth.models import User
# Create your models here.

class Unit(models.Model):
    title = models.CharField(max_length=2000)
    about = models.TextField()
    characters = models.TextField()
    price = models.IntegerField()
    photo = models.ImageField(upload_to='photo/')
    cat = models.ForeignKey('Category',on_delete=models.DO_NOTHING)

    def save(self):
        super().save()
        img = Image.open(self.photo.path)

        if img.height > 300 or img.width > 400:
            output_size = (300, 400)
            img.thumbnail(output_size)
            img.save(self.photo.path)

    def __str__(self):
        return self.title

class Category(models.Model):
    cat = models.CharField(max_length=20000)
    group = models.ForeignKey('Group',on_delete=models.CASCADE)
    def __str__(self):
        return self.cat

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Group(models.Model):
    gr = models.CharField(max_length=2000)

    def __str__(self):
        return self.gr


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/')
    birth = models.DateField(auto_created=True)

class UserQueston(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    unit = models.ForeignKey(Unit,on_delete=models.CASCADE)
    question = models.TextField()
    choice = models.CharField(max_length=100000,null=True)

