from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from .models import RemoteUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from datetime import datetime
from django.http import HttpResponseForbidden
from .utils import passwordIsExpired


def login(request):
    if request.user.is_authenticated: # Session used
        return redirect(request.GET.get('next','/')) # NEXT PAGE OR HOME
    
    
    context = {
        'username': request.user.get_username(),
        'next': request.GET.get('next','/'), # Track next page...
        }
    
    # OFF INTRANET LOGIN
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        context['username'] = username
        user = authenticate(request,username=username,password=password)
        # user.check_password() checks if is valid, active and password is correct
        if user is not None and password and user.check_password(password):
            # Password change policy
            if passwordIsExpired(user) or not user.has_usable_password():
                messages.warning(request, 'La tua password è scaduta e deve essere cambiata.')
                request.POST = None # Remove old post data
                return change_password(request, user=user)
            else:
                login_auth(request, user, user.backend)
                return redirect(request.POST.get('next','/'))
        else:
            messages.error(request, 'Username o password non corretti!')
            return render(request, 'login.html', context) 
    
    # INTRANET LOGIN 
    else: # GET request
        # Try to authenticate with REMOTE_USER
        if authenticate(request):
            user = RemoteUser.objects.filter(username__iexact=username).first()
            if user is not None and user.is_active:
                login_auth(request, user, 'django.contrib.auth.backends.RemoteUserBackend')
                return redirect(request.GET.get('next','/'))
        return render(request, 'login.html', context)

        

@login_required
def logout(request):
    logout_auth(request)
    messages.success(request, 'Logout effettuato!')
    return redirect('remoteuser:login')
    



def change_password(request, user = None):
    context = {}
    
    if request.POST:
        user_id = request.POST.get('user')
        password = request.POST.get('password') # None if not set
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if user_id and password and password1 and password2:
            user = RemoteUser.objects.filter(id=user_id).first()
            context['user_id'] = user.id
            context['has_usable_password'] = user.has_usable_password() # At first access the password may be blank
        
            if password1 != password2:
                messages.error(request, 'Password non coincidenti!')
            elif not user.check_password(password):
                messages.error(request, 'Password non corretta!')
            elif password == password2:
                messages.error(request, 'La nuova password deve essere diversa dalla precedente!')
            else:
                try:
                    validate_password(password2) # None if password is valid, raise exception otherwise
                except exceptions.ValidationError as e:
                    for m in list(e.messages):
                        messages.error(request, m)
                else:
                    user.set_password(password2) # Set new password
                    user.last_password_change = datetime.now() # Update last password change
                    user.save() # Apply changes
                    messages.success(request,'Password cambiata correttamente.')
                    login_auth(request, user, 'django.contrib.auth.backends.ModelBackend') # Make user already logged in
                    return redirect("home")
                
        else:
            messages.error(request, 'Errore input. Riprova!')
    
    # GET request
    else:
        if user:
            pass
        elif request.user.is_authenticated:
            user = request.user
        else:
            return HttpResponseForbidden()
        
        context['user_id'] = user.id
        context['has_usable_password'] = user.has_usable_password() # At first access the password may be blank
    
    return render(request, 'change_password.html', context)


    
    
