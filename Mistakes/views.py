from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum, Max, Min, Count, F, Q, Avg
from .serializers import *
from .models import *
from User.serializers import *
from User.models import *


class PhotoList(ListCreateAPIView):
    parser_classes = [JSONParser, MultiPartParser]
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class PhotoEditView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def patch(self, request, id):
        photo = Photo.objects.get(id=id)
        rasm = request.data.get('photo')
        photo.photo = rasm
        photo.save()
        return Response({'message': 'successfully'})

    def get(self, request, id):
        try:
            photo = Photo.objects.get(id=id)
            ser = PhotoSerializer(photo)
            return Response(ser.data)
        except:
            return Response({'message': "bu id xato"})

    def delete(self, request, id):
        photo = Photo.objects.get(id=id)
        photo.delete()
        return Response({'message':'successfully deleted'})


class Ish_TuriView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request):
        ish_turi = Ish_turi.objects.all()
        ser = Ish_turiSerializer(ish_turi, many=True)
        return Response(ser.data)

    def post(self, request):
        serializer = Ish_turiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class Ish_TuriDetail(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request, id):
        try:
            ish_turi = Ish_turi.objects.get(id=id)
            ser = Ish_turiSerializer(ish_turi)
            return Response(ser.data)
        except:
            return Response({'message': "bu id xato"})

    def patch(self, request, id):
        ish_turi = Ish_turi.objects.get(id=id)
        serializer = Ish_turiSerializer(ish_turi, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, id):
        ish_turi = Ish_turi.objects.get(id=id)
        ish_turi.delete()
        return Response(status=204)


class BolimView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request):
        bolim = Bolim.objects.all()
        ser = BolimSerializer(bolim, many=True)
        return Response(ser.data)

    def post(self, request):
        """
        name : string
        bulim_id : string (unique)
        user : id
        """
        ser = BolimSerializer(data=request.data)
        if ser.is_valid():
            userr = ser.validated_data.get('user')
            if userr.is_bulim==True:
                ser.save()
                return Response(ser.data, status=201)
            return Response({'message': 'Bu User Bulimga Boshliq Bo\'lolmaydi Chunki Bu User Bulim Uchun Emas!'})
        return Response(ser.errors, status=400)


