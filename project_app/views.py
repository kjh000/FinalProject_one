from django.shortcuts import render
import pandas as pd
import numpy as np
import csv
import sys
import os
# Create your views here.

def mainFunc(request):
    return render(request,'main.html')

def findFunc(request):
    if request.method =='GET':
        print('GET 요청 처리')
        
        irum = request.GET.get("itemSelect")
        print(irum)
        dfl = df[df['품목'].str.contains(irum) & df['지역'].str.contains("종로구 내수동")& df['마트이름'].str.contains("지씨마트")].values.tolist()
        dfl.sort(key=lambda x : x[5])
        return render(request,'finder.html',{'dfl':dfl, 'irum':irum})
    else:
        print('error')


names = ['지역','마켓종류','마트이름','분류','품목','가격']

dir = os.path.dirname(os.path.realpath(__file__))

ldata = dir + '\static\csvs\local_mart.csv'
gdata = dir + '\static\csvs\gmarket.csv'

local = pd.read_csv(ldata, header = None,names = names)
gmarket = pd.read_csv(gdata, header = None,names=['품목','가격'])

df = pd.DataFrame(local)
df_g = pd.DataFrame(gmarket)

# prod = input('검색할 품목 : ')
prod = '라면'
dfl = df[df['품목'].str.contains(prod) & df['지역'].str.contains("종로구 내수동")& df['마트이름'].str.contains("지씨마트")].values.tolist()
dfl_g = df_g[df_g['품목'].str.contains(prod)].values.tolist()

dfl.sort(key=lambda x : x[5])
dfl_g.sort(key=lambda x : x[1])

# print(dfl)
# print(dfl_g)

def testFunc(request):
    msg = dfl
    return render(request,'test.html',{'myMsg':msg}) # forward 방식

def insertFunc(request):
    if request.method =='GET':
        print('GET 요청 처리')
        return render(request,'insert.html') #forward 방식 <jsp:
        # return HttpResponseRedirect('insert.html') # redirect 방식
    elif request.method =='POST':
        print('POST 요청 처리')
        
        irum = request.POST.get('name')
        dfl = df[df['품목'].str.contains(irum) & df['지역'].str.contains("종로구 내수동")& df['마트이름'].str.contains("지씨마트")].values.tolist()
        dfl.sort(key=lambda x : x[5])
        print(dfl)
        # return render(request,'finder.html',{'df0':dfl[0][0],'df1':dfl[0][1],'df2':dfl[0][2],'df3':dfl[0][3],'df4':dfl[0][4],'df5':dfl[0][5]})
        return render(request,'finder.html',{'dfl':dfl})
        
    else:
        print('error')
        