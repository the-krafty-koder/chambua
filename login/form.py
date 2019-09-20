from django import forms

class login_form(forms.Form):
    name = forms.CharField(max_length=45)
    institution_id = forms.IntegerField()
    attrs = {
        "type": "password"
    }

    password = forms.CharField(min_length=8,widget=forms.TextInput(attrs=attrs))


class signup_form(forms.Form):
    institution_name = forms.CharField(max_length=45)
    email = forms.EmailField()
    attrs = {
        "type": "password"
    }

    password = forms.CharField(min_length=8,widget=forms.TextInput(attrs=attrs))
