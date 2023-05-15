from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.query import QuerySet

from django.db.models.signals import post_save
from django.dispatch import receiver


class FullUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = (
            "ADMIN",
            "Admin",
        )
        STUDENT = (
            "STUDENT",
            "Student",
        )
        STAFF = (
            "STAFF",
            " Staff",
        )

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role

        return super().save(*args, **kwargs)
    

class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        resultat = super().get_queryset(*args, **kwargs)
        return resultat.filter(role=FullUser.Role.STUDENT)


class Student(FullUser):
    base_role = FullUser.Role.STUDENT

    student = StudentManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Bonjour Apprenant"
    

@receiver(post_save, sender=Student)

def create_user_profile(sender,instance,created, **kwargs):
    if created and instance.role=="STUDENT":
        StudentProfil.objects.create(user=instance)



class StudentProfil(models.Model):
    user = models.OneToOneField(FullUser, on_delete=models.CASCADE)
    student_id=models.IntegerField(null=True, blank=True)
    


class StaffManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        resultat = super().get_queryset(*args, **kwargs)
        return resultat.filter(role=FullUser.Role.STAFF)


class Staff(FullUser):
    base_role = FullUser.Role.STAFF

    staff = StaffManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Bonjour Professeur"
    

@receiver(post_save, sender=Staff)

def create_user_profile(sender,instance,created, **kwargs):
    if created and instance.role=="STAFF":
        StaffProfil.objects.create(user=instance)
        


class StaffProfil(models.Model):
    user = models.OneToOneField(FullUser, on_delete=models.CASCADE)
    staff_id=models.IntegerField(null=True, blank=True)    




class Produit(models.Model):

    nom = models.CharField(max_length = 150)
    libelle=models.TextField()
    date_ajout=models.DateField(auto_now=False, auto_now_add=True)
    # quantite=models.IntegerField()


