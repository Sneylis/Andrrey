from django.urls import path
from . import views
from django.contrib.auth import views as authViews
from .views import *

app_name='techMarket'


urlpatterns = [
    path('',views.index, name='index'),
    path('category/<int:cat_id>/',views.showCat,name='showCategory'),
    path('group/<int:group_id>',views.SGroup,name='ShGroup'),
    path('unit/<int:unit_id>/',views.showUnit,name='ShowUnit'),
    path('del/<int:unit_id>',views.delunit,name='delUnit'),
    path('addUnit/',views.AddUnit,name='addunit'),
    path('updUnit/<int:pk>/', views.updunit.as_view(), name='updUnit'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path('Profile',views.user_link,name='userLink'),
    path('exit/',authViews.LogoutView.as_view(next_page='techMarket:index'),name='exit'),
    path('about/',views.about,name='About'),
    path('password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('question/<int:unit_id>/',views.GetQuestion,name='getQuestion'),
    path('MyQyestuion/',views.ShUserQuestion,name='UserQuestion'),
    path('GetQuestion/',views.GetAsnwer,name='AdminQuestion'),
    path('GetChoice/<int:pk>',views.GetChiuce,name='AdminChoice'),

    path('addGroup',views.AddGroup,name='addGroup'),
    path('delGr/<int:pk>',views.delGr,name='delGr'),
    path('updGr/<int:pk>',views.updGr.as_view(),name='updGroup'),

    path('addCat/',views.AddCat,name='addCat'),
    path('delCat/<int:pk>',views.delCat,name='delCat'),
    path('updCat/<int:pk>',views.updCat.as_view(),name='updCat')



]