from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    lisence = models.PositiveBigIntegerField(null=True , blank=True , verbose_name='لایسنس')
    first_timer = models.BooleanField(default=True , null=True , blank=True)
    first_login = models.BooleanField(default=False , null=True , blank=True)


class Hesabha(models.Model):
    code_hesab = models.PositiveIntegerField(verbose_name='کد حساب کل' )
    name_hesab = models.CharField(max_length=200 )
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name_hesab

class Moein(models.Model):
    code_hesab = models.PositiveIntegerField(verbose_name='کد حساب معین')
    name_hesab = models.CharField(max_length=200 )
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    hesabha = models.ForeignKey(Hesabha , on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name_hesab

class tafsili(models.Model):
    code_hesab = models.PositiveIntegerField(verbose_name='کد حساب تفصیلی')
    name_hesab = models.CharField(max_length=200)
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    moein = models.ForeignKey(Moein , on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name_hesab

class GetToken(models.Model):
    TOKEN = models.CharField(max_length=200 , null=True , blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Category(models.Model):
    shomare_sanad = models.PositiveIntegerField(unique=True)
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE , null=True)
    date_create = models.DateTimeField(auto_now_add=True)   
    date_modify = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False , null=True , blank=True)  
    ai_sanad= models.BooleanField(default=False , blank=True , null=True)

    def __str__(self) -> str:
        return str(self.shomare_sanad)

class Asnad(models.Model):
    kol = models.CharField(max_length=200)
    moein = models.CharField(max_length=200)
    tafs = models.CharField(max_length=200)
    sharhe_hesab = models.CharField(max_length=200)
    bedehkar = models.PositiveBigIntegerField(blank=True , null=True)
    bestankar = models.PositiveBigIntegerField( blank=True , null=True)
    verified = models.BooleanField(default=False , null=True , blank=True)    
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE , null=True)
    category = models.ForeignKey(Category , on_delete=models.CASCADE , related_name='asnad')


    def __str__(self) -> str:
        return self.sharhe_hesab


class Docs(models.Model):
    doc_file = models.FileField(upload_to='docs/')
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)