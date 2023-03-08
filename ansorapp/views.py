from django.shortcuts import render
from django.http import Http404
from rest_framework import status
# status.HTTP_400_BAD_REQUEST
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
import random

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from ansorapp.models import (User, PhoneOTP, Courses, Rooms, Dates, Teacher, Themes, Groups, Students, Payments, Attendance)
from ansorapp.serializers import (ValidatePhoneSendOTPSerializer, ValidateOTPSerializer, CreateUserSerializer, 
                                  UserSerializer, CoursesSerializers, RoomsSerializers, DatesSerializers, TeacherSerializers, 
                                  ThemesSerializers, PostThemesSerializers, GroupsSerializers, StudentsSerializers, 
                                  PaymantsSerializers, AttendanceSerializers)


import requests


class RoomsAPIView(APIView):
    serializer_class=RoomsSerializers
    permission_classes=(IsAdminUser,)
    
    @swagger_auto_schema(request_body=RoomsSerializers)
    def post(self,request):
        serializer=RoomsSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response("Can't posted !")
    
    def get(self,request):
        rooms=Rooms.objects.all()
        serializer=RoomsSerializers(rooms,many=True)
        return Response(data=serializer.data)
    
    def put(self,request,id,*args, **kwargs):
        pass


class DatesAPIView(APIView):
    serializer_class=DatesSerializers
    permission_classes=(IsAdminUser,)
    
    @swagger_auto_schema(request_body=DatesSerializers)
    def post(self,request):
        serializer=DatesSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response("Can't posted !")
    
    def get(self,request):
        dates=Dates.objects.all()
        serializer=DatesSerializers(dates, many=True)
        return Response(data=serializer.data)
    
    def put(self,request,id,*args, **kwargs):
        pass

class TeacherAPIView(APIView):
    serializer_class=TeacherSerializers
    permission_classes=(IsAdminUser,)
    
    @swagger_auto_schema(request_body=TeacherSerializers)
    def post(self,request):
        serializer=TeacherSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response("Can't posted !")

    def get(self,request):
        teacher=Teacher.objects.all()
        serializer=TeacherSerializers(teacher, many=True)
        return Response(data=serializer.data)
    
    def put(self,request,id,*args, **kwargs):
        pass


class ThemesAPIView(APIView):
    serializer_class=PostThemesSerializers
    permission_classes=(IsAuthenticated,)
    
    @swagger_auto_schema(request_body=PostThemesSerializers)
    def post(self,request):
        serializer=PostThemesSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer_obj = serializer
            serializer_obj.save(user=request.user)
            return Response(data=serializer_obj.data)
        else:
            return Response("Can't posted !")
    
    def get(self,request):
        queryset=Themes.objects.filter(user=request.user)
        serializer_class=ThemesSerializers(queryset,many=True)
        return Response(serializer_class.data)
    
    def put(self,request):
        pass


class GroupAPIView(APIView):
    serializer_class=GroupsSerializers
    permission_classes=(IsAdminUser,)
    
    @swagger_auto_schema(request_body=GroupsSerializers)
    def post(self,request):
        serializer=GroupsSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response("Can't posted !")

    def get(self,request):
        group=Groups.objects.all()
        serializer=GroupsSerializers(group, many=True)
        return Response(data=serializer.data)
    
    def put(self,request,id,*args, **kwargs):
        pass
    

class StudentAPIView(APIView):
    serializer_class=StudentsSerializers
    permission_classes=(IsAdminUser,)
    
    @swagger_auto_schema(request_body=StudentsSerializers)
    def post(self,request):
        serializer=StudentsSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response("Can't posted !")

    def get(self,request):
        student=Students.objects.all()
        serializer=StudentsSerializers(student, many=True)
        return Response(data=serializer.data)
    
    def put(self,request,id,*args, **kwargs):
        pass
    

