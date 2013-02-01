# Django + Facebook Graph API authentication
This is a django app to use the new Graph API authentication with Django. It uses the standard authentication build into Django.

Make sure you read http://developers.facebook.com/docs/authentication/ to have an idea of how this is intended to work.

## Basic setup for example project
1. Go into `./example`
2. Set up the FACEBOOK_APP_ID and FACEBOOK_APP_SECRET to your Facebook app (Set one up at https://developers.facebook.com/apps)
3. Run `python manage.py syncdb`
4. Run `python manage.py runserver`
5. Go to http://localhost:8000 and login!

## settings.py
Here are the differences between a base Django settings.py and the ones needed for the example project to run:

    AUTHENTICATION_BACKENDS = ('facebook.backend.FacebookBackend', 'django.contrib.auth.backends.ModelBackend')
    AUTH_PROFILE_MODULE = 'facebook.FacebookProfile'
    FACEBOOK_APP_ID = os.environ['FACEBOOK_APP_ID']
    FACEBOOK_APP_SECRET = os.environ['FACEBOOK_APP_SECRET']
    FACEBOOK_SCOPE = 'email,publish_stream'
    INSTALLED_APPS = ['facebook']

## Contributions
I (ryanmark) added a couple features:
- When a user logs in successfully, he will get redirected to the url specified in the LOGIN_REDIRECT_URL setting.
- Can add an setup step for new facebook users.

### Adding a setup step
You can force a new facebook user to fill out a form or register for an account. To redirect the user to a setup page instead of automatically creating an account, add this to your setting.py:

    FACEBOOK_FORCE_SIGNUP = True

The new facebook user will be redirected to the url route named
'facebook_setup'. Your setup view should look something like this:

    def setup(request):
        # we need a code from facebook
        code = request.GET.get('code')

        #you need to be logged into facebook.
        user = authenticate(token=code, request=request)

        if request.method == "POST":
            # Process sign up form
            # django.contrib.auth.login and redirect if successful

        # Display sign up form

