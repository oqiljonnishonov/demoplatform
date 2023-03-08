from rest_framework import serializers
from django.forms import ValidationError
from  ansorapp.models import (User, PhoneOTP, Courses, Rooms, Dates, Teacher, Themes, 
                              Groups, Students, Payments, Attendance)



class CoursesSerializers(serializers.ModelSerializer):
    class Meta:
        model=Courses
        fields=('id','course_name')

class RoomsSerializers(serializers.ModelSerializer):
    class Meta:
        model=Rooms
        fields=('id','room')

class DatesSerializers(serializers.ModelSerializer):
    class Meta:
        model=Dates
        fields=('id','date')

# class PostTeacherSerializers(serializers.ModelSerializer):
#     class Meta:
#         model=Teacher
#         fields=('id','full_name','phone_num')

class TeacherSerializers(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields=('id','full_name','phone_num','user_id')

class PostThemesSerializers(serializers.ModelSerializer):
    class Meta:
        model=Themes
        fields=('id','day','theme')

class ThemesSerializers(serializers.ModelSerializer):
    class Meta:
        model=Themes
        fields=('id','day','theme','user_id')

class GroupsSerializers(serializers.ModelSerializer):
    class Meta:
        model=Groups
        fields=('id','name','room_id','teacher_id','course_id','time','date_id')

class StudentsSerializers(serializers.ModelSerializer):
    class Meta:
        model=Students
        fields=('id','full_name','group_id','phone_num1','phone_num2','user_id')

# class PostStudentsSerializers(serializers.ModelSerializer):
#     class Meta:
#         model=Students
#         fields=('id','full_name','group_id','phone_num1','phone_num2')

# class DefaultPaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Payments
#         fields=('id','default_payment')

class PaymantsSerializers(serializers.ModelSerializer):
    class Meta:
        model=Payments
        fields=('id','default_payment','current_payment','all_payments','present','user_id')

class AttendanceSerializers(serializers.ModelSerializer):
    class Meta:
        model=Attendance
        fields=('id','student_id','course_id','theme_id','date','present')

# class StudentPeymantsSerializers(serializers.ModelSerializer):
#     class Meta:
#         model=Payments
#         fields=('id','default_payment','current_payment','all_payments','present','user')

# class StudentPeymantsSerializers(serializers.ModelSerializer):
#     class Meta:
#         model=Attendance
#         fields=('id','student','course','theme','date','present')




# class ApplicantsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Applicants
#         fields=('id','full_name','phone_num','course')






class ValidatePhoneSendOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneOTP
        fields = ('full_name','phone','course_id')

class ValidateOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneOTP
        fields = ('phone', 'otp',)

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('phone','password')
        extra_kwargs={'password':{'write_only':True}}

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','phone')

# def validate_birthdate(self,data):
#             if data<data.fromisoformat('1950-01-01'):
#                 raise ValidationError(detail="Incorrect Data")
#             return data