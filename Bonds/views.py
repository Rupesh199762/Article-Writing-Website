from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse 
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.conf import settings
import pandas as pd
import os
from .models import BondModel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate
from django.contrib import messages
from authentication.models import Comment, ACModel

# Create your views here.
def home(request):
    template = loader.get_template('bond\index.html')
    data = BondModel.objects.values_list('name_of_political_party',flat=True).distinct()
    lables = [party_name for party_name in data]
    values = [(BondModel.objects.filter(name_of_political_party=party_name).count()) for party_name in data]
    money = []
    for party in lables:
        total_amount = 0
        get_amount = BondModel.objects.filter(name_of_political_party=party)
        for amount in get_amount:
            total_amount = total_amount + amount.denomination
        money.append(total_amount)
    data_2 = BondModel.objects.values_list('short_name',flat=True).distinct()
    short_lable = [party for party in data_2]
    
    current_page_name = request.get_full_path()
    context = {
        'labels': lables,
        'short_lable':short_lable,
        'values': values,
        'money': money,
        'current_url' : current_page_name
    }
    return HttpResponse(template.render(context,request))

def user_page(request,session_id):
    userName = request.session.get('user_name')
    if userName:
        user = User.objects.get(username = userName)
    return home(request)
    
# def detailed_view(request):
#     template = loader.get_template('bond\details.html')
#     partyList = [party for party in BondModel.objects.values_list('name_of_political_party',flat=True).distinct()]

#     if request.method == 'POST':
#         party_name = request.POST['party_list']
#         company_name = request.POST['company_list']
#         bondId = request.POST['bond_list']

#         if party_name != "Select Party Name" and company_name =="-select party-" and bondId == '-select party-':
#             data = BondModel.objects.filter(name_of_political_party=party_name)
#             paginator = Paginator(data, 10)  # Number of items per page
#             page_number = request.GET.get('page')
#             try:
#                 page_obj = paginator.page(page_number)
#             except PageNotAnInteger:
#                 page_obj = paginator.page(1)
#             except EmptyPage:
#                 page_obj = paginator.page(paginator.num_pages)
#             total = 0 
#             for dt in data:
#                 total = total + dt.denomination
#             context = {
#                 'Data':data,
#                 'PartyName':party_name,
#                 'partyList':partyList,
#                 'total_amount':total,
#                 'page_obj':page_obj
#             }
#             return HttpResponse(template.render(context,request))

#     elif 'name' in request.GET:
#         Name = request.GET['name']
#         data = BondModel.objects.filter(name_of_political_party=Name)
#         paginator = Paginator(data, 10)  # Number of items per page
#         page_number = request.GET.get('page')
#         try:
#             page_obj = paginator.page(page_number)
#         except PageNotAnInteger:
#             page_obj = paginator.page(1)
#         except EmptyPage:
#             page_obj = paginator.page(paginator.num_pages)
#         total = 0 
#         for dt in data:
#             total = total + dt.denomination
#         context = {
#             'Data':data,
#             'partyList':partyList,
#             'PartyName':Name,
#             'total_amount':total,
#             'page_obj':page_obj
#         }
#         return HttpResponse(template.render(context,request))

#     return HttpResponse(template.render())