class BolimDetail(APIView):
    parser_classes = (MultiPartParser, JSONParser)
    def get(self, request, id):
        # try:
        bulim = Bolim.objects.get(id=id)
        xod = Xodim.objects.filter(bulimi = bulim)
        ser = BolimSerializer(bulim)
        xodim = XodimSerializer(xod, many=True)
        a = {}
        if Hisobot.objects.filter(xodim__bulimi=bulim):
            missed = Hisobot.objects.filter(xodim__bulimi=bulim)
            sum_xato = missed.aggregate(soni=Sum('xato_soni'))
            sum_butun = missed.aggregate(soni=Sum('butun_soni'))
            total_mistakes = sum_xato['soni'] + sum_butun['soni']
            xato_foizi = round((sum_xato['soni'] * 100) / (total_mistakes) if total_mistakes else 0, 2)
            butun_foizi = round((sum_butun['soni'] * 100) / (total_mistakes) if total_mistakes else 0, 2)
            a[str('bulim_name')]=str(bulim.name)
            a[str('bulim_id')]=str(bulim.bulim_id)
            a[str('bulim_boshliq')]=str(bulim.user.first_name)
            a[str('xato_soni')]=sum_xato
            a[str('butun_soni')]=sum_butun
            a[str('Xato_foizi')]=xato_foizi
            a[str('Butun_foizi')]=butun_foizi
            a[str('hisobot_soni')]=len(missed)
            b = missed.aggregate(Count('xodim'))
            a[str('xodim_soni')]=b
            c = []
            for j in missed:
                found = False
                for item in c:
                    if item['mahsulot_name'] == j.mahsulot.name:
                        item['mahsulot_id'] = j.mahsulot.mahsulot_id
                        item['xato_soni'] += j.xato_soni
                        item['butun_soni'] += j.butun_soni
                        found = True
                        break
                if not found:
                    c.append({'mahsulot_name': j.mahsulot.name, 'mahsulot_id': j.mahsulot.mahsulot_id, 'xato_soni': j.xato_soni, 'butun_soni': j.butun_soni})
            for i in missed:
                for item in c:
                    if item['mahsulot_name'] == i.mahsulot.name:
                        item['Xato_foizi'] = round(item['xato_soni']*100/(item['xato_soni'] + item['butun_soni']), 2)
                        item['Butun_foizi'] = round(item['butun_soni']*100/(item['xato_soni'] + item['butun_soni']), 2) 
            d = []
            for j in missed:
                found = False
                for item in d:
                    if item['xato_name'] == j.xato.name:
                        item['xato_id'] = j.xato.xato_id
                        item['mahsulot_name'] = j.mahsulot.name
                        item['xato_soni'] += j.xato_soni
                        found = True
                        break
                if not found:
                    d.append({'xato_name': j.xato.name, 'xato_id': j.xato.xato_id, 'mahsulot_name': j.mahsulot.name, 'xato_soni': j.xato_soni})
            now = timezone.now()
            one_year_ago = now - timedelta(days=365)
            six_months_ago = now - timedelta(days=30*6)
            three_months_ago = now - timedelta(days=30*3)
            one_month_ago = now - timedelta(days=30)
            one_week_ago = now - timedelta(days=7)
            one_day_ago = now - timedelta(days=1)
            statistics = []
            def calculate_statistics(start_date, end_date):
                data = []
                bulim = Bolim.objects.get(id=id)
                hisobots = Hisobot.objects.filter(xodim__bulimi=bulim, created_at__range=[start_date, end_date])
                total_xato_soni = 0
                total_butun_soni = 0
                total_mistakes = 0
                xato_foizi = 0
                butun_foizi = 0
                for hisobot in hisobots:
                    total_xato_soni += hisobot.xato_soni
                    total_butun_soni += hisobot.butun_soni
                    total_mistakes = total_xato_soni + total_butun_soni
                    xato_foizi = round((total_xato_soni * 100) / (total_mistakes) if total_mistakes else 0, 2)
                    butun_foizi = round((total_butun_soni * 100) / (total_mistakes) if total_mistakes else 0, 2)
                    # print(xato_foizi)
                    # print(butun_foizi)
                data.append({
                    'bulim_name': bulim.name,
                    'xato_soni': total_xato_soni,
                    'butun_soni': total_butun_soni,
                    'Xato_foizi': xato_foizi,
                    'Butun_foizi': butun_foizi,
                })
                return data
            statistics.append({'period': '1 year', 'data': calculate_statistics(one_year_ago, now)})
            statistics.append({'period': '6 months', 'data': calculate_statistics(six_months_ago, now)})
            statistics.append({'period': '3 months', 'data': calculate_statistics(three_months_ago, now)})
            statistics.append({'period': '1 month', 'data': calculate_statistics(one_month_ago, now)})
            statistics.append({'period': '1 week', 'data': calculate_statistics(one_week_ago, now)})
            statistics.append({'period': '1 day', 'data': calculate_statistics(one_day_ago, now)})
            return Response({'data':ser.data,
                         'statistic':a,
                         'mahsulot':c,
                         'xato': d,
                         'xodimlar':xodim.data,
                         'time_statistic':statistics,
                         })
        return Response({'data':ser.data,
                         'statistic':None,
                         'mahsulot':None,
                         'xato': None,
                         'xodimlar':None,
                         'time_statistic':None,
                         })
        # except:
        #     return Response({'message': "bu id xato"})
            
    def patch(self, request, id):
        bolim = Bolim.objects.get(id=id)
        serializer = BolimSerializer(bolim, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, id):
        user = request.user
        bulim = Bulim.objects.get(id=id)
        if user.is_admin==True or user.is_direktor==True:
            bulim.delete()
            return Response(status=204)
        return Response({'message':'Bulimni Siz Uchirolmaysiz, Uchirish Uchun Direktor Yoki Adminga Murojat Qiling'})


