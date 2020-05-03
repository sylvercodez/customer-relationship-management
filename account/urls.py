from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('user/',views.userpage,name='user_page'),
    path('register/',views.Register,name='register'),
    path('login/',views.loginuser,name='login'),
    path('logout/',views.logoutuser,name='logout'),

    path('products/',views.products, name='products'),
    path('customers/<str:pk_test>/',views.customer, name='customers'),
    path('about/',views.about, name='about'),
    
    path('creatcustomer/',views.createCustomer,name='customerform'),
    path('updatecustomerform/',views.updatecustomerform,name='updatecustomerform'),

    path('profile/',views.accountsettings, name='profile'),
    path('createform/<str:pk>/',views.createform, name='createform'),
    path('updateform/<str:pk>/',views.updateform, name='updateform'),
    path('deleteform/<str:pk>/',views.delete_form, name='deleteform'),
    
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), 
        name="password_reset_complete"),



]

'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''