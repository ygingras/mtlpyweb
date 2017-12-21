import os
import logging
import datetime

import pytz

from urllib.parse import urlparse

from django import forms
from django.utils.translation import get_language, gettext_lazy as _
from django.shortcuts import (render, get_object_or_404)

from django.urls import reverse
from django.conf import settings

from django.core.mail import send_mail
from django.core.urlresolvers import resolve

from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import translation

from mtlpy.blog.models import Post
from mtlpy.api.videos import get_all_videos
from mtlpy.models import Sponsor

log = logging.getLogger(__name__)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    message = forms.CharField()
    email = forms.EmailField()


def home_page(request):
    posts = Post.published_objects.all()[:3]
    sponsors = (Sponsor.objects
                .filter(frontpage=True)
                .filter(~Q(partner=True))
                .order_by('ordering'))
    partners = (Sponsor.objects.filter(frontpage=True, partner=True)
                .order_by('ordering'))
    ctx = {
        'blog_posts': posts,
        'sponsors': sponsors,
        'partners': partners,
        }
    return render(request, 'index.html', ctx)


def change_locale(request, language):
    """
    Change the language of the current user to <language> and redirect
    to <redirect_to> if present, if not, it will:

    1) get the referrer
    2) extract the path of this url
    3) get the view corresponding to this path

    Then the language is changed and we are redirecting to the resolved url.

    :param request: The HttpRequest object of the view
    :param language: the languge code to switch to
    :param redirect_to: url the user is gonna be redirected (default None)
    :return: HttpResponseRedirect
    """
    resolved_path = None

    redirect_to = request.GET.get('redirect_to')

    if redirect_to is None:
        current_language = get_language()
        redirect_to = request.META.get('HTTP_REFERER', f"/{current_language}/")
        path = urlparse(redirect_to).path
        resolved_path = resolve(path)

    translation.activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language

    if resolved_path:
        redirect_to = reverse(
            resolved_path.view_name,
            args=resolved_path.args,
            kwargs=resolved_path.kwargs,
        )

    return HttpResponseRedirect(redirect_to)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['email']
            recipients = settings.CONTACT_EMAILS
            message = _('From: %(name)s\n\nMessage: %(message)s') % {
                'name': name,
                'message': message,
            }
            subject = _('Message from MontrealPython.org contact form')
            send_mail(subject, message, sender, recipients)
    else:
        form = ContactForm()

    return render(request, "contact.html", {
        'form': form,
        'contact_email': settings.CONTACT_EMAILS[0],
    })


def styleguide(request):
    return render(request, 'styleguide.html', {})


def videos(request):
    videos = get_all_videos(settings.YOUTUBE_API_KEY)
    return render(request, 'videos.html', {"videos": videos})


def sponsor_details(request, slug):
    sponsor = get_object_or_404(Sponsor, slug=slug)
    return render(request, 'sponsor_details.html', {"sponsor": sponsor})


def sponsorship(request):
    sponsors = (Sponsor.objects
                .filter(frontpage=True)
                .filter(~Q(partner=True))
                .order_by('ordering'))
    return render(request, 'sponsorship.html', {"sponsors": sponsors})


debug_startup_time = datetime.datetime.now(pytz.utc).isoformat()


def debug(request):
    log.info(
        "Debug request\nscheme=%s\n env\n%s\n headers\n%s",
        request.scheme, os.environ, request.META,
    )

    response = {
        'headers': {k: str(v) for k, v in request.META.items()},
        'process': {'startup_time': debug_startup_time},
    }
    return JsonResponse(response)
