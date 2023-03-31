from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("my_app/", include("my_app.urls")),
    path('', include('users.urls')),
    path('api/', include('api.urls')),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html'),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='reset.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'),
         name='password_reset_complete')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ეს გვჭირდება იმისთვის რომ პროექტის გვერდზე რო გადავალთ სტატიკური ფაილები გვიჩვენოს
# MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# ეს ქვედაც  იგივეა მარა,
# DEBUG = False
# ALLOWED_HOSTS = ['localhost', '127.0.0.1']
# რომ შევცვალეთ აღარ გვაჩვენბდა სურათებს და მაგისთვისააა
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

