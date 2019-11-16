from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.urls import url

from .views import QuestionListView, AnswerViewSet, UserViewSet, QuestionUserListView

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('answer', AnswerViewSet, basename='answer')
router.register('user', UserViewSet, basename='user')

API_VERSION = '(?P<version>v\d+)'

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    url(f'{API_VERSION}/questions/', QuestionListView.as_view(), name='question-list'),
    url(f'{API_VERSION}/question-users/', QuestionUserListView.as_view(), name='question-users'),
    url(f'{API_VERSION}/', include(router.urls)),
]
