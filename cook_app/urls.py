from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.root),
    path('home', views.home),
    path('register', views.register),
    path('login', views.login_view),
    # in
    path('userin_home', views.userin_home),
    path('add_recipe', views.add_recipe),
    path('edit/<int:id>', views.edit),
    path('delete/<int:id>', views.delete),
    path('chefs', views.chefs),
    path('edit_profile', views.edit_profile),
    path('profile/<int:id>', views.profile),
    path('recipe/<int:id>', views.recipe_detail),
    # out
    path('logout', views.logout),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
