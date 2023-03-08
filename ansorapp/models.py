from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

# Create your models here.

class Rooms(models.Model):
    room=models.CharField(max_length=50 , verbose_name='Rooms')
    
    def __str__(self):
        return self.room

class Dates(models.Model):
    date=models.CharField(max_length=20 , verbose_name='Course date')
    
    def __str__(self):
        return self.date

class Courses(models.Model):
    course_name=models.CharField(max_length=100 , verbose_name='Course title')

    def __str__(self):
        return self.course_name

# class Applicants(models.Model):
#     # full_name=models.CharField(max_length=50 , verbose_name='Applicant Full Name')
#     # phone_num=models.CharField(max_length=13,verbose_name='Applicant phone number')
#     # course=models.ForeignKey(Courses,on_delete=models.CASCADE , verbose_name='Course type')
    
#     def __str__(self):
#         return self.full_name



class UserManager(BaseUserManager):
    def create_user(self,phone,password=None,is_staff=False,is_active=True,is_admin=False):
        if not phone:
            raise ValueError('Users must have a phone number')
        if not password:
            raise ValueError('Users must have a password')
        
        user_obj=self.model(phone=phone)
        user_obj.set_password(password)
        # user_obj.username=username
        user_obj.staff=is_staff
        user_obj.admin=is_admin
        user_obj.active=is_active
        user_obj.save(using=self._db)
        return user_obj
    
    def create_staffuser(self,phone,password=None):
        user=self.create_user(phone,password=password,is_staff=True)
        return user
    
    def create_superuser(self, phone, password=None):
        user = self.create_user(phone=phone,password=password,is_staff=True,is_admin=True)
        return user
    

class User(AbstractBaseUser):
    phone_regex=RegexValidator(regex=r'^\+?1?\d{9,14}$',message="Phone number nust be entered in the format: '+998906417999'. Up to 14 digits allowed")
    phone=models.CharField(validators=[phone_regex],max_length=20,unique=True)
    # photos=models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True , verbose_name="Rasm")
    first_login=models.BooleanField(default=False)
    active=models.BooleanField(default=True)
    staff=models.BooleanField(default=False)
    admin=models.BooleanField(default=False)
    # comment=models.ForeignKey(Comment,on_delete=models.CASCADE)
    username=None #models.CharField(max_length=20,blank=True,verbose_name='username')
    USERNAME_FIELD='phone'
    REQUIRED_FIELDS=[]
    
    objects=UserManager()
    
    def __str__(self):
        return self.phone
    
    def get_full_name(self):
        if self.phone:
            return self.phone
    
    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active

class PhoneOTP(models.Model):
    phone_regex=RegexValidator(regex=r'^\+?1?\d{9,14}$',message="Phone number nust be entered in the format: '+998906417999'. Up to 14 digits allowed")
    phone=models.CharField(validators=[phone_regex],max_length=20,unique=True)
    otp=models.CharField(max_length=6,blank=True,null=True)
    validated=models.BooleanField(default=False,help_text='if it is true,that means user have validate otp correctly i second API')
    
    full_name=models.CharField(max_length=50 , verbose_name='Applicant Full Name',blank=True,null=True)
    # phone_num=models.CharField(max_length=13,verbose_name='Applicant phone number')
    course_id=models.ForeignKey(Courses,on_delete=models.CASCADE , verbose_name='Course type',blank=True,null=True)
    
    def __str__(self):
        return str(self.phone) + ' if sent ' + str(self.otp)



class Teacher(models.Model):
    phone_regex=RegexValidator(regex=r'^\+?1?\d{9,14}$',message="Phone number nust be entered in the format: '+998906417999'. Up to 14 digits allowed")
    full_name=models.CharField(max_length=50 , verbose_name='Teacher Full Name')
    phone_num=models.CharField(validators=[phone_regex] , max_length=13 , verbose_name='Teacher phone number' , unique=True)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.full_name

class Themes(models.Model):
    day=models.CharField(max_length=3 , verbose_name='Theme Number')
    theme=models.CharField(max_length=200 , verbose_name='Theme name')
    # teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)

class Groups(models.Model):
    name=models.CharField(max_length=50 , verbose_name='Group Name')
    room_id=models.ForeignKey(Rooms , on_delete=models.CASCADE , verbose_name='Group room')
    teacher_id=models.ManyToManyField(Teacher)
    course_id=models.ForeignKey(Courses,on_delete=models.CASCADE , verbose_name='Group subject')
    time=models.TimeField()
    date_id=models.ForeignKey(Dates,on_delete=models.CASCADE , verbose_name='Group date')
    
    def __str__(self):
        return self.name

