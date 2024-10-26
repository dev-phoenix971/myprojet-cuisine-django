from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from cuisineantillaise.views import index
from django.conf.urls.i18n import i18n_patterns

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('i18n/', include('django.conf.urls.i18n')),

# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += i18n_patterns(
#     path('', index, name="home"),
#     path('accounts/', include('accounts.urls')),

# )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="home"),
    path('', include('accounts.urls')),
    path('blog/', include('blog.urls')),
    path('tinymce/', include("tinymce.urls")),
    path('contact/', include('contact.urls')),
    path('recettes/', include('recettes.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)