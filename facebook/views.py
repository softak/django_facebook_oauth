import urllib

from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render

def login(request):
    """ First step of process, redirects user to facebook, which redirects to authentication_callback. """
    
    redirect_uri = request.build_absolute_uri('/facebook/authentication_callback')
    redirect_args = {}
    if request.GET.get('next'):
        redirect_args['next'] = request.GET.get('next')            
    if request.GET.get('user'): 
        redirect_args['user'] = str(request.user.id)
        
    redirect_uri = redirect_uri + '?' + urllib.urlencode(redirect_args)
            
    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'scope': settings.FACEBOOK_SCOPE,
        'redirect_uri': redirect_uri,
        #'response_type': 'token'
    }
    return HttpResponseRedirect('https://www.facebook.com/dialog/oauth?' + urllib.urlencode(args))

def verification(request, template_name=None, authentication_form=None, redirect_url=None):
    code = request.GET.get('code')
    anonymous_user = authenticate(token=code, request=request)

    if request.method == 'POST':
        form = authentication_form(data=request.POST)
        if form.is_valid():
            verified_user = form.get_user()
            if anonymous_user.email == verified_user.email:
                verified_user.facebookprofile = anonymous_user.facebookprofile
                verified_user.facebookprofile.save()
                verified_user.save()
                
                auth_login(request, verified_user)
                
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

                return redirect(redirect_url) 
    else:
        form = authentication_form(anonymous_user=anonymous_user)

    request.session.set_test_cookie()
    return render(request, template_name, { 'form': form })


def authentication_callback(request):
    """ Second step of the login process.
    It reads in a code from Facebook, then redirects back to the home page. """
    code = request.GET.get('code')
    user = authenticate(token=code, request=request)
    
    if request.GET.get('user'):        
        url = reverse('profiles.notification_settings')
        
        if user is None:
            url += "?error=%s" % "Not Match Facebook User"
                        
        resp = HttpResponseRedirect(url)        
        return resp

    if user.is_anonymous():
        if user.verification_required:
            url = reverse('facebook_verification')
            url += "?code=%s" % code
            resp = HttpResponseRedirect(url)

        elif user.signup_required:
            url = reverse('facebook_setup')
            url += "?code=%s" % code
            resp = HttpResponseRedirect(url)

    else:
        auth_login(request, user)

        #figure out where to go after setup
        url = getattr(settings, "LOGIN_REDIRECT_URL", "/")

        resp = HttpResponseRedirect(url)
    
    return resp
