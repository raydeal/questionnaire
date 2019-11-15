from django.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework.urls import url

from .views import QuestionListView, AnswerViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('answer', AnswerViewSet)

API_VERSION = '(?P<version>v\d+)'

urlpatterns = [
    url(f'{API_VERSION}/auth/', include('rest_framework.urls')),
    url(f'{API_VERSION}/questions/', QuestionListView.as_view(), name='question-list'),
    url(f'{API_VERSION}/', include(router.urls)),
]
