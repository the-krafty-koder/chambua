from .tables import *
from django.shortcuts import render, HttpResponse, redirect
from .form import *
from .models import *
from visual.graphs import *
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required(login_url="/login/")
def submit_view(request):
    if request.method == "POST":
        form = submit_form(request.POST)
        teacher = teacher_form(request.POST)

        if form.is_valid():
            if teacher.is_valid():
                form_data = form.cleaned_data
                teach = teacher.cleaned_data
                search_existence(request.user, form_data['class_name'], form_data['stream_name'],form_data['classteacher_name'], form_data['exam_name'],sucess())
                teach = Teacher.objects.create(stream_name=form_data['stream_name'],teacher_list =
                {
                           "Mathematics":teach['Mathematics'],
                           "English":teach['English'],
                           "Kiswahili":teach['Kiswahili'],
                           "Physics":teach['Physics'],
                           "Chemistry":teach['Chemistry'],
                           "Biology":teach['Biology'],
                           "Geography":teach['Geography'],
                           "History":teach['History'],
                           "Business":teach['Business'],
                           "CRE":teach['CRE'],
                           "French":teach['French']})
                set_dataframe(request.user.name,form_data['class_name'], form_data['stream_name'],form_data['exam_name'], teach )

                return  redirect('/see')


    else:
        form = submit_form()
        teacher = teacher_form()

    return render(request, 'submission_table.html', {'form':form,
                                                     'teacher':teacher,
                                                     'submission_table':submit_app})

def complete(request):
    return HttpResponse("Data Submission completed")