from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nutrition.urls')),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="authentification/reset_password.html"),
         name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="authentification/reset_password_sent.html"),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="authentification/reset_password_confirm.html"),
         name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="authentification/password_reset_complete.html"),
         name='password_reset_complete'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
