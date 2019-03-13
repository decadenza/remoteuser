from django.contrib import admin
from django import forms # Forms validation
from django.contrib.auth.forms import UserCreationForm
from .models import RemoteUser, RemoteUserPassword, Grade
from django.contrib.auth.forms import ReadOnlyPasswordHashField


# User creation
class RemoteUserForm(forms.ModelForm):
    
    class Meta:
        model = RemoteUser
        fields = ('username','grade','first_name','last_name','email','has_write_permission','is_active','is_staff','is_superuser',)
    
    '''
    def clean_email(self):
        data = self.cleaned_data['email']
        if data: # Allow blank
            domain = data.split('@')[1]
            if domain.lower() != 'YOURDOMAIN.COM'.lower(): # Caseless comparison
                raise forms.ValidationError('Inserire email con dominio "YOURDOMAIN.COM".')
            else:
                return data
        else:
            return data
    '''
    
    def clean_username(self):
        return self.cleaned_data['username'].upper() # Force uppercase username
    
    
class RemoteUserAdmin(admin.ModelAdmin):
    
    form = RemoteUserForm
    list_display = ('username','grade','first_name','last_name','is_active','is_staff','is_superuser','has_write_permission','email','last_login',)  
    search_fields =  ('username','grade__grade_long','first_name','last_name','email',)
    
# Password change
class RemoteUserPasswordForm(UserCreationForm):
    
    class Meta:
        model = RemoteUserPassword
        fields = ('password',)
    
    password = ReadOnlyPasswordHashField(help_text='In caso di impostazione di una nuova password, sarà richiesto all\'utente di cambiarla al primo accesso.')
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RemoteUserPasswordForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        # Force SET password as expired (only good for first access)
        user.last_password_change = None
        
        if commit:
            user.save()
        return user    

class RemoteUserPasswordAdmin(admin.ModelAdmin):
    
    form = RemoteUserPasswordForm
    list_display = ('username','first_name','last_name','is_active','is_staff','is_superuser','password',)  
    search_fields =  ('username','first_name','last_name','email',)
    

# Grades
class GradeForm(forms.ModelForm):
    
    class Meta:
        model = Grade
        fields = ('grade_short','grade_long',)


class GradeAdmin(admin.ModelAdmin):
    
    form = GradeForm
    list_display =('grade_short','grade_long',)
    search_fields =('grade_short','grade_long',)

    
admin.site.register(RemoteUserPassword, RemoteUserPasswordAdmin)
admin.site.register(RemoteUser, RemoteUserAdmin)
admin.site.register(Grade, GradeAdmin)
