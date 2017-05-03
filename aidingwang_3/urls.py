from django.conf.urls import patterns, include, url
import xadmin
from django.conf.urls.static import static
from django.conf import settings
import xadmin
from home import views
xadmin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aidingwang_3.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^xadmin/', include(xadmin.site.urls)),
    # url(r'^',include('home.urls')),
    url(r'^$',views.index),
    url(r'^catalog/',include('catalog.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls',namespace='catalog')),
    url(r'^Accounts/', include('Accounts.urls')),
    url(r'^Store/', include('Store.urls')),
    # url(r'^ueditor/',include('DjangoUeditor.urls' )),
    # url(r'^Store/',include('Store.urls'))
                       )
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