class Students(models.Model):
    phone_regex=RegexValidator(regex=r'^\+?1?\d{9,14}$',message="Phone number nust be entered in the format: '+998906417999'. Up to 14 digits allowed")
    full_name=models.CharField(max_length=50 , verbose_name='Student Full Name')
    group_id=models.ManyToManyField(Groups)
    # payment=models.CharField(max_length=10 , verbose_name='Student payments')
    phone_num1=models.CharField(validators=[phone_regex] , max_length=13 , verbose_name='Student first phone number' , unique=True)
    phone_num2=models.CharField(validators=[phone_regex] , max_length=13 , verbose_name='Student second phone number' , unique=True)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)

    
    
    def __str__(self):
        return self.full_name
    

# class StudentPayments(models.Model): # bunda birmarta default , kegin faqat update ishlatiladi
#     default_payment=models.CharField(max_length=10 , verbose_name='Student Payments')#agar current defaultga teng bosa current success ! bolad
#     current_payment=models.CharField(max_length=10 , verbose_name='Student Payments' , null=True)
#     all_payments=models.CharField(max_length=10 , verbose_name='Student Payments' , null=True) #hozirjagacha ja'mi to'lovlar summasi
#     present = models.BooleanField(default=False , verbose_name='student payment')#agar bool bosilsa to'lov success bo'ladi va all payment o'zgarmaydi !(bu asosan grant/ehson yoki yordam uchun)
#     user=models.ForeignKey(User,on_delete=models.CASCADE)#vaqt qo'shish kerak !

# class TeacherPayments(models.Model):
#     default_payment=models.CharField(max_length=10 , verbose_name='Student Payments')#agar current defaultga teng bosa current success ! bolad
#     current_payment=models.CharField(max_length=10 , verbose_name='Student Payments' , null=True)
#     all_payments=models.CharField(max_length=10 , verbose_name='Student Payments' , null=True) #hozirjagacha ja'mi to'lovlar summasi
#     present = models.BooleanField(default=False , verbose_name='student payment')#agar bool bosilsa to'lov success bo'ladi va all payment o'zgarmaydi !(bu asosan jarima yoki o'qtuvchi ehsoni)
#     user=models.ForeignKey(User,on_delete=models.CASCADE)#vaqt qo'shish kerak !


class Payments(models.Model): # bunda birmarta default , kegin faqat update ishlatiladi
    default_payment=models.CharField(max_length=10 , verbose_name='Student Payments')#agar current defaultga teng bosa current success ! bolad
    current_payment=models.CharField(max_length=10 , verbose_name='Student Payments' , null=True)# qilingan to'lov yoki o'tkazilgan to'lov
    all_payments=models.CharField(max_length=10 , verbose_name='Student Payments' , null=True) #hozirjagacha ja'mi to'lovlar summasi
    present = models.BooleanField(default=False , verbose_name='student payment')#agar bool bosilsa to'lov success bo'ladi va all payment o'zgarmaydi !(bu asosan grant/ehson yoki yordam uchun)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)#vaqt qo'shish kerak !
    
    def __str__(self):
        return f"{self.user_id.phone} -> {self.current_payment} / {self.default_payment} -> {self.present}"


class Attendance(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    theme_id=models.ForeignKey(Themes,on_delete=models.CASCADE)
    # teacher_id=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    present = models.BooleanField(default=True , verbose_name='student_attendance')
    
    def __str__(self):
        return f"{self.student_id.full_name} {self.course_id} {self.date} {self.present}"



# class Check(models.Model):
    
#     FRESHMAN = 'FR'
#     SOPHOMORE = 'SO'
#     JUNIOR = 'JR'
#     SENIOR = 'SR'
#     GRADUATE = 'GR'
#     YEAR_IN_SCHOOL_CHOICES = [
#         (FRESHMAN, 'Freshman'),
#         (SOPHOMORE, 'Sophomore'),
#         (JUNIOR, 'Junior'),
#         (SENIOR, 'Senior'),
#         (GRADUATE, 'Graduate'),
#     ]
    
#     # nb=models.IntegerField()
#     nbc=models.DateField()
#     group=models.ForeignKey(Groups , on_delete=models.CASCADE)
#     teacher=models.ForeignKey()
#     student=models.ForeignKey()
    
#     def __str__(self):
#         return self.nbc


# {
#     'sana':[id , tema , bool]
# }



    