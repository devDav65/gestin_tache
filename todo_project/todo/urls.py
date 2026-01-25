from django.urls import path 
from .views import list_task, list_create, list_update, delete_task, completed_task, signin_user,login_user,logout_user,profil,change_password,update_profil,nocompleted_task


urlpatterns = [
    path("", list_task, name='list_task'),
    path("list_create/",list_create,name='list_create' ),
    path("list_update/<int:id>/",list_update,name='list_update' ),
    path("delete_task/<int:id>/",delete_task,name='delete_task' ),
    path("completed_task/<int:id>/",completed_task,name="completed_task"),
    path("signin_user/",signin_user,name="signin_user"),
    path("logout_user/",logout_user,name="logout_user"),
    path("login_user/",login_user,name="login_user"),
    path("profil/",profil,name="profil"),
    path("change_password/",change_password,name="change_password"),
    path("update_profil/",update_profil,name="update_profil"),
    path("nocompleted_task/<int:id>/",nocompleted_task,name="nocompleted_task"),



]                 