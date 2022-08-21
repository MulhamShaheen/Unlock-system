from django.shortcuts import render

import datetime

from django.shortcuts import render
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
# from ScoreManager.urls import PersonSerializer
import csv
from io import StringIO

"""
Тут написаны методы и классы которые отвечает за обработку и отправления нужных данных при определенных запросах 
"""


class PersonSerializer(
    serializers.ModelSerializer):
    """
    Класс наследник ModelSerializer, отвечает за оформление JSON объекты из объекта
    класса Person
    """

    class Meta:
        model = Person
        fields = ['id', 'first', 'middle', 'second', 'telegram', 'deeplink', 'score', 'team', 'qr']

    def create(self, validated_data):
        Person.objects.create(**validated_data)

    # def update(self, person, validated_data):


class UserSerializer(serializers.ModelSerializer):
    """
    Класс наследник ModelSerializer, отвечает за оформление JSON объекты из объекта
    класса User
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', ]



class PersonView(APIView):
    """
    Класс наследник APIView, отвечает за операции связаны с моделем Person
    """

    parser_classes = [JSONParser]

    def get(self, request, id):
        # Метод GET возвращает данные об объекте Person с соответственным id в запросе
        # print(request.GET)
        person = Person.objects.get(id=id)
        serializer = PersonSerializer(person)
        data = serializer.data
        return Response({"data": data, "bla": str(request.GET)})


class PersonScoreView(APIView):
    """
    Класс наследник APIView, отвечает за рейтинг и баллы
    """

    parser_classes = [JSONParser]

    def get(self, request):
        # метод запроса количество баллов участника по id
        person = Person.objects.get(id=request.GET['id'])
        score = person.score
        return Response({"data": {
            "score": score
        }})

    def post(self, request):
        # метод добавления баллов участнику по id
        person = Person.objects.get(id=request.data['id'])
        score = request.data['score']
        person.score += score
        person.save()

        return Response({
            "msg": f"added {score} points to {person.first} {person.second}",
            "data": {
                "person": f"{person.first} {person.second}",
                "score": person.score
            }
        })


class DayReportController(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        person = Person.objects.get(id=request.GET['id'])

        events = Event.objects.filter(date=datetime.date.today())

        data = []
        msg = ""
        sum = 0
        for event in events:
            if ScoreLog.objects.filter(person=person, event=event):
                log = ScoreLog.objects.get(person=person, event=event)
                temp = EventSerializer(event).data
                data.append(temp)

                msg += f"• <b>{temp['title']}</b>"
        if msg == "":
            msg = "Ты пока что за сегодня ничего не сделал"
        return Response({'msg': msg, 'daily_score': 0})


class EventAttendence(APIView):
    """
    Класс наследник APIView, отвечает за поосещаемость
    """

    parser_classes = [JSONParser, MultiPartParser]

    def get(self, request, id):
        # запрос список участников пристусвующих на мероприятии по id
        event = Event.objects.get(id=id)
        people = event.attendance.all()
        serializer = PersonSerializer(people, many=True)

        return Response({'attendance': serializer.data})

    def post(self, request, format=None):
        # добавить участника в список поосещаемости мероприятия
        event = Event.objects.get(id=request.data['event'])
        people = []

        for id in request.data['person_id']:
            person = Person.objects.get(id=id)
            people.append(person)
            event.attendance.add(person)

        event.save()
        serializer = PersonSerializer(people, many=True)
        return Response({'added': serializer.data})

    def put(self, request, format=None):
        # загрузка файла csv с данными (id участника и id мероприятия), который система обработает
        # и за тем  отмечает поосещаемость

        file_obj = request.data['file']
        event = Event.objects.get(id=request.data['event'])
        if file_obj.content_type == "text/csv":
            file = file_obj.read().decode('utf-8')
            csv_data = csv.DictReader(StringIO(file), delimiter=',')
            count = 0
            for row in csv_data:
                log = ScoreLog(person_id=row['person'], event_id=request.data['event'])
                count += 1
                log.save()
            return Response({"event": str(event), "added": count})

        return Response(status=400)


class EventScoreController(APIView):
    """
    Класс наследник APIView, отвечает за рейтинг на мероприятиях
    """
    parser_classes = [JSONParser]

    def post(self, request):
        # метод добавления баллов соответственных рейтингу на мероприятии

        event = Event.objects.get(id=request.data['event'])
        person = Person.objects.get(id=request.data['person_id'])

        rating = int(request.data['rating'])

        if 0 <= rating <= 10:
            rating /= 10
            added = event.max_point * rating
            person.score += added
            person.save()
            return Response({'status': f'added {added}'})

        return Response({'error': 'rating should be between 0 and 10'})


class TokenTester(APIView):  # можешь не смотреть на это
    parser_classes = [JSONParser]

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)


class PersonFinder(APIView):

    def get(self, request, name):  # redo
        temp = name.split(" ")[0]
        last = temp[0]
        first = temp[1]
        middle = temp[2]
        try:
            person = Person.objects.get(second=last, first=first)
            serializer = PersonSerializer(person)
            data = serializer.data

        except Person.DoesNotExist:
            return Response({'msg': 'Данные не найдены, вводите ещё раз или оьратитесь к ментору'}, status=404)

        return Response({'data': data})



class PeopleController(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request):
        return Response({"request": str(request)})

    def put(self, request):

        file_obj = request.data['file']
        if file_obj.content_type == "text/csv":

            file = file_obj.read().decode('utf_8_sig')
            csv_data = csv.DictReader(StringIO(file), delimiter=',')
            count = 0
            for row in csv_data:
                telegram = row['Telegram']
                if telegram:
                    if telegram[0:6] == "https:":
                        telegram = telegram.split(" ")[-1]
                    else:
                        if telegram[0] == "@":
                            telegram = telegram[1:]

                name = row['name']
                first = name.split(" ")[1]
                second = name.split(" ")[0]
                middle = name.split(" ")[2]
                person = Person(
                    first=first,
                    second=second,
                    middle=middle,
                    telegram=telegram

                )
                person.save()
                count += 1
            return Response({"added": count})

        return Response(status=400)


class EventCSV(APIView):
    parser_classes = [MultiPartParser]

    def put(self, request):

        file_obj = request.data['file']
        if file_obj.content_type == "text/csv":

            file = file_obj.read().decode('utf_8_sig')
            csv_data = csv.DictReader(StringIO(file), delimiter=',')
            count = 0
            err_arr = []
            for row in csv_data:

                name = row['name']
                first = name.split(" ")[1]
                second = name.split(" ")[0]
                try:
                    person = Person.objects.get(
                        first=first,
                        second=second,
                    )
                except Person.DoesNotExist:
                    err_arr.append(row['name'])
                if ScoreLog.objects.filter(person=person, event_id=request.data['event']):
                    pass
                else:
                    log = ScoreLog(person=person, event_id=request.data['event'])
                    log.save()
                    count += 1
            return Response({"added": count, "not found": err_arr})

        return Response(status=400)



class QRController(APIView):
    permission_classes = ()
    authentication_classes = ()
    parser_classes = [JSONParser]

    def get(self, request, event):
        return render(request, 'ScoreManager/index.html')

    def post(self, request, event):
        value = request.data['result']
        try:
            person = Person.objects.get(qr=value)
            target = Event.objects.get(id=event)
            if ScoreLog.objects.filter(person=person, event=event):
                return Response({"msg": f" {str(person)} уже добавлен"})
            log = ScoreLog(person=person, event=target)
            log.save()
        except Person.DoesNotExist:
            return Response({"msg": f"Что-то пошло не так"})
        except:
            return Response({"msg": f" {str(person)} уже добавлин"})

        return Response({"msg": f"added {str(person)}"})


# class AnswersController(APIView):

# id question
# id person
# answer

def index(request):
    return render(request, 'ScoreManager/index.html')
