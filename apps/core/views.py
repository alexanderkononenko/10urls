from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from apps.core.models import Url
from django.contrib.auth.models import User
import hashlib
from django.conf import settings


class HomepageView(View):
    def get(self, request):
        return render(request, 'home.html')

    def post(self, request):
        url = request.POST.get('url')
        try:
            u = Url.objects.get(url=url)
        except ObjectDoesNotExist:
            u = Url()
            u.url = url
            u.hash = hashlib.sha1(url.encode()).hexdigest()[:settings.HASH_LEN]
            u.owner = User.objects.filter(is_staff=False).order_by('?').first()
            u.save()
        return HttpResponseRedirect('/!' + u.hash)


class UrlView(View):
    def get(self, request, show, hash):
        url = get_object_or_404(Url, hash=hash)
        ret = ''
        if show:
            return render(request, 'url.html', {'url': url})
        else:
            return HttpResponseRedirect(url.url)
