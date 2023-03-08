from django.urls import path,include
from ansorapp.views import ValidatePhoneSendOTP,ValidateOTP,Register , CoursesAPIView


urlpatterns = [
    path('validate_form/', ValidatePhoneSendOTP.as_view(), name='validate_form'),
    path('validate_otp/', ValidateOTP.as_view(), name='validate_otp'),
    path('register/', Register.as_view(), name='register'),
    path('course/',CoursesAPIView.as_view(),name='Courses'),
    # path('applicant/',ApplicantAPIView.as_view(),name='Applicants'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # path('delete/<int:id>', PutCommentAPIView.as_view(), name='Update'),
    # path('CommentList/', CommentListAPIView.as_view(), name='CommentList'),
    # path('getusercomment/',GetUserCommentsAPIView.as_view()),
    # path('actors/',ActorAPIView.as_view(),name='Actors'),
    # path('movies/',MovieAPIView.as_view(),name='Movies'),
    # path('detmovie/<int:pk>',GetMovieAPIView.as_view(),name='GetMovie')

]