from django.urls import path
from . import views 



urlpatterns = [
    path('', views.home, name='home'),
    # path('category/<slug:category_slug>/', views.category_view, name='category_view'),
    path('about_us/', views.about_us, name='aboutus'),
    path('category_list/', views.category_list, name='categorylist'),
    path('contact_us/', views.contact_us, name='contactus'),
    path('my_account/', views.my_account, name='myaccount'),
    path('index_inverse/', views.index_inverse, name='indexinverse'),
    path('search_results/', views.search_results, name='searchresults'),


    path('faq/', views.FAQView.as_view(), name='faq'),
]