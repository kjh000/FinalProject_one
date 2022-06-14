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

# Create your views here.
items=['간장', '계란', '고추장', '과자', '기저귀', '껌', '냉동만두', '된장', '두루마리화장지', '두부', '라면', '마요네즈', '맛김', '맛살', '맥주', '밀가루', '분유', '사이다', '생리대', '생수', '샴푸', '설탕', '세탁세제', '소주', '시리얼', '식용유', '쌈장', '아이스크림', '어묵', '오렌지주스', '우유', '즉석밥', '참기름', '참치 캔', '커피', '케첩', '콜라', '햄']
names = ['지역','마켓종류','마트이름','분류','품목','가격']
# loc=['강남구','강동구','강서구']
# 간장 같은거 영문으로 => 연관상품 매칭
items_e = ['ganjang','yakult','gochu','snack','hip','gum','mando','doenjang','hyuji','dobu','ramen','mayonnaise','kim','crab','hite','garu','powder','cider','napkin','water','shampoo','sugar','pongpong','soju','seereal','oil','ssamjang','ice','fish','juice','milk','rice','chamoil','chamchi','coffee','ketchup','colla','ham']
idx = ['ramen','water','colla','rice','snack','gum','ice','garu','seereal','dobu','mando','sugar','gochu','doenjang','ssamjang','oil','ganjang','ketchup','mayonnaise','chamoil','kim','fish','crab','chamchi','ham','powder','juice','cider','coffee','milk','yakult','hite','soju','hip','hyuji','napkin','shampoo','pongpong']
dir = os.path.dirname(os.path.realpath(__file__))

ldata = dir + '\static\csvs\local_mart.csv'
rdata = dir + '\static\csvs\like.csv'

local = pd.read_csv(ldata, header = None, names = names) # 지역마트 정보
reco = pd.read_csv(rdata, header = None) # 연관상품 관련


df = pd.DataFrame(local)
df_r = pd.DataFrame(reco)
df_r.index = idx
df_r.columns = idx

def mainFunc(request):
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
        
        if products:
            productss = parsing2(products)
        if g_products:
            g_productss = parsing2(g_products)
        if f_products:
            f_productss = parsing2(f_products)
        
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
        
        
        
        return render(request,'finder.html',{'dfl':dfl, 'irum':irum,'reco':n_reco,'products':productss,'g_products':g_productss,'f_products':f_productss,'tot':tot,'g_tot':g_tot,'tot':f_tot,'loc':loc})
      
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
    

    
    g_df = craw_gmarket(name)
    if g_df.empty:
        g_product = {"name" : 'None',"price":'0'}
    else:
        g_product = {"name" : g_df[0],"price":g_df[1]}
    
    f_df = craw_fast(name)
    if f_df.empty:
        f_product = {"name" : 'None',"price":'0'}
    else:
        f_product = {"name" : f_df[0],"price":f_df[1]}
    
    if "prod" in request.session: #session이 생성되어있지 않으면, 즉 첫 번째 상품이 아니라면 productList에 상품 정보 저장하기
        productList = request.session["prod"]
        gmarketList = request.session["g_prod"]
        fastList = request.session["f_prod"]
        productList.append(product)
        gmarketList.append(g_product)
        fastList.append(f_product)
        request.session["prod"] = productList
        request.session["g_prod"] = gmarketList
        request.session["f_prod"] = fastList
        
        
        print("세션 유효 시간 : ", request.session.get_expiry_age())
    else: #session에 shop이 없으면 productList에 상품을 넣고 request.session에 "shop" 이라는 키를 만든다
        productList.append(product)
        request.session["prod"] = productList
        gmarketList.append(g_product)
        request.session["g_prod"] = gmarketList
        fastList.append(f_product)
        request.session["f_prod"] = fastList
    
    
    
    tot,g_tot,f_tot = 0,0,0
    for p in request.session['prod']:
        tot += p["price"]
    
    for g in request.session['g_prod']:
        g['price']=g['price'].replace(',',"")
        g_tot += int(g["price"])
    for f in request.session['f_prod']:
        f['price']=f['price'].replace(',',"")
        f_tot += int(f["price"])
        
    request.session["tot"] = tot
    request.session["g_tot"] = g_tot
    request.session["f_tot"] = f_tot
    
 
    context = {} #html에 보낼 용도
    context['products'] = request.session['prod']
    context['g_products'] = request.session['g_prod']
    context['f_products'] = request.session['f_prod']
    context['tot'] = request.session['tot']
    context['g_tot'] = request.session['g_tot']
    context['f_tot'] = request.session['f_tot']
    # dfl':dfl, 'irum':irum,'reco':n_reco
    context['dfl'] = dfl
    context['irum'] = irum
    context['reco'] = n_reco
    context['loc'] = loc
    request.session.set_expiry(30) #세션 시간 결정

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

    products = request.POST.get("products")
    g_products = request.POST.get("g_products")
    f_products = request.POST.get("f_products")
    
    tot = request.POST.get("tot")
    g_tot = request.POST.get("g_tot")
    f_tot = request.POST.get("f_tot")
    
    g_tot3 = int(g_tot) + 3000
    f_tot3 = int(f_tot) + 3000
    
    productss = parsing2(products)
    g_productss = parsing(g_products)    f_productss = parsing(f_products)

              
    return render(request,'receipt.html',{'products' : productss,'g_products' : g_productss,'f_products' : f_productss,'tot':tot,'g_tot':g_tot,'f_tot':f_tot,'g_tot3':g_tot3,'f_tot3':f_tot3})

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
    
    
    