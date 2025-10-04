from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart_view, name='cart'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('category/<str:name>/', views.books_by_category, name='books_by_category'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('wishlist/add/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('orders/', views.order_history_view, name='order_history'),
    path('wishlist/remove/<int:book_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('profile/', views.profile_view, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('wishlist/move-to-cart/<int:book_id>/', views.move_to_cart, name='move_to_cart'),

]