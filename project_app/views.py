from django.shortcuts import render
import pandas as pd
import numpy as np
import csv
import sys
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request as req
from urllib import parse
from project_app.models import Basket, Gbasket, Fbasket
from django.db.models import Sum

# Create your views here.
items=['간장', '계란', '고추장', '과자', '기저귀', '껌', '냉동만두', '된장', '두루마리화장지', '두부', '라면', '마요네즈', '맛김', '맛살', '맥주', '밀가루', '분유', '사이다', '생리대', '생수', '샴푸', '설탕', '세탁세제', '소주', '시리얼', '식용유', '쌈장', '아이스크림', '어묵', '오렌지주스', '우유', '즉석밥', '참기름', '참치 캔', '커피', '케첩', '콜라', '햄']
names = ['지역','마켓종류','마트이름','분류','품목','가격']
# loc=['강남구','강동구','강서구']
# 간장 같은거 영문으로 => 연관상품 매칭
items_e = ['ganjang','yakult','gochu','snack','hip','gum','mando','doenjang','hyuji','dobu','ramen','mayonnaise','kim','crab','hite','garu','powder','cider','napkin','water','shampoo','sugar','pongpong','soju','seereal','oil','ssamjang','ice','fish','juice','milk','rice','chamoil','chamchi','coffee','ketchup','colla','ham']
idx = ['ramen','water','colla','rice','snack','gum','ice','garu','seereal','dobu','mando','sugar','gochu','doenjang','ssamjang','oil','ganjang','ketchup','mayonnaise','chamoil','kim','fish','crab','chamchi','ham','powder','juice','cider','coffee','milk','yakult','hite','soju','hip','hyuji','napkin','shampoo','pongpong']
dir = os.path.dirname(os.path.realpath(__file__))

# ldata = dir + '\static\csvs\local_mart.csv'
# rdata = dir + '\static\csvs\like.csv'

# 위에 거가 맞는거
ldata = dir + '/static/csvs/local_mart.csv'
rdata = dir + '/static/csvs/like.csv'

local = pd.read_csv(ldata, header = None, names = names) # 지역마트 정보
reco = pd.read_csv(rdata, header = None) # 연관상품 관련


df = pd.DataFrame(local)
df_r = pd.DataFrame(reco)
df_r.index = idx
df_r.columns = idx

def mainFunc(request):
    if "prod" in request.session:
        prodList = request.session['prod']
        print(prodList)
        del request.session['prod']
    
        
    
    item=items
    return render(request,'main.html', {'item':item})

def findFunc(request):
    if request.method == 'POST':
       

        productss = []
        g_productss = []
        f_productss = []
       
        products = request.POST.get("products")
        g_products = request.POST.get("g_products")
        f_products = request.POST.get("f_products")
        tot = request.POST.get("tot")
        g_tot = request.POST.get("g_tot")
        f_tot = request.POST.get("f_tot")
        
        datas = Basket.objects.all()
        
        if products:
            productss = parsing2(products)
        if g_products:
            g_productss = parsing(g_products)
        if f_products:
            f_productss = parsing(f_products)
        
        print("productss : ",productss)

        irum = request.POST.get("searchInput")   
        loc=request.POST.get("searchLoc")
        
        dfl = df[df['분류'].str.contains(irum) & df['지역'].str.contains(loc)].values.tolist()
        dfl.sort(key=lambda x : x[5])
        
        if len(dfl) > 20:
            dfl = dfl[:20]
        
        reco = []
        n_reco = []
        if irum:
            id = items.index(irum)
            en_irum = items_e[id]
            
            df_reco = df_r.loc[en_irum]
            dfv = df_reco.values
        
            for i in range(len(dfv)):
                # 이거 like.csv 수정해야됨
                ii = items_e.index(idx[i])
                cnt = [dfv[i],items[ii]]
                
                reco.append(cnt)
         
        
            reco.sort(reverse=True)
        
        for i in reco[1:7]:
            n_reco.append(i[1])
        
        
        
        return render(request,'finder.html',{'datas':datas,'dfl':dfl, 'irum':irum,'reco':n_reco,'products':productss,'g_products':g_productss,'f_products':f_productss,'tot':tot,'g_tot':g_tot,'tot':f_tot,'loc':loc})
      
    else:
        print('error')

