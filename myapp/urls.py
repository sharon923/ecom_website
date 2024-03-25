from django.urls import path,include
from . import views

urlpatterns = [
     path('', views.index, name='home'),
     path('register/', views.register, name='register'),
     path('login/', views.login, name='login'),
     path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
     path('categoryadd/', views.category_add, name='categoryadd'),
     path('viewCategory/', views.viewCategory , name='viewCategory'),
     path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
     path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
     path('addProduct/', views.addProduct, name='addProduct'),
     path('viewProduct/', views.viewProduct, name='viewProduct'),
     path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
     path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
     path('userDashboard/', views.userDashboard, name='userDashboard' ),
     path('logout/', views.user_logout, name='logout'),
     path('userProfile/', views.userProfile, name='userProfile'),
     path('userProfileUpdate/', views.userProfileUpdate, name='userProfileUpdate'),
     path('category/', views.category, name='category'),
     path('products/', views.products, name='products'),
     path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
     path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
     path('update_quantity/<int:product_id>/<str:action>/', views.update_quantity, name='update_quantity'),
     path('view_cart/', views.view_cart, name='view_cart'),
     path('admin_logout/', views.admin_logout, name='admin_logout' ),
     path('razorpay_payment/<int:total_amount>/', views.razorpay_payment, name='razorpay_payment'),
     path('create_address/', views.create_address, name='create_address'),
     path('payment_success/', views.payment_success, name='payment_success'),
     path('payment_failed/', views.payment_failed, name='payment_failed'),
     path('purchase_history/', views.purchase_history, name='purchase_history'),
    path('download_purchase_pdf/<int:purchase_id>/', views.download_purchase_pdf, name='download_purchase_pdf'),
    path('all_purchases/', views.all_purchases, name='all_purchases'),
    path('update_password/', views.update_password, name='update_password'),
    path('delete-purchase/<int:purchase_id>/', views.delete_purchase, name='delete_purchase'),
    path('user_list/', views.user_list, name='user_list'),
    path('search/', views.search, name='search'),
]
