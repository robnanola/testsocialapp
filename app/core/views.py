from __future__ import unicode_literals 

from django.shortcuts import render
from django.contrib.auth.views import login
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.base import View, TemplateResponseMixin

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm

from app.core.models import UserProfile, Photo, WallItem
from app.core.utils import get_object_or_None
from app.core.forms import ProfileForm, ProfilePictureForm, SearchForm
from app.wall.forms import WallPostForm

import watson


class HomeView(FormView):

    template_name = 'app/home.html'
    form_class = WallPostForm

    def dispatch(self, *args, **kwargs):

        if self.request.user.is_authenticated():
            self.user = self.request.user
            self.wall_owner = get_object_or_None(User, id=kwargs.get('pk'))
            self.wall_posts = WallItem.objects.filter(Q(receiver=self.user)|Q(author=self.user)).order_by('-updated')

        return super(HomeView, self).dispatch(*args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['wall_posts'] = self.wall_posts
            context['wall_owner'] = self.wall_owner
        else:
            context['form'] = AuthenticationForm

        return context


    def form_valid(self, form):

        form.instance.receiver = self.user
        form.instance.author = self.user
        form.save(commit=True)

        return super(HomeView, self).form_valid(form)


    def get_success_url(self):
        return reverse('home')



class ProfileView(TemplateView):
    template_name = 'app/profile.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        user_profile = get_object_or_None(UserProfile, user=self.request.user)

        if user_profile is None:
            return HttpResponseRedirect(reverse_lazy('profile_update'))

        return super(ProfileView, self).dispatch(*args, **kwargs)


class UpdateProfileView(UpdateView):
    model = UserProfile
    fields = ['address', 'phone', 'work', 'education']
    template_name_suffix = '_update_form'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UpdateProfileView, self).dispatch(*args, **kwargs)


class UpdateProfileFormView(FormView):
    template_name = 'app/core/userprofile_update_form.html'
    fields = ['address', 'phone', 'work', 'education']
    form_class = ProfileForm
    model = UserProfile
    success_url = reverse_lazy('profile')




    def get_object(self):

        user_profile = get_object_or_None(UserProfile, user=self.request.user)

        if user_profile is None:
            # return a new instance of user_profile
            user_profile = UserProfile()
            user_profile.user = self.request.user
            user_profile.save()

            #return user_profile

        return user_profile

    def object_to_dict(self, obj=None):
        if obj:
            return model_to_dict(obj, fields=self.fields)

        return model_to_dict(self.get_object(), fields=self.fields)

    def get_initial(self):
        return self.object_to_dict()

    def form_valid(self, form):
        updates = self.object_to_dict(obj=form.instance)

        UserProfile.objects.filter(user=self.request.user).update(**updates)

        return super(UpdateProfileFormView, self).form_valid(form)



class UpdateProfilePicture(FormView):
    template_name = 'app/core/update_profile_picture.html'
    form_class = ProfilePictureForm
    success_url = reverse_lazy('profile')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """

        """
        self.user = self.request.user
        self.photos = Photo.objects.filter(user=self.user).order_by('-created')
        self.profile_picture = get_object_or_None(Photo, user=self.user, profile_pic=True)

        return super(UpdateProfilePicture, self).dispatch(*args, **kwargs)


    def form_valid(self, form):

        # we assume that every new upload will be the default profile pic
        # set all photos of user profile_pic to false
        self.photos.update(profile_pic=False)

        form.instance.user = self.user
        form.instance.original_filename = form.instance.original_image.name[:128]
        form.instance.original_filesize = form.instance.original_image.size
        form.instance.profile_pic = True

        form.save(commit=True)

        return super(UpdateProfilePicture, self).form_valid(form)


class SearchView(View, TemplateResponseMixin):
    template_name = 'app/core/search.html'
    form_class = SearchForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SearchView, self).dispatch(*args, **kwargs)


    def get(self, *args, **kwargs):

        return self.render_to_response({'form':self.form_class})

    def post(self, *args, **kwargs):

        search_query = self.request.POST.get('search','')
        print search_query
        search_results = watson.search(search_query)


        return self.render_to_response({'form': self.form_class(self.request.POST), 
            'results': search_results})