def searchFunc(request):
    
    if request.method == 'POST':

        irum = request.POST.get("searchInput")
        loc=request.POST.get("searchLoc")
        

        dfl = df[df['분류'].str.contains(irum) & df['지역'].str.contains(loc)].values.tolist()
        dfl.sort(key=lambda x : x[5])
        
        reco = []
        n_reco = []
        id = items.index(irum)
        en_irum = items_e[id]
        
        df_reco = df_r.loc[en_irum]
        dfv = df_reco.values
        
        for i in range(len(dfv)):

            ii = items_e.index(idx[i])
            cnt = [dfv[i],items[ii]]

            reco.append(cnt)

        reco.sort(reverse=True)
        
        for i in reco[1:7]:
            n_reco.append(i[1])
        
        print(n_reco)
        
        return render(request,'finder.html',{'dfl':dfl, 'irum':irum,'reco':n_reco})
    else:
        print('error')


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
        return render(request,'finder.html',{'dfl':dfl})
        
    else:
        print('error')

def basketFunc(request):

    name = request.POST.get("name")
    price = request.POST.get("price")
    price = int(price)
    
    
    g_df = craw_gmarket(name)
    f_df = craw_fast(name)
    if g_df.empty:
        g_product = {"name" : 'None',"price":0}
        f_product = {"name" : 'None',"price":0}
        
    else:
        g_df[1] = g_df[1].replace(',',"")
        f_df[1] = f_df[1].replace(',',"")
        
        g_df[1] = int(g_df[1])
        f_df[1] = int(f_df[1])
        
        
        g_product = {"name" : g_df[0],"price":g_df[1]}
        f_product = {"name" : f_df[0],"price":f_df[1]}

    Gbasket(
        pname = g_df[0],
        price = g_df[1]
            ).save()
    
    Fbasket(
        pname = f_df[0],
        price = f_df[1]
    
        ).save()
    datas = Basket.objects.all()
    Basket(
        pname =name,
        price = price
        ).save()
    

    product = {"name" : name, "price" : price}
    productList = []
    gmarketList = [] # 지마켓 최저가 장바구니
    fastList = [] # 당일 배송 장바구니
    
    irum = request.POST.get("searchInput")   
    loc=request.POST.get("searchLoc")
   
    
    dfl = df[df['분류'].str.contains(irum) & df['지역'].str.contains(loc)].values.tolist()
    dfl.sort(key=lambda x : x[5])
    
    if len(dfl) > 20:
        dfl = dfl[:20]
    
    reco = []
    n_reco = []
    if irum:
        id = items.index(irum)
        en_irum = items_e[id]
        
        df_reco = df_r.loc[en_irum]
        dfv = df_reco.values
    
        for i in range(len(dfv)):
            # 이거 like.csv 수정해야됨
            ii = items_e.index(idx[i])
            cnt = [dfv[i],items[ii]]
            
            reco.append(cnt)
     
    
        reco.sort(reverse=True)
    
    for i in reco[1:7]:
        n_reco.append(i[1])


 
    context = {} #html에 보낼 용도

    context['dfl'] = dfl
    context['irum'] = irum
    context['reco'] = n_reco
    context['loc'] = loc
    context['datas'] = datas

    return render(request, 'finder.html', context)


def reFinderFunc(request):
    
    return render(request, 'Finder.html')

def resetFunc(request):
    del request.session["prod"]
    return render(request, 'basket.html')
    
def craw_gmarket(item):
    
    item = parse.quote(item)
    url = "https://browse.gmarket.co.kr/search?keyword="
    url = url+item
  
    html = urlopen(url)
    
    soup = BeautifulSoup(html,'html.parser')
    
    gm_names = []
    gm_prices = []
    gmarket = []
    
    names = soup.select('span.text__item')
    prices = soup.select('strong.text.text__value')
    
    for name in names:
        gm_names.append(name.text.strip())
    
    for price in prices:
        gm_prices.append(price.text.strip())
    
    g_df = pd.DataFrame({'제품명':gm_names,'가격':gm_prices})
    
    g_df = g_df.sort_values('가격')
    if g_df.empty:
        return g_df
    else:
        return g_df.iloc[0]


