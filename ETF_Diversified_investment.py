#ETF 분산투자


import FinanceDataReader as fdr
from pandas import Series,DataFrame
import matplotlib.pyplot as plt
import datetime
import numpy
import math


# 한국주식의 가격 자료 저장
df_KStock = fdr.DataReader('069500','2013-05-10') # KODEX 200의 데이터프레임 읽어오기
price_df_KODEX200 = df_KStock['Close'] /22269   # KODEX200의 가격의 데이터프레임

# 한국채권(3년물)의 가격 자료 저장
df_KBSTAR3Y =fdr.DataReader('114100','2013-05-10')
price_KBSTAR3Y= df_KBSTAR3Y['Close']/93826

# 미국주식(SPY)의 가격 자료 저장
df_SnP500_SPY = fdr.DataReader('SPY', '2013-05-10')
price_df_SPY = df_SnP500_SPY['Close']/163.41

#미국채권(10년물)의 가격 자료 저장
df_TLT = fdr.DataReader('TLT','2013-05-10')
price_df_TLT = df_TLT['Close']/118.75



"""
#4개 자산의 시계열 데이터 출력

print("한국주식\n")
print(price_df_KODEX200)

print("한국채권\n")
print(price_KBSTAR3Y)

print("미국주식\n")
print(price_df_SPY)

print("미국채권\n")
print(price_df_TLT)
"""


#포트폴리오의 비율 입력받기

print("한국, 미국의 주식과 채권 ETF로 이루어진 포트폴리오의 각종 지표를 보여주는 프로그램입니다.\n")

while True:
    print("각 자산의 비율을 백분율로 선택해주세요.(100이하)  맨 마지막인 미국 채권의 비율은 나머지 3개 자산군의 비율에 의해 자동으로 결정됩니다.")
    a=int(input('한국 주식의 비율을 입력하세요:'))
    b=int(input('한국 채권의 비율을 입력하세요:'))
    c=int(input('미국 주식의 비율을 입력하세요:'))
    d=100-a-b-c

    #비율이 100이 넘지 않을 경우 루프문 탈출
    if a+b+c<=100:
        break
    #비율이 100이 넘을 경우 다시 반복
    else:
        print("\n비율이 100이 넘습니다. 100 이하가 되도록 다시 입력해주세요")

print('\n한국 주식의 비율은' ,a)
print('한국 채권의 비율은' ,b)
print('미국 주식의 비율은' ,c)
print('한국 채권의 비율은' ,d,'입니다.\n')


#포트폴리오의 기간을 입력받기

#선택할 수 있는 날짜 (2013-5-10~ 오늘)
first_date =  start_date=datetime.datetime.strptime("2013-05-10", "%Y-%m-%d")
today_date = datetime.datetime.today()

print('포트폴리오의 기간을 입력받습니다. 2013-05-10 ~',today_date.strftime('%Y-%m-%d') ,'사이의 기간만 가능합니다.\n')
i=1
while i==1:
    try:
        #포트폴리오 시작날짜 입력
        start_year=int(input('시작년도를 입력하세요'))
        start_month=int(input('시작 개월을 입력하세요'))
        start_day=int(input('시작 일을 입력하세요'))
        #포트폴리오 종료날짜 입력
        end_year=int(input('\n종료년도를 입력하세요'))
        end_month=int(input('종료 개월을 입력하세요'))
        end_day=int(input('종료 일을 입력하세요'))
        #입력받은 정수를 문자열로 변환
        start_date=str(start_year)+'-'+str(start_month)+'-'+str(start_day)
        end_date = str(end_year) + '-' + str(end_month) + '-' + str(end_day)
        # 문자열을 datetime으로 변환
        start_date=datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")


        if start_date<first_date:
            print("입력된 시작날짜가 2013-05-10 보다 빠릅니다. 다시 입력해 주십시오.\n")

        elif end_date>today_date:
            print("입력된 종료날짜가 "+today_date.strftime('%Y-%m-%d')+ "보다 이후입니다. 다시 입력해주십시오.\n")
        else:
            print("시작날짜는"+start_date.strftime('%Y-%m-%d')+", 종료날짜는"+end_date.strftime('%Y-%m-%d')+"입니다.\n")
            i=0

    #예외처리, 날짜가 잘못 입력됬을 경우 루프문 다시 반복
    except ValueError as e:
        print('잘못된 날짜를 입력했습니다. 다시 입력해주세요.\n')

#포트폴리오 구하기

#최종 포트폴리오
portpolio=(a*price_df_KODEX200.loc[start_date:end_date]+b*price_KBSTAR3Y.loc[start_date:end_date]\
          +c*price_df_SPY.loc[start_date:end_date]+d*price_df_TLT.loc[start_date:end_date])

#포트폴리오의 구매가격
portpolio_start_price=portpolio[0]

#포트폴리오의 행의 개수(투자일수) 구하기
portpolio_length=len(portpolio)-1

#포트폴리오의 최종판매가격 구하기
portpolio_end_price=portpolio[portpolio_length]

#만약 입력된 날짜가 휴일인 경우 nan이 뜸. 개장한 날짜가 나올 때 까지 날짜가 1씩 감소하는 루프문
while math.isnan(portpolio_end_price):
    portpolio_length=portpolio_length-1
    portpolio_end_price = portpolio[portpolio_length]

#총수익률 계산
gross_rate_of_return=(portpolio_end_price-portpolio_start_price)/portpolio_start_price*100
#표준편차
std=numpy.std(portpolio)

print("포트폴리오의 총 수익률은 %.1f 입니다." %gross_rate_of_return)
print("포트폴리오의 표준편차는 %.2f 입니다." %std)

# 그래프로 시각화
plt.plot(portpolio/portpolio_start_price)
plt.show()

