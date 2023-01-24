
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('logout', views.logout_ftn, name = "logout"),
    path('monitor', views.load_monitor, name="monitor"), 
    path('site', views.load_site, name="site"), 
    path('kavumu', views.load_kavumu, name="kavumu"), 
    path('upload_data', views.load_upload_data, name="upload_data"), 
    path('update_db', views.upload_data_ftn, name="update_db"), 
    path('export', views.load_export, name="export"),
    path('export_db', views.new_export_ftn, name="export_db"), 
]