def detailed_view(request):
    template = loader.get_template('bond\details.html')
    partyList = [party for party in BondModel.objects.values_list('name_of_political_party',flat=True).distinct()]
    if request.method == 'POST':
        party_name = request.POST['party_list']
        company_name = request.POST['company_list']
        bondId = request.POST['bond_list']
        ls = getting_data(request,party_name)

        if party_name != "" and (company_name =="" or company_name == "All") and (bondId == "" or bondId == "All"):
            data = BondModel.objects.filter(name_of_political_party=party_name)

        elif party_name != "" and (company_name !="" or company_name != "All") and (bondId == "" or bondId == "All"):
            data = BondModel.objects.filter(name_of_political_party=party_name,name_of_purchaser=company_name)

        elif party_name != "" and (company_name == "All") and (bondId != "" or bondId != "All"):
            data = BondModel.objects.filter(bond_id=bondId)

        elif party_name != "" and (company_name !="" or company_name != "All") and (bondId != "" or bondId != "All"):
            data = BondModel.objects.filter(bond_id=bondId)
        
        else:
             messages.success(request,'Somthing Went Wrong!')

        lables = ls[0]
        values = ls[1]
    
        paginator = Paginator(data, 10)  # Number of items per page
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        total = 0 
        for dt in data:
            total = total + dt.denomination
        
        context = {
            'lables':lables,
            'values':values,
            'Data':data,
            'partyList':partyList,
            'PartyName':party_name,
            'total_amount':total,
            'page_obj':page_obj
        }
        return HttpResponse(template.render(context,request))

    elif 'name' in request.GET:
        party_name = request.GET['name']
        data = BondModel.objects.filter(name_of_political_party=party_name)

        ls = getting_data(request,party_name)
        lables = ls[0]
        values = ls[1]
    
        paginator = Paginator(data, 10)  # Number of items per page
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        total = 0 
        for dt in data:
            total = total + dt.denomination
        
        context = {
            'lables':lables,
            'values':values,
            'Data':data,
            'partyList':partyList,
            'PartyName':party_name,
            'total_amount':total,
            'page_obj':page_obj
        }
        return HttpResponse(template.render(context,request))

def get_company_list(request):
    val = request.GET.get('selected_value')
    items = BondModel.objects.filter(name_of_political_party=val).values_list('name_of_purchaser',flat=True).distinct()
    options = [item for item in items]
    return JsonResponse(options, safe=False)

def get_bond_list(request):
    val1 = request.GET.get('selected_company_name')
    val2 = request.GET.get('selected_party_name')

    if val1 == 'All':
        items = BondModel.objects.filter(name_of_political_party=val2).values_list('bond_id')
    else:
        items = BondModel.objects.filter(name_of_political_party=val2, name_of_purchaser=val1).values_list('bond_id')
    
    options = [item for item in items]
    return JsonResponse(options, safe=False)


def getting_data(request,party_name):
    data = BondModel.objects.filter(name_of_political_party=party_name).values_list('name_of_purchaser',flat=True).distinct()
    items = [dta for dta in data]
    total = 0 
    values=[]
    for company_name in data:
        for dt in BondModel.objects.filter(name_of_political_party=party_name,name_of_purchaser=company_name):
            total = total + dt.denomination
        values.append(total) 
    return [items,values]


def view_articles(request):
    template = loader.get_template('bond/articles.html')
    latest_items_first = Comment.objects.all().order_by('-date_time')
    articles = ACModel.objects.all().order_by('-date_time')
    return HttpResponse(template.render({'articles':articles,'items': latest_items_first},request))

def article_data(request,a_id):
    data = ACModel.objects.get(articleid=a_id)
    latest_items_first = Comment.objects.all().order_by('-date_time')
    articles = ACModel.objects.all()[:5]
    # data_items = get_items(request)
    return render(request,'bond/data.html',{'Data':data,'articles':articles,'items': latest_items_first})
    
def view_try(request):
    template = loader.get_template('bond/try.html')
    articles = ACModel.objects.all().delete()
    return HttpResponse(template.render({'articles': articles},request))

# def get_items(request):
#     if request.user.is_authenticated:
#         username = request.user.username
#         related_article = ACModel.objects.filter(user=username)
#         print(related_article)



        

   






























#upload data from excel file
def upload_excel(request):

    se = True

    file_path = "static\merged.xlsx"
    df = pd.read_excel(file_path) 

    print(type(df))

    if se == True:
        for index,row in df.iterrows():
            my_model = BondModel(
                bond_id = row['BondId'],
                date_of_purchase = row['Date Of Purchase'],
                name_of_purchaser = row['Name of the Purchaser'],
                date_of_expiry = row['Date of Expiry'],
                name_of_political_party = row['Name of Political Party'],
                date_of_encashment = row['Date of Encashment'],
                denomination = row['Denomination'],
                status = row['Status']
            )
            my_model.save()

        return HttpResponse("Success")
    return HttpResponse("upload ")    
    



