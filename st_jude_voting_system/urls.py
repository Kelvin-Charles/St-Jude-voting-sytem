from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from election import views as election_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('election.urls')),
    path('login/', election_views.CustomLoginView.as_view(), name='login'),
    path('logout/', election_views.CustomLogoutView.as_view(), name='logout'),
    path('register/', election_views.register_view, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 