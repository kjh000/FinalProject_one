from django.shortcuts import render
import pandas as pd
import numpy as np
import csv
import sys
import os
# Create your views here.
items=['간장', '계란', '고추장', '과자', '기저귀', '껌', '냉동만두', '된장', '두루마리화장지', '두부', '라면', '마요네즈', '맛김', '맛살', '맥주', '밀가루', '분유', '사이다', '생리대', '생수', '샴푸', '설탕', '세탁세제', '소주', '시리얼', '식용유', '쌈장', '아이스크림', '어묵', '오렌지주스', '우유', '즉석밥', '참기름', '참치 캔', '커피', '케첩', '콜라', '햄']

def mainFunc(request):
    item=items
    return render(request,'main.html', {'item':item})

def findFunc(request):
    if request.method =='GET':
        print('GET 요청 처리')
        
        irum = request.GET.get("searchInput")
        print(irum)
        dfl = df[df['분류'].str.contains(irum) & df['지역'].str.contains("종로구")].values.tolist()
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
        