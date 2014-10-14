from django.views.generic.base import View, TemplateResponseMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

from app.core.models import Photo
from app.core.utils import JSONResponse, response_mimetype, get_object_or_None


class SetProfilePicAjaxView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SetProfilePicAjaxView, self).dispatch(*args, **kwargs)


    def post(self, *args, **kwargs):
        print self.request.POST.get('uuid'),'>>>>>>>>>>'

        uuid = self.request.POST.get('uuid')
        user = self.request.user

        profile_pic = get_object_or_None(Photo, user=user, uuid=uuid)

        if profile_pic:
            # set pictures to false first
            user.profile_pictures.update(profile_pic=False)

            profile_pic.profile_pic = True
            profile_pic.save()

            data = {'status': 'OK'}

        else:
            data = {'status': 'ERROR'}

        if self.request.is_ajax():
            response = JSONResponse(data, {}, response_mimetype(self.request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response





