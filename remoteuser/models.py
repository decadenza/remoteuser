'''
2019 Pasquale Lafiosca
'''

from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, UserManager
from django import forms

# Allow case insensitive username
class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

 
class RemoteUser(AbstractUser):
    
    class Meta:
        verbose_name= 'Utente Remoto'
        verbose_name_plural = 'Utenti Remoti'
    
    # Custom fields
    has_write_permission = models.BooleanField(default=False,verbose_name='Permessi di scrittura')
    password = models.CharField(max_length=200, verbose_name='Password off intranet', help_text = 'La password è richiesta per accedere al di fuori della rete intranet.')
    last_password_change = models.DateTimeField(null=True, blank=True)
    grade = models.ForeignKey('Grade', on_delete=models.SET_NULL, blank=True, null=True, default=None, verbose_name='Grado')
    
    # Set custom user manager (defined above)
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    def fullName(self):
        name = ''
        if self.grade:
            name += str(self.grade)+' '
        if self.last_name:
            name += str(self.last_name)+' '
        if self.first_name:
            name += str(self.first_name)+' '
        name += '('+str(self.username)+')'
        return name
    
    # Override parent fields
    def __init__(self, *args, **kwargs):
        super(RemoteUser, self).__init__(*args, **kwargs)
        self._meta.get_field('username').validators = [RegexValidator(regex=r'^[A-Za-z0-9]+$',message='Username in formato non valido!')]
        self._meta.get_field('username').help_text = 'Username (es. utente123)'
        self._meta.get_field('password').help_text = 'La password è richiesta per accedere al di fuori della rete intranet.'
        self._meta.get_field('password').blank = True
        self._meta.get_field('first_name').blank = False
        self._meta.get_field('last_name').blank = False
        #self._meta.get_field('email').blank = False
    
        
#Proxy model for password change      
class RemoteUserPassword(RemoteUser):
    
    class Meta:
        proxy = True
        verbose_name= 'Gestione Password'
        verbose_name_plural = 'Gestione Password'
    

class Grade(models.Model):
    
    class Meta:
        verbose_name= 'Grado'
        verbose_name_plural = 'Gradi'
    
    grade_short = models.CharField(max_length=10, verbose_name='Grado (sigla)')
    grade_long = models.CharField(max_length=100, verbose_name='Grado (per esteso)')
    
    def __str__(self):
        return self.grade_short


    
