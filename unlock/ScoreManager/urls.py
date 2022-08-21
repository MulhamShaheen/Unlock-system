import rest_framework.views
from django.urls import path, include

from .models import Person

from rest_framework import routers, viewsets
from .views import *

"""
В этом файле написаны пути и URL, какой ответ получить по какой URL 
"""
# # ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PersomViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer



router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'people', PersomViewSet)


urlpatterns = [
    # тут каждый путь связан с методом или классом в файле views.py
    # path('main/', csrf_exempt(views.index), name='index'),
    path('today/', DayReportController.as_view(), name='index'),
    path('participant/find/<name>',PersonFinder.as_view(), name='find_by_name'),
    # path('test/', TestView.as_view(), name='test'),
    path('score/', PersonScoreView.as_view(), name='person_score_path'),
    path('participant/<int:id>', PersonView.as_view(), name='person_path'),
    path('attendence/', EventAttendence.as_view(), name='attendence'),
    # path('attendence/<int:id>', get attendence, name='attendence'),
    path('event/score/', EventScoreController.as_view(), name='score'),
    path('event/upload/', EventCSV.as_view(), name='upload_event'),
    path('upload/', PeopleController.as_view(), name='upload'),
    path('qr/test/', csrf_exempt(QRController.as_view()), name='qr'),
    path('qr/scan/<int:event>', csrf_exempt(QRController.as_view()), name='qr'),
    path('', include(router.urls)),
]
