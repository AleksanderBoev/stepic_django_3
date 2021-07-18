from django.shortcuts import render
from vacancies.models import Company
from vacancies.models import Specialty
from vacancies.models import Vacancy
from django.db.models import Count, Variance

def company_view(request, company_id):
    company_data = Company.objects.get(id=company_id)
    return render(request, 'companies/companies.html', {
        'company': company_data,
    })


def main_view(request):
    return render(request, 'index.html', {
        'companies': Company.objects.all(),
        'vacancies': Vacancy.objects.all(),
        'specialty': Specialty.objects.all(),
    })


def vacancy_view(request, vacancy_id):
    return render(request, 'vacancy/vacancy.html', {
        'vacancy': Vacancy.objects.get(id=vacancy_id)
    })


def vacancies_view(request, vacancies_path=None):
    print(vacancies_path)
    if vacancies_path is None:
        vacancies = Vacancy.objects.all()
    else:
        vacancies = Vacancy.objects.filter(specialty__code=vacancies_path)
    return render(request, 'vacancies/vacancies.html', {
        'vacancies': vacancies,
    })
