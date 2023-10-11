import os
import uuid
import datetime
import csv
import json
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from .forms import UploadFileForm
from django.db import models
from django.contrib.auth.models import User
import googlemaps


def index(request):
    if validate_is_authenticated(request) == True:
        students_count = Estudiantes.objects.all().count()
        users_count = User.objects.all().count()
        return render(request, 'pages/index.html', {"users_count": users_count, "students_count": students_count})
    else:
        return redirect("/accounts/login/")

###Lista de estudiantes
def listStudents(request):
    if validate_is_authenticated(request) == True:
        students_list = Estudiantes.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(students_list, 20)
        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)
        return render(request, "pages/students.html", {"students": students})
    else:
        return redirect("/accounts/login/")


def listStudentsMap(request):
    if validate_is_authenticated(request) == True:
        #
        students = None
        if request.method == 'POST':
            students = Estudiantes.objects.filter(promedio_acumulado__range=(request.POST.get('min'), request.POST.get('max')))
        else:
            students = Estudiantes.objects.all()
        
        return render(request, "pages/studentsMap.html", {"students": students})
    else:
        return redirect("/accounts/login/")


def viewStudent(request, id):
    if validate_is_authenticated(request) == True:
        student = Estudiantes.objects.get(id=id)
        return render(request, "pages/view_student.html", {"student": student})
    else:
        return redirect("/accounts/login/")


def editStudent(request, id):
    if validate_is_authenticated(request) == True:
        if request.method == 'POST':
            '''form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                process_file_upload(handle_uploaded_file(request.FILES['file']))
                response = redirect("/studentsupload")
                response.set_cookie('correct', 'correct',10)
                return response'''
            print("Welcome")
        else:
            student = Estudiantes.objects.get(id=id)
            return render(request, "pages/edit_student.html", {"student": student})
    else:
        return redirect("/accounts/login/")


def handle_uploaded_file(f):
    now = datetime.datetime.now()
    nameFile = str(uuid.uuid1())[:8] + "_" + str(now.strftime("%Y%m%d%H%M%S")) + '.csv'
    with open('static/uploads/' + nameFile , 'wb+', encoding='utf-8') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return nameFile


def process_file_upload(nf):
    gmaps = googlemaps.Client(key=os.getenv('SECRET_KEY_GOOGLE'     , None))
    with open("static/uploads/" + nf, 'r') as file:
        csvreader = csv.DictReader(file, delimiter=";")
        for row in csvreader:
            result = json.dumps(gmaps.geocode(str(row['direccion'] +', Medellin, Colombia')))
            result2 = json.loads(result)
            i = Estudiantes()
            i.identificacion = row['identificacion']
            i.nombres = row['nombres']
            i.apellidos = row['apellidos']
            i.genero = row['genero']
            i.fecha_nacimiento = row['fecha_nacimiento']
            i.correo_electronico = row['correo_electronico']
            i.telefono = row['telefono']
            i.comuna = row['comuna']
            i.barrio = row['barrio']
            i.direccion = row['direccion']
            i.estrato = row['estrato']
            i.carrera = row['carrera']
            i.dir_latitude = result2[0]['geometry']['location']['lat']
            i.dir_longitude = result2[0]['geometry']['location']['lng']
            i.facultad = row['facultad']
            i.creditos_aprobados = row['creditos_aprobados']
            i.promedio_acumulado = row['promedio_acumulado']
            i.save()
    

def uploadStudents(request):
    
    if validate_is_authenticated(request) == True:
        if "correct" in request.COOKIES.keys() :
            correct = 1
        else:
            correct = 0

        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                process_file_upload(handle_uploaded_file(request.FILES['file']))
                response = redirect("/studentsupload")
                response.set_cookie('correct', 'correct',10)
                return response
        else:
            form = UploadFileForm()
        return render(request, 'pages/upload_student.html', {'form': form, 'correct' : correct})
    else:
        return redirect("/accounts/login/")


def validate_is_authenticated(request):
    if request.user.is_authenticated:
        return True
    else:
        return False
    