def craw_fast(item):
    
    item = parse.quote(item)
    url = "https://browse.gmarket.co.kr/search?keyword="
    url = url+item+"&t=e&tf=e:128935607"

    html = urlopen(url)
    
    soup = BeautifulSoup(html,'html.parser')
    
    gm_names = []
    gm_prices = []
    gmarket = []
    
    names = soup.select('span.text__item')
    prices = soup.select('strong.text.text__value')
    
    for name in names:
        gm_names.append(name.text.strip())
    
    for price in prices:
        gm_prices.append(price.text.strip())
    
    g_df = pd.DataFrame({'제품명':gm_names,'가격':gm_prices})
    
    g_df = g_df.sort_values('가격')
    
    if g_df.empty:
        return g_df
    else:
        return g_df.iloc[0]


def receipt(request):


    datas = Basket.objects.all()
    gdatas = Gbasket.objects.all()
    fdatas = Fbasket.objects.all()
    
    sum = Basket.objects.aggregate(Sum('price'))
    gsum = Gbasket.objects.aggregate(Sum('price'))
    fsum = Fbasket.objects.aggregate(Sum('price'))
    
    context ={}
    context['products'] = datas
    context['g_products'] = gdatas
    context['f_products'] = fdatas
    context['tot'] = sum['price__sum']
    context['g_tot'] = gsum['price__sum']
    context['f_tot'] = fsum['price__sum']
    context['g_tot3'] = gsum['price__sum']+3000
    context['f_tot3'] = fsum['price__sum']+3000
    
    
    
    
    return render(request,'receipt.html',context)

def parsing(input):
    output = []
    c = input[1:-1]
    c = c.replace('{',"")
    c = c.replace('}',"") 
    
    c = c.split(',')
    for i in range(len(c)):
        j = c[i]
        if i%2 == 0:
            cc = {}
            if i == 0:
                cc['name'] = j[9:-1]
            else:
                cc['name'] = j[10:-1]
        else:
            cc['price'] = int(j[11:-1])
            output.append(cc)
    
    return output
# 진짜 
def parsing2(input):
    output = []
    c = input[1:-1]
    c = c.replace('{',"")
    c = c.replace('}',"") 
    
    c = c.split(',')
    for i in range(len(c)):
        j = c[i]
        if i%2 == 0:
            cc = {}
            if i == 0:
                cc['name'] = j[9:-1]
            else:
                cc['name'] = j[10:-1]
        else:
            cc['price'] = int(j[10:])
            output.append(cc)
    
    return output

def clearFunc(request):
    irum = request.POST.get("searchInput")   
    loc=request.POST.get("searchLoc")
   
    Basket.objects.all().delete()
    Gbasket.objects.all().delete()
    Fbasket.objects.all().delete()
    
    
    dfl = df[df['분류'].str.contains(irum) & df['지역'].str.contains(loc)].values.tolist()
    dfl.sort(key=lambda x : x[5])
    
    if len(dfl) > 20:
        dfl = dfl[:20]
    
    reco = []
    n_reco = []
    if irum:
        id = items.index(irum)
        en_irum = items_e[id]
        
        df_reco = df_r.loc[en_irum]
        dfv = df_reco.values
    
        for i in range(len(dfv)):
            # 이거 like.csv 수정해야됨
            ii = items_e.index(idx[i])
            cnt = [dfv[i],items[ii]]
            
            reco.append(cnt)
     
    
        reco.sort(reverse=True)
    
    for i in reco[1:7]:
        n_reco.append(i[1])
    
    context = {}
    context['dfl'] = dfl
    context['irum'] = irum
    context['reco'] = n_reco
    context['loc'] = loc
    return render(request,'finder.html',context)
    