class PaymentAPIView(APIView):
    serializer_class=PaymantsSerializers
    permission_classes=(IsAdminUser,)
    
    @swagger_auto_schema(request_body=PaymantsSerializers)
    def post(self,request):
        serializer=PaymantsSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            serializer_obj=serializer
            payment_id=serializer_obj.data.get('id')
            payment=Payments.objects.get(pk=payment_id)
            if payment.default_payment==payment.current_payment:
                payment.current_payment.replace('Successful !')
                a=int(payment.default_payment)
                b=int(payment.all_payments)
                payment.all_payments.replace(f"{a+b}")
                payment.save()
                return Response("Successfully paid !")
            elif payment.default_payment!=payment.current_payment:
                return Response(data=serializer.data)
            else:
                return Response("replace() func isn't worked !")
            # comment.user.add((request.user.id))
            # comment.save()
        
            
        else:
            return Response("Can't posted !")

    def get(self,request):
        student=Payments.objects.all()
        serializer=PaymantsSerializers(student, many=True)
        return Response(data=serializer.data)
    
    def put(self,request,id,*args, **kwargs):
        pass


class AttendenceAPIView(APIView):
    serializer_class=AttendanceSerializers
    permission_classes=(IsAuthenticated,)
    
    @swagger_auto_schema(request_body=AttendanceSerializers)
    def post(self,request):
        serializer=AttendanceSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            #sms/alert to student func
            
            return Response(data=serializer.data)
        else:
            return Response("Can't posted !")

    def get(self,request):
        attend=Attendance.objects.all()
        serializer=AttendanceSerializers(attend, many=True)
        return Response(data=serializer.data)
    
    def put(self,request,id,*args, **kwargs):
        pass







class CoursesAPIView(APIView):
    serializer_class=CoursesSerializers
    permission_classes=(IsAdminUser,)
    @swagger_auto_schema(request_body=CoursesSerializers)
    def post(self,request):
        serializer=CoursesSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response('Cant posted !')
        
    def get(self,request):
        actors=Courses.objects.all()
        serializer=CoursesSerializers(actors,many=True)
        return Response(data=serializer.data)

# class ApplicantAPIView(APIView):
#     serializer_class=ApplicantsSerializer
#     permission_classes=(AllowAny,)
    
#     @swagger_auto_schema(request_body=ApplicantsSerializer)
#     def post(self,request):
#         serializer=ApplicantsSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             # serializer.save()
#             a=serializer.data
#             print(a.get('full_name'))
#             print(a.get('phone_num'))
#             b=Courses.objects.get(id=a.get('course'))
#             print(b)
            
#             bot_token='6066491939:AAEDBrclIjq88En5z-Vzy33IHCwjl6xOEsM'
#             url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
#             message_data=f"New Applicant:\n{a.get('full_name')}\n{a.get('phone_num')}\n{b}"
#             chat_id=1731117573
#             payload = {
#                 "text": message_data,
#                 "parse_mode": "HTML",
#                 "disable_web_page_preview": False,
#                 "disable_notification": False,
#                 "reply_to_message_id": 0,
#                 "chat_id": chat_id
#             }
#             headers = {
#                 "accept": "application/json",
#                 "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
#                 "content-type": "application/json"
#             }
#             response = requests.post(url, json=payload, headers=headers)
#             print(response.text)
            
#             return Response(data=serializer.data)
#         else:
#             return Response('Cant sent !')


# import requests
# bot_token=''
# url = "https://api.telegram.org/bot{bot_token}/sendMessage"
# message_data=f"New Applicant:\n{a.get('full_name')}\n{a.get('phone_num')}\n{b}"

# payload = {
#     "text": "Required",
#     "parse_mode": "Optional",
#     "disable_web_page_preview": False,
#     "disable_notification": False,
#     "reply_to_message_id": 0,
#     "chat_id": "Unknown Type: mixed type"
# }
# headers = {
#     "accept": "application/json",
#     "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
#     "content-type": "application/json"
# }

# response = requests.post(url, json=payload, headers=headers)

# print(response.text)


# https://api.telegram.org/bot{token}/{method}

# For example:

# https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/sendMessage
 



#Auth:

