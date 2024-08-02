from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .helpers.profile import ProfileManager


# Create your views here.
@login_required
def profile(request):
    if request.method == "GET":
        return render(request, 'user_profile.html', context={'user': request.user})

    # if it is a POST:
    profile_mgr = ProfileManager(request)

    user = profile_mgr.update_the_user(password2=request.POST.get('password2'))

    if user:
        return render(request, 'user_profile.html',
                      context={'user': user,
                               'is_error_in_update': True})
    else:
        return render(request, 'user_profile.html',
                      context={'user': request.user,
                               'is_valid': profile_mgr.get_html_validation_dict})
