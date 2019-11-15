from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import QuestionListView, AnswerViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('answer', AnswerViewSet)

API_VERSION = '1'

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('v{}/'.format(API_VERSION), include(router.urls)),
    path('v{}/questions/'.format(API_VERSION), QuestionListView.as_view(), name='question-list')
]
