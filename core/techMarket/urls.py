from django.urls import path
from . import views
from django.contrib.auth import views as authViews
app_name='techMarket'

urlpatterns = [
    path('',views.index, name='index'),
    path('category/<int:cat_id>/',views.showCat,name='showCategory'),
    path('unit/<int:unit_id>/',views.showUnit,name='ShowUnit'),
    path('del/<int:unit_id>',views.delunit,name='delUnit'),
    path('addUnit/',views.AddUnit,name='addunit'),
    path('updUnit/<int:pk>/', views.updunit.as_view(), name='updUnit'),
    path('updPass/',views.updPass.as_view(),name='updPass'),
    path('register/',views.register.as_view(),name='register'),
    path('login/',views.login.as_view(),name='login'),
    path('Profile',views.user_link,name='userLink'),
    path('exit/',authViews.LogoutView.as_view(next_page='index'),name='exit')
]