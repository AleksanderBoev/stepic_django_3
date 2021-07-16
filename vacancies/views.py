from django.shortcuts import render


def company_view(request, company_id):
    return render(request, 'companies/companies.html')


def main_view(request, company_id):
    return render(request, 'index.html')


def vacancy_view(request, vacancy_id):
    return render(request, 'vacancy/vacancy.html')


def vacancies_view(request, vacancies_path=None):
    return render(request, 'vacancies/')
