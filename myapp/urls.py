from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', views.HistoryView)

urlpatterns = [
    path('', views.index),
    # path('signup/', views.signup),
    path('signout/', views.signout),
    path('login/', views.handleLoginRequest),
    path('submit-signup/', views.handleSignupRequest),
    path('history/', views.history),
    path('logs/', views.logs),
    path('transactions/', views.transactions),
    path('analytics/', views.analytics),
    path('search/', views.search),
    path('delete-history/<int:id>/', views.delete_history),
    # analytics
    path('api',views.ChartData.as_view()),
    path('restapi/', include(router.urls)),
    # notifications
    path('notify/', views.notify),
]