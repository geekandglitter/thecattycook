 
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from recipes import views
from django.urls import path
from .views import ModelList # this is for the new class-based view
from recipes.models import AllRecipes

urlpatterns = [
 
  path("admin/", admin.site.urls),  # Activates the admin interface 
  path('', views.home, name='home'),  
   
  path('error', views.errors_view),
  path('scrape', views.scrape_view),   
  path('get', views.get_view),
  path('getchron', views.getchron_view), 
  path('searchsuggestions', views.searchsuggestions_view),
  path('searchresults', views.searchboxes_view),  
  path('get-the-model-data', views.get_the_model_data_view),
  path('go-here', ModelList.as_view(model=AllRecipes)), 
  path('count-words', views.count_words_view),   
  path('get-store', views.get_and_store_view),
  path('feedparsed', views.feedparse_view), 
  path('searchedinput', views.searchinput_view), 
  
]

 
