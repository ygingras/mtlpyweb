from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.views.decorators.cache import cache_page

import mtlpy.views
import mtlpy.blog.views
import mtlpy.pages.views

from mtlpy.blog.feed import BlogEntriesFeed
from mtlpy.files import media

from django.contrib import admin


urlpatterns = [
    url(r'^robots\.txt$', mtlpy.views.robotstxt, name='robots.txt'),

    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^blog/transfer_tool/$', mtlpy.blog.views.transfer_posts_tool,
        name='transfer_tool'),
    # url(r'^debug$', mtlpy.views.debug, name='debug'),
    media(),
]

urlpatterns += i18n_patterns(
    url(r'^$', mtlpy.views.home_page, name='home_page'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$',
        mtlpy.blog.views.post, name='blog_detail'),
    url(r'^blog/(?P<slug>[-\w|\W]+)/$', mtlpy.blog.views.PostListView.as_view(),
        name='blog_category'),
    url(r'^blog/$', mtlpy.blog.views.PostListView.as_view(), name='blog'),
    url(r'^user/(?P<userid>\d+)/$', mtlpy.blog.views.UserPostListView.as_view(),
        name='user_posts'),
    url(r'^sponsor/(?P<slug>[-\w|\W]+)/$', mtlpy.views.sponsor_details,
        name='sponsor_details'),
    url(r'^styleguide', mtlpy.views.styleguide),
    url(r'^videos/', cache_page(15 * 60)(mtlpy.views.videos), name='videos'),
    url(r'^sponsorship/', mtlpy.views.sponsorship, name='sponsorship'),
    url(r'^slackin', include('django_slackin_public.urls')),

    url(r'^feed/$', BlogEntriesFeed(), name="feed"),
    url(r'^change_locale/(?P<language>\w{2})/$', mtlpy.views.change_locale,
        name='change_locale'),
    url(r'^admin/?', admin.site.urls),

    # Flatpages must be evaluated after all others since 404 will be raised if not found
    url(r'^(?P<url>.*)$', mtlpy.pages.views.i18n_flatpage, name='flatpage'),
)
