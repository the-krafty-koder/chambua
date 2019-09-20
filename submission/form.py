from django import forms


class submit_form(forms.Form):
    exam_name = forms.CharField(max_length=50)
    class_name = forms.CharField(max_length=50)
    stream_name = forms.CharField(max_length=50)
    classteacher_name = forms.CharField(max_length=50)

class teacher_form(forms.Form):
    stream_name = forms.CharField(max_length=30)
    Mathematics = forms.CharField(max_length = 20)
    English = forms.CharField(max_length = 20)
    Kiswahili = forms.CharField(max_length = 20)
    Physics = forms.CharField(max_length = 20)
    Chemistry = forms.CharField(max_length=20)
    Biology = forms.CharField(max_length = 20)
    Geography = forms.CharField(max_length = 20)
    History = forms.CharField(max_length = 20)
    Business = forms.CharField(max_length=20)
    CRE = forms.CharField(max_length = 20)
    French = forms.CharField(max_length = 20)