from django.urls import path
from . import views
from django.views.decorators.cache import never_cache

urlpatterns = [
    path("home/", views.index, name="home"),
    path("projects/<str:pk>/", never_cache(views.projects), name="projects"),
    path("create-project", views.create_project, name='create-project'),
    path('update-project/<str:pk>/', never_cache(views.update_project), name='update-project'),
    path('delete-project/<str:pk>/', views.delete_project, name='delete-project'),
]