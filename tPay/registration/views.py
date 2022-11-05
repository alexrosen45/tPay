from django.http import HttpResponse
from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.shortcuts import render
from registration.models import Person

from .forms import PersonForm

def registration(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PersonForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # save valid form data to database
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            student_number = form.cleaned_data['student_number']
            person = Person(first_name=first_name, last_name=last_name, student_number=student_number)
            person.save()

            # redirect to a new URL:
            return render(request, "registration/registration_complete.html", {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PersonForm()

    return render(request, "registration/registration.html", {'form': form})