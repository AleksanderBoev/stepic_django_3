from django.shortcuts import render
from vacancies.models import Company
from vacancies.models import Specialty
from vacancies.models import Vacancy
from django.http import Http404, HttpResponseServerError



def company_view(request, company_id):
    try:
        company_data = Company.objects.get(id=company_id)
        return render(request, 'companies/companies.html', {
            'company': company_data,
        })
    except Company.DoesNotExist:
        raise Http404
    except Exception as error:
        return HttpResponseServerError('''<br><h1>The error on server</h1>''')



def main_view(request):
    try:
        return render(request, 'index.html', {
            'companies': Company.objects.all(),
            'vacancies': Vacancy.objects.all(),
            'specialty': Specialty.objects.all(),
        })
    except Exception as error:
        return HttpResponseServerError('''<br><h1>The error on server</h1>''')


def vacancy_view(request, vacancy_id):
    try:
        return render(request, 'vacancy/vacancy.html', {
            'vacancy': Vacancy.objects.get(id=vacancy_id)
        })
    except Vacancy.DoesNotExist:
        raise Http404
    except Exception as error:
        return HttpResponseServerError('''<br><h1>The error on server</h1>''')


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
