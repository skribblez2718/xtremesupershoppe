from django.urls import path
from base.views import user_views as views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.register_user, name="register"),
    path('proof/', views.get_proof, name='proof'),
    
    path('profile/', views.get_user_profile, name="user-profile"),
    path('profile/update/', views.update_user_profile, name="user-profile-update"),
    path('', views.get_users, name="users"),

    path('<str:pk>/', views.get_user_by_id, name="user-by-id"),
    path('delete/<str:pk>/', views.delete_user, name="user-delete"),
    path('update/<str:pk>/', views.update_user, name="user-update"),
]