class ValidatePhoneSendOTP(APIView):
    serializer_class=ValidatePhoneSendOTPSerializer
    permission_classes=(AllowAny,)
    
    @swagger_auto_schema(request_body=ValidatePhoneSendOTPSerializer)
    def post(self,request):
        phone_number=request.data.get('phone')
        full_name=request.data.get('full_name')
        course=request.data.get('course')
        
        if phone_number and full_name and course:
            phone=str(phone_number)
            user=User.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response(
                    {
                        'status':False,
                        'detail':'this phone number already exist !',
                    }
                )
            else:
                key=send_otp(phone)
                if key:
                    old=PhoneOTP.objects.filter(phone__iexact=phone)
                    if old.exists():
                        old.first()
                    serializer=ValidatePhoneSendOTPSerializer(data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                    ootp= PhoneOTP.objects.get(phone__iexact=phone)
                    ootp.otp=key
                    ootp.save()
	
                    # PhoneOTP.objects.create(phone=phone,otp=key ,full_name=full_name , course=course )
                    
                    return Response(
                        {
                            'status':True,
                            'detail':'OTP sent successfully !',
                        }
                    )
                else:
                    return Response(
                        {
                            'status':False,
                            'detail':'sending otp error !',
                        }
                    )
        else:
            return Response(
                {
                    'status':False,
                    'detail':'phone number is not given post request !'
                }
            )



def send_otp(phone):
    if phone:
        key = random.randint(99999, 999999)
        print(key)
        return key
    else:
        return False


class ValidateOTP(APIView):
    serializer_class=ValidateOTPSerializer
    permission_classes=(AllowAny,)

    @swagger_auto_schema(request_body=ValidateOTPSerializer)
    def post(self,request):
        phone=request.data.get('phone',False)
        otp_send=request.data.get('otp',False)
        
        if phone and otp_send:
            old=PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old=old.first()
                otp=old.otp
                if str(otp_send)==str(otp):
                    full_name=old.full_name
                    phone_num=old.phone
                    subject=old.course_id
                    
                    bot_token='6066491939:AAEDBrclIjq88En5z-Vzy33IHCwjl6xOEsM'
                    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                    message_data=f"New Applicant:\n{full_name}\n{phone_num}\n{subject}"
                    chat_id=1731117573
                    payload = {
                        "text": message_data,
                        "parse_mode": "HTML",
                        "disable_web_page_preview": False,
                        "disable_notification": False,
                        "reply_to_message_id": 0,
                        "chat_id": chat_id
                    }
                    headers = {
                        "accept": "application/json",
                        "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
                        "content-type": "application/json"
                    }
                    response = requests.post(url, json=payload, headers=headers)
                    print(response.text)
                    
                    old.validated=True
                    old.delete()
                    return Response(
                        {
                            'status':True,
                            'detail':'OTP matched. Please proceed for registration !',
                        }
                    )
                else:
                    return Response(
                        {
                            'status':False,
                            'detail':'OTP INCORRECT !',
                        }
                    )
            else:
                return Response(
                    {
                        'status':False,
                        'detail':'First proceed via sending otp request !',
                    }
                )
        else:
            return Response({
                'status': False,
                'detail': 'please provide both phone and OTP for validation !',
            })


class Register(APIView):
    serializer_class=CreateUserSerializer
    permission_classes=(IsAdminUser,)
    
    @swagger_auto_schema(request_body=CreateUserSerializer)
    def post(self,request):
        phone=request.data.get('phone',False)
        password=request.data.get('password',False)
        username=request.data.get('username',False)
        if phone and password:
            # old=PhoneOTP.objects.filter(phone__iexact=phone)
            # if old.exists():
            #     old=old.first()
            #     validated=old.validated
            #     data=request.data
                # if validated:
            data=request.data
            reg_serializer=CreateUserSerializer(data=data)
            if reg_serializer.is_valid():
                password=reg_serializer.validated_data.get('password')
                reg_serializer.validated_data['password']=make_password(password)
                new_user=reg_serializer.save()
                # old.delete()
                return Response(
                    {
                        'status':True,
                        'detail':'Account successfuly created !'
                    }
                )
            else:
                return Response(
                    {
                        'status':False,
                        'detail':"OTP haven't verified .First do that step !"
                    }
                )
                        
        # else:
        #     return Response(
        #         {
        #             'status':False,
        #             'detail':'please verify phone first !',
        #         }
        #     )
        else:
            return Response(
                {
                    'status': False,
                    'datail': "Both Phone and password are not sent !",
                }
            )