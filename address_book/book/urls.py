from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.urls import path
from book import views

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'homepage.html'), name='homepage'),
    path('<int:pk>/profile/', views.ContactDetail.as_view(), name='contact-information'),
    path('all-contacts/', views.ContactList.as_view(), name='all-contacts'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add/', views.create_contact, name='add-contact'),
    path('<int:pk>/profile/star/', views.mark_star, name='mark-star'),
    path('starred/', views.StarredList.as_view(), name='starred'),
    path('<int:pk>/profile/delete/', views.ContactDelete.as_view(), name='contact-delete'),
    path('<int:pk>/profile/edit/', views.update_contact, name='edit-contact'),
    path('search/', views.search_query, name='search')
]