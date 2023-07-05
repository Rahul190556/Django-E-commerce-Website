from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,ChangePasswordForm,MypasswordResetForm,MySetPasswordForm
urlpatterns = [
    path('',views.ProductView.as_view(),name='home'),
    path('search/',views.SearchView,name='search'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart, name='show_cart'),
    path('pluscart/', views.Plus_cart, name='plus_cart'),
    path('minuscart/', views.Minus_cart, name='minus_cart'),
    path('removecart/', views.Remove_cart, name='remove_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='payment_done'),

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),

    path('mobile/', views.mobile, name='mobile'),
    path('laptop/', views.laptop, name='laptop'),
    path('topwear', views.topwear, name='topwear'),
    path('bottomwear', views.bottomwear, name='bottomwear'),

    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    path('topwear/<slug:data>', views.topwear, name='topweardata'),
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomweardata'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',
    authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password/change/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html',
    form_class=ChangePasswordForm,success_url="/password/change/done/"),name='password_change'),
    path("password/change/done/",auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),
         name='passwordchangedone'),
    path("password/reset/",auth_views.PasswordResetView.as_view(template_name='app/passwordreset.html'
       ,form_class=MypasswordResetForm),name='passwordreset'),
    path("password-reset/done",auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),
         name='password_reset_done'),
    path("password-reset-confirm/<uidb64>/<token>",auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',
        form_class=MySetPasswordForm),
         name='password_reset_confirm'),
    path('password-reset-complete',auth_views.PasswordResetCompleteView.as_view(template_name="app/password_reset_complete.html")
         ,name='password_reset_complete'),




    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
