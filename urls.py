from django.conf.urls import patterns,  include,  url
from view import index, login, register, newidea, uploadify_script, profile_delete, reachnewwordidea, reachnewimgidea, addgood, addcollect, showcollected, userinfo, myidea, showmyidea, showmycollectedidea, howtoaddlooknumber, logout, changepwd, caijian, upload_temppic, editidea, reacheditidea, jubao, noie, changebadge, truelogin, deltest
import settings
from django.contrib import admin
admin.autodiscover()


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': settings.STATIC_URL + 'baricon/mini_logo.ico'}),
    (r'^admin/',  include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^index/$', index),
    (r'^login/$', login),
    (r'^register/$', register),
    (r'^newidea/(.+)/$', newidea),
    (r'^upload_script/$', uploadify_script),
    (r'^upload_temppic/$', upload_temppic),
    (r'^delete_uploadfile/$', profile_delete),
    (r'^reachnewwordidea/$', reachnewwordidea),
    (r'^reachnewimgidea', reachnewimgidea),
    (r'^addgood/$', addgood),
    (r'^addcollect/$', addcollect),
    (r'^showcollected/$', showcollected),
    (r'^showmycollectedidea/$', showmycollectedidea),
    (r'^userinfo/$', userinfo),
    (r'^myidea/$', myidea),
    (r'^showmyidea/$', showmyidea),
    (r'^howtoaddlooknumber/$', howtoaddlooknumber),
    (r'^logout/$', logout),
    (r'^changepwd/$', changepwd),
    (r'^caijian/$', caijian),
    (r'^editidea/$', editidea),
    (r'^reacheditidea/$', reacheditidea),
    (r'^jubao/$', jubao),
    (r'^noie/$', noie),
    (r'^changebadge/$', changebadge),
    (r'^truelogin/$', truelogin),
    (r'^deltest/$', deltest),
    (r'^$', index),
    # Examples:
    # url(r'^$',  'newlm1d.views.home',  name='home'),
    # url(r'^newlm1d/',  include('newlm1d.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/',  include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/',  include(admin.site.urls)),
)
