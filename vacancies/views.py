from django.shortcuts import render
from vacancies.models import Company
from vacancies.models import Specialty
from vacancies.models import Vacancy
from django.http import Http404, HttpResponseServerError
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
import django_vacancies.settings as settings
from django.contrib.auth.models import User
from django import forms
from django.views.generic import ListView

class vacancy_edit_form(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('title',
                  #'specialty',
                  'skills',
                  'description',
                  'salary_min',
                  'salary_max',
                  )

def mycompany_vacancy_create_view(request, vacancy_id=None, **kwargs):
    if kwargs['new']:
        data = Vacancy()
    else:
        data = Vacancy.objects.get(id=vacancy_id)
    if request.method.upper() == 'POST':
        form_data = vacancy_edit_form(request.POST)
        if form_data.is_valid():
            print(True, form_data.cleaned_data)
            form_data = form_data.save(commit=False)
            form_data.specialty = Specialty.objects.get(code=request.POST.get('specialty'))
            form_data.company = Company.objects.get(owner__username=request.user)
            form_data.save()
        else:
            print(form_data.errors)
            print(request.POST.get('specialty'))
    return render(request, 'companies/vacancy-edit.html', {
            'vacancy': data,
            'specialty': Specialty.objects.all(),
        })

class mycompany_vacancies_view(ListView):
    model = Vacancy
    template_name ='companies/vacancy-list.html'
    def get_queryset(self):
        return Vacancy.objects.filter(company__owner__username=self.request.user)

class mycompany_edit_form(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name',
                  'location',
                  'description',
                  'employee_count',
                  )

def mycompany_edit_view(request, **kwargs):
    data = Company.objects.filter(owner=User.objects.get(username=request.user))
    #print('ddd',data.first().owner)
    if request.method.upper() == 'POST':
        updata_data = mycompany_edit_form(request.POST)
        if updata_data.is_valid():
            updata_data = updata_data.save(commit=False)
            updata_data.owner = User.objects.get_by_natural_key(username=request.user)
            if data.count() and request.FILES.get('logo') is None:
                print('dd')
                updata_data.logo = data.first().logo
            else:
                updata_data.logo = request.FILES.get('logo') or '/company_images/default.png'
            if data.count():
                print('logo', updata_data.logo)
                Company.objects.filter(owner=User.objects.get(username=request.user)).update(
                    name=updata_data.name,
                    location=updata_data.location,
                    logo=updata_data.logo,
                    description=updata_data.description,
                    employee_count=updata_data.employee_count,
                    owner=User.objects.get(username=request.user),
                )
            else:
                updata_data.save()
            reneder_data = updata_data
        else:
            print(repr(updata_data.errors))
            reneder_data = updata_data.cleaned_data
        return render(request, 'companies/company-edit.html', {
            'company': reneder_data,
            'form': updata_data,
        })
    print(request.META.get('HTTP_REFERER'))
    if data.count() == 0 and '/mycompany/letsstart' not in (request.META.get('HTTP_REFERER') or ''):
        return HttpResponseRedirect('/mycompany/letsstart')
    elif kwargs['new'] and data.count():
        return HttpResponseRedirect('/mycompany')
    return render(request, 'companies/company-edit.html', {
        'company': data.first(),
        'form': mycompany_edit_form,
    })

def mycompany_letsstart_view(request):
    return render(request, 'companies/company-create.html')
def mycompany_vacancy_view(request):
    return render(request, 'companies/company-create.html')

def company_view(request, company_id):
    try:
        company_data = Company.objects.get(id=company_id)
        return render(request, 'companies/companies.html', {
            'company': company_data,
        })
    except Company.DoesNotExist:
        raise Http404



def main_view(request):
    print(User.objects.filter(username=request.user).count())
    return render(request, 'index.html', {
        'companies': Company.objects.all(),
        'vacancies': Vacancy.objects.all(),
        'specialty': Specialty.objects.all(),
    })


def vacancy_view(request, vacancy_id):
    if request.method.upper() == 'POST':
        print('sss')
        print(request.POST.get('userName'))
        return render(request, 'vacancy/send.html', {
            'vacancy_id': vacancy_id,
            'picture_rout': settings.MEDIA_URL + '/check.png',
        })
    try:
        return render(request, 'vacancy/vacancy.html', {
            'vacancy': Vacancy.objects.get(id=vacancy_id),
        })
    except Vacancy.DoesNotExist:
        raise Http404


def vacancies_view(request, vacancies_path=None):
    try:
        if vacancies_path is None:
            vacancies = Vacancy.objects.all()
        else:
            vacancies = Vacancy.objects.filter(specialty__code=vacancies_path)
            if vacancies.count() == 0:
                raise Http404
        return render(request, 'vacancies/vacancies.html', {
            'vacancies': vacancies,
        })
    except Http404:
        raise Http404
    except Exception as error:
        return HttpResponseServerError('''<br><h1>The error on server</h1>''')
