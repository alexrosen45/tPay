from django import forms

class PersonForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    student_number = forms.CharField(max_length=50)