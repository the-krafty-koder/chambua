from django.shortcuts import render
from .graphs import *
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="/login/")
def visual(request):
    return  render(request, 'see.html', {'dropdown':graph().get_dropdown(),
                                         'donut':graph().get_donut(),
                                         'scatter':graph().get_scatter(),
                                         'scatter_arts':graph().get_scatter_arts(),
                                         'scatter_math': graph().get_scatter_math(),
                                         'interactive': graph().get_interactive(),
                                         "gradeA":graph().number()["A"],
                                         "gradeB":graph().number()["B"],
                                         "gradeC":graph().number()["C"],
                                         "gradeD":graph().number()["D"],
                                         "gradeE":graph().number()["E"],
                                         "high1":graph().improve()["high1"],
                                         "high2":graph().improve()["high2"],
                                         "high3":graph().improve()["high3"],
                                         "weight1":graph().str_wk()["weight1"],
                                         "weight2": graph().str_wk()["weight2"],
                                         "weight3":graph().str_wk()["weight3"],
                                         "weight4":graph().str_wk()["weight4"],
                                         "top":graph().details()["top"],
                                         "Mean":graph().details()["Mean"],
                                         "Last":graph().details()["Last"]})
@login_required(login_url="/login/")
def subj_view(request):
    return render(request,'subj.html',{"subj_interactive":graph().get_subj_interactive(),
                                       "interactive":graph().get_teacher_ranking(),
                                       "chem":graph().corry()["Chem"],
                                       "eng":graph().corry()["Eng"],
                                       "weight3": graph().str_wk()["weight3"],
                                       "weight4": graph().str_wk()["weight4"],
                                       "low1":graph().improve()["low1"],
                                       "low2":graph().improve()["low2"]},)
