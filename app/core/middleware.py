import logging
import time

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from app.core.models import UserProfile
from app.core.views import UpdateProfileFormView


class ForceUserProfile:
    """
    Force user to update his profile.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):

        if request.user.is_authenticated() and \
        not request.path.startswith(reverse('profile_update')):
            try:
                up = UserProfile.objects.get(user=request.user)

                if not up.is_filled_up:
                    return HttpResponseRedirect(reverse('profile_update'))    

            except UserProfile.DoesNotExist, e:
                print e
                # returning an HTTPResponse will effectively intercept this request
                return HttpResponseRedirect(reverse('profile_update'))