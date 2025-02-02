from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from election import views as election_views
from django.contrib.auth import views as auth_views
from election.admin_customization import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('election.urls')),
    path('login/', auth_views.LoginView.as_view(
        template_name='admin/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', election_views.CustomLogoutView.as_view(), name='logout'),
    path('register/', election_views.register_view, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 