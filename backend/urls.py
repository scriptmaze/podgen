"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from backend import views # fonction qui gère upload des fichiers PDF


# Fonction pour la route principal
def home(request):
    """
    View function for the home route.
    
    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        JsonResponse: A JSON response with a welcome message.
    """
    print(request)
    return JsonResponse({"message": "T dans le backend la route utilisé est le root"})


urlpatterns = [
    path('', home, name='home'),  # route par défault, page d'acceuil
    path('upload-pdf/', views.upload_pdf, name='upload_pdf'),  # route pour uploader un PDF
    path('api/podcasts/', views.list_podcasts, name='list_podcasts'),
    path('podcast-status/', views.get_podcast_status, name="podcast_status"),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:  # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