class MaxsulotView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request):
        maxsulot = Maxsulot.objects.all()
        l=[]
        for i in maxsulot:
            h = Hisobot.objects.filter(mahsulot=i)
            for j in h:
                found = False
                for item in l:
                    if item['mahsulot_name'] == j.mahsulot.name:
                        item['xato_soni'] += j.xato_soni
                        item['butun_soni'] += j.butun_soni
                        found = True
                        break
                if not found:
                    l.append({'id':j.mahsulot.id, 'mahsulot_id':j.mahsulot.mahsulot_id, 'mahsulot_name': j.mahsulot.name, 'xato_soni': j.xato_soni, 'butun_soni': j.butun_soni, 'Xato_foizi': None, 'Butun_foizi': None})
            for i in h:
                for item in l:
                    if item['mahsulot_name'] == i.mahsulot.name:
                        item['Xato_foizi'] = round(item['xato_soni']*100/(item['xato_soni'] + item['butun_soni']), 2)
                        item['Butun_foizi'] = round(item['butun_soni']*100/(item['xato_soni'] + item['butun_soni']), 2) 

        ser = MaxsulotSerializer(maxsulot, many=True)
        return Response({'statistics':l, 'data':ser.data})

    def post(self, request):
        serializer = MaxsulotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class MaxsulotDetail(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request, id):
        mahsulot = Maxsulot.objects.get(id=id)
        ser = MaxsulotSerializer(mahsulot)
        a = []
        missed = Hisobot.objects.filter(mahsulot=mahsulot)
        for j in missed:
            found = False
            for item in a:
                if item['xato_name'] == j.xato.name:
                    item['xato_soni'] += j.xato_soni
                    item['butun_soni'] += j.butun_soni
                    found = True
                    break
            if not found:
                a.append({'xato_name': j.xato.name , 'xato_soni': j.xato_soni, 'butun_soni': j.butun_soni})
        for i in missed:
            for item in a:
                if item['xato_name'] == i.xato.name:
                    item['Xato_foizi'] = round(item['xato_soni']*100/(item['xato_soni'] + item['butun_soni']), 2)
                    item['Butun_foizi'] = round(item['butun_soni']*100/(item['xato_soni'] + item['butun_soni']), 2) 
        return Response({'data':ser.data,
                         'statistic':a})

    def patch(self, request, id):
        maxsulot = Maxsulot.objects.get(id=id)
        serializer = MaxsulotSerializer(maxsulot, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, id):
        maxsulot = Maxsulot.objects.get(id=id)
        if request.user.is_tekshiruvchi == True or request.user.is_admin == True or request.user.is_direktor == True:
            maxsulot.delete()
        return Response({'message':'Siz Admin, Direktor yoki Tekshiruvchi emassiz'})


class ProblemView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request):
        problem = Problem.objects.all()
        ser = ProblemSerializer(problem, many=True)
        return Response(ser.data)
    
    def post(self, request):
        serializer = ProblemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class ProblemDetail(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request, id):
        try:
            problem = Problem.objects.get(id=id)
            ser = ProblemSerializer(problem)
            return Response(ser.data)
        except:
            return Response({'message': "bu id xato"})

    def patch(self, request, id):
        problem = Problem.objects.get(id=id)
        serializer = ProblemSerializer(problem, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, id):
        problem = Problem.objects.get(id=id)
        if request.user.is_tekshiruvchi == True or request.user.is_direktor==True or request.user.is_admin==True:
            problem.delete()
        return Response({'message':'Siz Admin, Direktor yoki Tekshiruvchi emassiz'})


class HisobotView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        hisobot = Hisobot.objects.all()
        ser = HisobotGetSerializer(hisobot, many=True)
        return Response(ser.data)

    def post(self, request):
        if request.data.get('xodim'):
            data = request.data
            data['user'] = request.user.id
            serializer = HisobotSerializer(data=data)
            if serializer.is_valid() and request.user.is_tekshiruvchi == True or request.user.is_admin == True or request.user.is_direktor == True:
                d = serializer.save()
                if data.get('photo'):
                    photo = data.getlist('photo', [])
                    for x in photo:
                        s = Photo.objects.create(photo=x)
                        d.photo.add(s)
                return Response(serializer.data)
            return Response({'error':serializer.errors, 'message':'Siz tekshiruvchi emassiz'})
        return Response({'message':'Xodim berilmagan'})


class HisobotDetail(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id):
        try:
            hisobot = Hisobot.objects.get(id=id)
            ser = HisobotSerializer(hisobot)
            return Response(ser.data)
        except:
            return Response({'message': "bu id xato"})
    
    def patch(self, request, id):
        a = request.data.getlist('photo', [])
        hisobot = Hisobot.objects.get(id=id)
        serializer = HisobotSerializer(hisobot, data = request.data, partial=True)
        if serializer.is_valid() and request.user.is_tekshiruvchi == True or request.user.is_admin == True or request.user.is_direktor == True:
            s = serializer.save()
            if a:
                for x in a:
                    n = Photo.objects.create(photo=x)
                    s.photo.add(n)
            return Response(serializer.data)
        return Response({'error':serializer.errors, 'message':'Siz Admin, Direktor yoki Tekshiruvchi emassiz'})
    
    def delete(self, request, id):
        hisobot = Hisobot.objects.get(id=id)
        if request.user.is_tekshiruvchi == True or request.user.is_direktor==True or request.user.is_admin==True:
            hisobot.delete()
            return Response({'message':'Hisobot muvvafaqiyatli o\'chirildi'})
        return Response({'message':'Siz Admin, Direktor yoki Tekshiruvchi emassiz'})


