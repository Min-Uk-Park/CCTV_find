#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import requests
# from bs4 import BeautifulSoup as bs
# import pandas as pd

# dv = input('지역을 입력하세요. : ')

# api_key = "EcvPTV8/txYONcgKQK2S9KkJowH9knkAfgDbyRATHPcyihJWdzZzHU70CmqdGNOfrQF2Cni4fmIXBtes8y27bA=="
# url = 'http://openapi.jeonju.go.kr/rest/cctv/getCctvList'


# params ={'serviceKey' : api_key, 'pageSize' : '2000', 'authApiKey' : '', 'dataValue' : dv, 'startPage' : '1' }

# response = requests.get(url, params=params).text
# data = bs(response,'xml')

# # print(data.prettify())

# temp = [['기준일자','대수','화소','도로명주소','목적','경도','위도','번지주소','설치년월','보관일수']] # CCTV위치별 정보 리스트
# data.select('body>data>list')

# for i in data.select('body>data>list'):
#     a = []
#     a.append(i.select_one('baseDate').text) # 이렇게 해도 된다!
#     a.append(i.cameraCnt.string)
#     a.append(i.cameraPixel.string)
#     a.append(i.cctvAddr.string)
#     a.append(i.cctvNm.string)
#     a.append(i.cctvPosx.string)
#     a.append(i.cctvPosy.string)
#     a.append(i.dongAddr.string)
#     a.append(i.insYM.string)
#     a.append(i.storageDay.string)
    
#     # print(a)
#     temp.append(a)

# df = pd.DataFrame(temp)
# df.rename(columns=df.iloc[0,:],inplace=True)
# df.drop(df.index[0],inplace=True)
# # df


# In[2]:


# # 위의 코드를 아래로 단순화 시킨다!
# import requests
# from bs4 import BeautifulSoup as bs
# import pandas as pd

# dv = input('지역을 입력하세요. : ')

# api_key = "EcvPTV8/txYONcgKQK2S9KkJowH9knkAfgDbyRATHPcyihJWdzZzHU70CmqdGNOfrQF2Cni4fmIXBtes8y27bA=="
# url = 'http://openapi.jeonju.go.kr/rest/cctv/getCctvList'

# params ={'serviceKey' : api_key, 'pageSize' : '2000', 'authApiKey' : '', 'dataValue' : dv, 'startPage' : '1' }

# response = requests.get(url, params=params).text
# data = bs(response,'xml')

# # print(data.prettify())

# temp = [['기준일자','대수','화소','도로명주소','목적','경도','위도','번지주소','설치년월','보관일수']] # CCTV위치별 정보 리스트
# tags=['baseDate','cameraCnt','cameraPixel','cctvAddr','cctvNm','cctvPosx',
#      'cctvPosy','dongAddr','insYM','storageDay']


# for i in data.select('body>data>list'):
#     a = []
#     for tag in tags:
#         a.append(i.select_one(f'{tag}').text) # 코드 단순화시킨다.
#         # a.append(i.tag.string)

#     temp.append(a)
    
# df = pd.DataFrame(temp)
# df.rename(columns=df.iloc[0,:],inplace=True)
# df.drop(df.index[0],inplace=True)
# # df


# In[3]:
import sys
sys.path.append('c:/Users/LG/anaconda3/Lib/site-packages')
# 위 코드 더 단순화 시킨 코드(DF을 한 번에 만든다!)
from folium.plugins import MarkerCluster
from haversine import haversine # 위도, 경도 이용하여 구 상에서 두 점 사이의 직선거리 구하기(default 단위는 km)
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import folium
# ①전주 송천동 cctv위치 찾아 표시하고 경찰청도시교통정보센터(https://www.utic.go.kr)에서 cctv url을 가져와 하이퍼링크로 연결해보기
# ②그리고 그 반경에 원을 표시하고  ③marker_cluster를 통해서 나타내기!

dvs = input('지역을 입력하세요. : ').split()

api_key = "EcvPTV8/txYONcgKQK2S9KkJowH9knkAfgDbyRATHPcyihJWdzZzHU70CmqdGNOfrQF2Cni4fmIXBtes8y27bA=="
url = 'http://openapi.jeonju.go.kr/rest/cctv/getCctvList'


# In[4]:


# 최대반경 구하는 함수
def rad(k1,total):
    max = 0
    # if total['위도'] != 0.000000 & total['경도'] != 0.000000:
    for lat,len in zip(total['위도'],total['경도']):
        if (lat != 0.000000) & (len != 0.000000):
            k2 = (lat,len)
            distance = haversine(k1,k2,unit='m')
            if distance>max:max = distance
    # print(max)
    return max

