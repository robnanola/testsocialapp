from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.generic.base import View, TemplateResponseMixin

from app.core.utils import get_object_or_None
from app.wall.forms import WallPostForm
from app.core.models import WallItem

class UserWallView(FormView):
    """
    User's wall, contain posts, and user's info
    @param: pk
    """

    template_name = 'app/core/wall.html'
    form_class = WallPostForm


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        self.user = self.request.user
        self.wall_owner = get_object_or_None(User, id=kwargs.get('pk'))
        self.wall_posts = WallItem.objects.filter(Q(receiver=self.wall_owner)|Q(author=self.wall_owner)).order_by('-updated')

        return super(UserWallView, self).dispatch(*args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(UserWallView, self).get_context_data(**kwargs)
        context['wall_posts'] = self.wall_posts
        context['wall_owner'] = self.wall_owner

        return context


    def form_valid(self, form):

        form.instance.receiver = self.wall_owner
        form.instance.author = self.user
        form.save(commit=True)

        return super(UserWallView, self).form_valid(form)


    def get_success_url(self):
        return reverse('user_wall', kwargs={'pk': self.wall_owner.id})


class WallItemView(View, TemplateResponseMixin):

    template_name = 'app/core/post_item.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WallItemView, self).dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        post = WallItem.objects.get(uuid=kwargs.get('uuid',''))
        return self.render_to_response({'post':post})

