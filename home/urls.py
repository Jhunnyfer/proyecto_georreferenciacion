from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.uploadStudents),
    path('students', views.listStudents),
    path('viewstudent/<int:id>', views.viewStudent),
    path('editstudent/<int:id>', views.editStudent),
    path('studentsmap', views.listStudentsMap),
    path('studentsupload', views.uploadStudents),
]
