from django.urls import path
from . import views

urlpatterns = [
    path('check/',views.postCheck,name="check"),
    path('keywords/',views.postKeywords,name="keywords"),
    path('sections/',views.postSections,name="sections"),
    path('articles/',views.postArticles,name="articles"),
    path('onlysections/',views.postOnlySections,name="onlysections"),
    path('onlyarticles/',views.postOnlyArticles,name="onlyarticles"),
]