# 지도 그리는 함수
def mapdraw(mc,max_rad,cctv_total):
    # m = folium.Map([a,b],
    #            zoom_start=17, 
    #            width=1200, 
    #            height=500
    #           )
    
 
    # marker_cluster = MarkerCluster().add_to(m)
    lotte_url = 'http://www.utic.go.kr/view/map/cctvStream.jsp?cctvid=L33009&cctvname=%25EC%2586%25A1%25EC%25B2%259C%25EC%2582%25BC%25EA%25B1%25B0%25EB%25A6%25AC&kind=F&cctvip=115.92.162.198&cctvch=null&id=09&cctvpasswd=null&cctvport=null&minX=127.07123553865512&minY=35.80648295905291&maxX=127.1689049616251&maxY=35.87768082988352'
    for addr,why,lat,len in zip(cctv_total['도로명주소'],cctv_total['목적'],cctv_total['위도'],cctv_total['경도']):
        try:
            if (lat==35.8541955) & (len==127.119541):# 송천 롯데마트 삼거리 cctv 하이퍼링크 첨부
                folium.Marker([lat,len],
                        popup = why + f'<br><a href = {lotte_url}>cctv링크연결</a></br>' ,
                        tooltip= addr,
                        icon=folium.Icon(icon='camera',color='green')).add_to(mc)
            else:
                folium.Marker([lat,len],
                            popup = why + f'{lat},{len}',
                            tooltip= addr,
                            icon=folium.Icon(icon='camera',color='green')).add_to(mc)
        except:
            pass
    

# 중심 기준 원 그리는 함수
def circle_draw(a,b,max_rad,m,dv):
    folium.Marker([a,b],tooltip=dv,icon=folium.Icon(color='blue',icon='star')).add_to(m)
    folium.Circle([a,b],radius=max_rad,fill_color = 'green').add_to(m)
    print(max_rad)
    return m


# In[5]:


# 각 동 위도, 경도 평균 구하기
def avg_find(base):
    s = 0
    c=0
    temp = []

    for i in base:
        try:
            s+=float(i)
            temp.append(float(i))
            c+=1
            
        except:
            temp.append(0)
    # print(s,c,s/c)
    return s/c,temp


# In[6]:


# 전주 시청 중심으로 한 개의 지도 생성
latitude = 35.8242238      # 전주시청 위도
longitude = 127.1479532   # 전주시청 경도
m = folium.Map(location=[latitude, longitude],
               zoom_start=17, 
               width=1200, 
               height=500
              )

mc = MarkerCluster().add_to(m) # cctv개수 zoom 풀었을 때 개수 나타내기 위해서 적용해준다.

# 동 별 cctv나타내고 그 중심으로 원 그리기
for dv in dvs:
    cctv_total=pd.DataFrame()
    params ={'serviceKey' : api_key, 'pageSize' : '2000', 'authApiKey' : '', 'dataValue' : dv, 'startPage' : '1' }

    response = requests.get(url, params=params).text
    data = bs(response,'xml')

    # 코드 단순화!
    col=['기준일자','대수','화소','도로명주소','목적','경도','위도','번지주소','설치년월','보관일수']
    tag=['baseDate','cameraCnt','cameraPixel','cctvAddr','cctvNm','cctvPosx',
        'cctvPosy','dongAddr','insYM','storageDay']
    
    for c,t in zip(col,tag):
        cctv_total[c]=[i.text for i in data.select(t)]

    cctv_total = cctv_total[['도로명주소','목적','위도','경도']] 
    # cctv_total['위도'].dtypes
    
    avg1,lat_temp = avg_find(cctv_total['위도'])
    avg2,len_temp = avg_find(cctv_total['경도'])

    cctv_total['위도'] = lat_temp
    cctv_total['경도'] = len_temp
    
    k1 = (avg1,avg2)
    
    # 최대반경 구하기
    max_dis = rad(k1,cctv_total)
    
    # 지도에 cctv기호를 표시하여 나타내는 함수 mc를 인수로 설정한 이유는 mc 안에 m을 적용했기 때문이다. (지도에 적용함과 동시에 개수를 표시해주는 기능가짐)
    mapdraw(mc,max_dis,cctv_total)
    final_m = circle_draw(avg1,avg2,max_dis,m,dv)
    
final_m


# In[7]:


# 전주시청을 중심으로 지도 그리기
latitude = 35.8242238      # 전주시청 위도
longitude = 127.1479532   # 전주시청 경도
m = folium.Map(location=[latitude, longitude],
               zoom_start=17, 
               width=1200, 
               height=500
              )
# m


# In[8]:


# m이라는 지도를 나타내는 객체를 인수로 하여 add_to()하기

folium.Marker(location=[latitude, longitude],
              popup='전주시청',
              tooltip='아름다운 도시 <br>전주</br>').add_to(m)# tooltip은 마우스 대면 보이는 문구/ popup은 클릭 시 보이는 문구
# m


# In[9]:


from haversine import haversine
# pip install --user [package_name] => 있지도 않은 파일로 경로가 설정되어 있음 아마 가상환경 만들어서?? 맞다!
# pip install [package_name] => 기본 경로를 anaconda3/~~/site~ 로 환경변수 Path 바꿔주었는데 괜찮은지....? 원래 기본값이 이 경로였는데 갑자기 다른 경로로 바뀌어서 
# 수동으로 강제적으로 바꿔줌.... ?? 괜찮지만 에러가 반복되면 아나콘다를 재설치하는 것이 낮다!

