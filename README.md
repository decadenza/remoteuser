# Django remoteuser app
"remoteuser" is a subclass of Django AbstractUser class. It allows Django to use single sign-on policies of Windows networks, based on REMOTE_USER meta data that comes with http requests.
You can manage the users using the classic Django admin views.

__Disclamer__
This is a application of a bigger project that I cannot share at the moment. I hope it may help somebody not to reinvent the wheel.

__ENGLISH__
Django user authentication using BOTH request.META['REMOTE_USER'] header (Windows single sign-on is based on this) AND allow classic username and password.

INSTALLATION:
1) Copy remoteuser folder into your Django project root directory.

2) Install the application inserting 'remoteuser.apps.RemoteUserConfig' into INSTALLED_APPS (see settings.py of your project).

3) Remaining in your project's settings.py, add this code (you can adapt it as you want):
```
# RemoteUser Login settings
AUTH_USER_MODEL = 'remoteuser.RemoteUser'
LOGIN_REDIRECT_URL = ""
LOGIN_URL = "/login"
PASSWORD_CHANGE_FREQUENCY = 7776000 # 90 days password change policy (set to False to deactivate)
```
4) Extra options:
- Set up an appropriate regex for your usernames in models.py, line 46
- Uncomment and adapt a restricted email policy in admin.py, line 15 and over (this app does not include user self registration)
- You can use the custom decorator *write_permission_required* in your views.



__ITALIAN__
Autenticazione utenti attraverso il dominio (usando header in request.META['REMOTE_USER']) E usando i classici username e password.

INSTALLAZIONE:

1) Copiare la cartella remoteuser nella cartella principale.

2) Installare l'applicazione inserendo 'remoteuser.apps.RemoteUserConfig' nella lista INSTALLED_APPS (vedi settings.py del tuo progetto).

3) Sempre in settings.py del progetto, il seguente codice (adattare a piacere):
```
# RemoteUser Login settings
AUTH_USER_MODEL = 'remoteuser.RemoteUser'
LOGIN_REDIRECT_URL = ""
LOGIN_URL = "/login"
PASSWORD_CHANGE_FREQUENCY = 7776000 # 90 days password change policy (set to False to deactivate)
```
4) Opzioni extra:
- Impostare una regex per gli username in models.py, riga 46
- Decommentare e adattare un vincolo per le email in admin.py, dalla riga 15 in poi (questa app non è pensata per consentire la registrazione autonoma degli utenti)
- Puoi usare il decorator personalizzato *write_permission_required* nelle tue views.
