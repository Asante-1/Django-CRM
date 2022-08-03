from django.urls import path
from . import views
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView,

)

app_name='Leads'
urlpatterns = [
    path('', views.LandingPageView.as_view(), name="Landing_page"),
    path('Lead/',views.LeadListView.as_view(), name='Lead'),
    path('create/',views.LeadCreateView.as_view(), name='create'),
    path('<int:pk>/update/',views.LeadUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/',views.LeadDeleteView.as_view(), name='delete'),
    path('Leads/<int:pk>/', views.LeadDetailView.as_view(), name='Lead_detail'),
    path('login/', LoginView.as_view(), name='Login'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('logout/', LogoutView.as_view(), name='Logout'),
    path('<int:pk>/assign_agent/', views.AssignAgentView.as_view(), name='assign_agent'),
    path('signup/', views.SignUpView.as_view(), name='Signup'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('<int:pk>/category-detail/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('<int:pk>/category-update/', views.LeadCategoryUpdateView.as_view(), name='category_update'),
    path('<int:pk>/followups-create/', views.FollowupCreateView.as_view(), name='followups_create'),
    path('<int:pk>/followups-update/', views.FollowUpUpdateView.as_view(), name='followups_update'),
    path('<int:pk>/followups-delete/', views.FollowUpDeleteView.as_view(), name='followups_delete'),
    path('create-category /', views.CategoryCreateView.as_view(), name='category-create'),
]