import pandas as pd
print(pd.__version__)
import numpy as np
import time
import threading
#야후 파이낸스 사용
import yfinance as yf
#오늘 날짜 가져오기
import datetime as dt

#함수 정의, 나스닥종합지수, 다우지수, s&p500 데이터를 2012~ 오늘까지 가져옴
def get_index():
    #오늘 날짜
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    nasdaq = yf.Ticker("^IXIC")
    dow = yf.Ticker("^DJI")
    s_p = yf.Ticker("^GSPC")
    nasdaq_df = nasdaq.history(start="2012-01-01", end=today)
    dow_df = dow.history(start="2012-01-01", end=today)
    s_p_df = s_p.history(start="2012-01-01", end=today)
    #데이터프레임에서 종가만 가져오기
    nasdaq_df = nasdaq_df['Close']
    dow_df = dow_df['Close']
    s_p_df = s_p_df['Close']
    #데이터프레임 합치기
    index_df = pd.concat([nasdaq_df, dow_df, s_p_df], axis=1)
    #컬럼명 변경
    index_df.columns = ['Nasdaq', 'DJIA', 'S&P500']
    #날짜 %Y-%m-%d 형식으로 변경
    index_df.index = index_df.index.strftime('%Y-%m-%d')
    
    #csv파일로 저장
    index_df.to_csv('public/index.csv')
    index_df.to_csv('public/index_2012.csv')
    print('index.csv 파일 저장 완료')

    #전일 대비 상승폭 % 구현
    #전일 대비 상승폭 % = (오늘 종가 - 전일 종가) / 전일 종가 * 100
    #전일 대비 상승폭 % 컬럼 추가
    index_df['Nasdaq_chg'] = 0.0
    index_df['DJIA_chg'] = 0.0
    index_df['S&P500_chg'] = 0.0
    #전일 대비 상승폭 % 계산
    for i in range(1, len(index_df)):
        index_df.iloc[i, 3] = (index_df.iloc[i, 0] - index_df.iloc[i-1, 0]) / index_df.iloc[i-1, 0] * 100
        index_df.iloc[i, 4] = (index_df.iloc[i, 1] - index_df.iloc[i-1, 1]) / index_df.iloc[i-1, 1] * 100
        index_df.iloc[i, 5] = (index_df.iloc[i, 2] - index_df.iloc[i-1, 2]) / index_df.iloc[i-1, 2] * 100

    #자르기 최근 10일자
    index_df = index_df[-10:]
    
    #열 선택, 변화율만
    index_df = index_df.iloc[:, 3:]

    #소수점 2자리까지 표현
    index_df = index_df.round(2)

    #열이름 바꾸기
    index_df.columns = ['나스닥 변화율(%)', '다우지수 변화율(%)', 's&p500 변화율(%)']
    
    #csv파일로 저장
    index_df.to_csv('public/index_chg.csv')
    print('index_chg.csv 파일 저장 완료')

#함수정의, 나스닥, 다우, s&p500의 이평선 데이터
def get_ma():
    #index.csv파일 불러오기
    index_df = pd.read_csv('public/index.csv', index_col=0)
    #이평선 데이터 생성
    index_df['nasdaq_ma5'] = index_df['Nasdaq'].rolling(window=5).mean()
    index_df['nasdaq_ma20'] = index_df['Nasdaq'].rolling(window=20).mean()
    index_df['nasdaq_ma60'] = index_df['Nasdaq'].rolling(window=60).mean()
    index_df['nasdaq_ma120'] = index_df['Nasdaq'].rolling(window=120).mean()
    index_df['nasdaq_ma200'] = index_df['Nasdaq'].rolling(window=200).mean()

    index_df['dow_ma5'] = index_df['DJIA'].rolling(window=5).mean()
    index_df['dow_ma20'] = index_df['DJIA'].rolling(window=20).mean()
    index_df['dow_ma60'] = index_df['DJIA'].rolling(window=60).mean()
    index_df['dow_ma120'] = index_df['DJIA'].rolling(window=120).mean()
    index_df['dow_ma200'] = index_df['DJIA'].rolling(window=200).mean()
     
    index_df['s_p_ma5'] = index_df['S&P500'].rolling(window=5).mean()
    index_df['s_p_ma20'] = index_df['S&P500'].rolling(window=20).mean()
    index_df['s_p_ma60'] = index_df['S&P500'].rolling(window=60).mean()
    index_df['s_p_ma120'] = index_df['S&P500'].rolling(window=120).mean()
    index_df['s_p_ma200'] = index_df['S&P500'].rolling(window=200).mean()

    #csv파일로 저장
    index_df.to_csv('public/index_ma.csv')
    print('index_ma.csv 파일 저장 완료')

    #index.csv파일, index_ma.csv파일, index_ma_gap.csv 파일 모두 불러오기
    #불러오기
    index_df = pd.read_csv('public/index.csv', index_col=0)
    index_ma_df = pd.read_csv('public/index_ma.csv', index_col=0)

    #자르기 2018-01-01부터 자르기
    index_df = index_df['2018-01-01':]
    index_ma_df = index_ma_df['2018-01-01':]
    
    # #데이터프레임 datetime으로 바꾸기
    # index_df.index = pd.to_datetime(index_df.index, format='%Y-%m-%d')
    # index_ma_df.index = pd.to_datetime(index_ma_df.index, format='%Y-%m-%d')

    #csv파일로 저장
    index_df.to_csv('public/index.csv')
    index_ma_df.to_csv('public/index_ma.csv')
    print('index.csv, index_ma.csv 파일 기간 자르기 완료')

#지수 빼기 이평선 데이터
def get_index_ma():
    #index.csv불러오기
    index_df = pd.read_csv('public/index.csv', index_col=0)
    #index_ma.csv파일 불러오기
    index_ma_df = pd.read_csv('public/index_ma.csv', index_col=0)
    #지수 빼기 이평선 데이터 생성 
    #예시 코드 df['column3'] = df.apply(lambda x: cos_sim(x['column1'], x['column2']), axis=1)
    index_ma_df['nasdaq_ma5_gap'] = index_ma_df.apply(lambda x: x['Nasdaq'] - x['nasdaq_ma5'], axis=1)
    index_ma_df['nasdaq_ma20_gap'] = index_ma_df.apply(lambda x: x['Nasdaq'] - x['nasdaq_ma20'], axis=1)
    index_ma_df['nasdaq_ma60_gap'] = index_ma_df.apply(lambda x: x['Nasdaq'] - x['nasdaq_ma60'], axis=1)
    index_ma_df['nasdaq_ma120_gap'] = index_ma_df.apply(lambda x: x['Nasdaq'] - x['nasdaq_ma120'], axis=1)
    index_ma_df['nasdaq_ma200_gap'] = index_ma_df.apply(lambda x: x['Nasdaq'] - x['nasdaq_ma200'], axis=1)

    index_ma_df['dow_ma5_gap'] = index_ma_df.apply(lambda x: x['DJIA'] - x['dow_ma5'], axis=1)
    index_ma_df['dow_ma20_gap'] = index_ma_df.apply(lambda x: x['DJIA'] - x['dow_ma20'], axis=1)
    index_ma_df['dow_ma60_gap'] = index_ma_df.apply(lambda x: x['DJIA'] - x['dow_ma60'], axis=1)
    index_ma_df['dow_ma120_gap'] = index_ma_df.apply(lambda x: x['DJIA'] - x['dow_ma120'], axis=1)
    index_ma_df['dow_ma200_gap'] = index_ma_df.apply(lambda x: x['DJIA'] - x['dow_ma200'], axis=1)

    index_ma_df['s_p_ma5_gap'] = index_ma_df.apply(lambda x: x['S&P500'] - x['s_p_ma5'], axis=1)
    index_ma_df['s_p_ma20_gap'] = index_ma_df.apply(lambda x: x['S&P500'] - x['s_p_ma20'], axis=1)
    index_ma_df['s_p_ma60_gap'] = index_ma_df.apply(lambda x: x['S&P500'] - x['s_p_ma60'], axis=1)
    index_ma_df['s_p_ma120_gap'] = index_ma_df.apply(lambda x: x['S&P500'] - x['s_p_ma120'], axis=1)
    index_ma_df['s_p_ma200_gap'] = index_ma_df.apply(lambda x: x['S&P500'] - x['s_p_ma200'], axis=1)

    #csv파일로 저장
    index_ma_df.to_csv('public/index_ma_gap.csv')
    print('index_ma_gap.csv 파일 저장 완료')

   
    index_ma_gap_df = pd.read_csv('public/index_ma_gap.csv', index_col=0)    
    #이격도 마지막 1행만 남기기
    index_ma_gap_df_last = index_ma_gap_df.tail(1)
    
    #퍼센트 만들어서 붙이기
    index_ma_gap_df_last['nasdaq_ma5_gap_percent'] = index_ma_gap_df_last['nasdaq_ma5_gap'] / index_ma_gap_df_last['Nasdaq'] * 100
    #str로 바꾸기
    index_ma_gap_df_last['nasdaq_ma5_gap_percent'] = index_ma_gap_df_last['nasdaq_ma5_gap_percent'].astype(str)
    #퍼센트 붙이기
    index_ma_gap_df_last['nasdaq_ma5_gap_percent'] = index_ma_gap_df_last['nasdaq_ma5_gap_percent'] + '%'
    #소수점 2자리까지만
    index_ma_gap_df_last['nasdaq_ma5_gap_percent'] = index_ma_gap_df_last['nasdaq_ma5_gap_percent'].str[:5]
    #괄호 붙이기
    index_ma_gap_df_last['nasdaq_ma5_gap_percent'] = ' (' + index_ma_gap_df_last['nasdaq_ma5_gap_percent'] + ')'

    #index_ma_gap_df_last['nasdaq_ma5_gap']에 붙이기
    index_ma_gap_df_last['nasdaq_ma5_gap'] = index_ma_gap_df_last['nasdaq_ma5_gap'].astype(str) + index_ma_gap_df_last['nasdaq_ma5_gap_percent']
    
    #반복
    index_ma_gap_df_last['nasdaq_ma20_gap_percent'] = index_ma_gap_df_last['nasdaq_ma20_gap'] / index_ma_gap_df_last['Nasdaq'] * 100
    index_ma_gap_df_last['nasdaq_ma20_gap_percent'] = index_ma_gap_df_last['nasdaq_ma20_gap_percent'].astype(str)
    index_ma_gap_df_last['nasdaq_ma20_gap_percent'] = index_ma_gap_df_last['nasdaq_ma20_gap_percent'] + '%'
    index_ma_gap_df_last['nasdaq_ma20_gap_percent'] = index_ma_gap_df_last['nasdaq_ma20_gap_percent'].str[:5]
    index_ma_gap_df_last['nasdaq_ma20_gap_percent'] = ' (' + index_ma_gap_df_last['nasdaq_ma20_gap_percent'] + ')'
    index_ma_gap_df_last['nasdaq_ma20_gap'] = index_ma_gap_df_last['nasdaq_ma20_gap'].astype(str) + index_ma_gap_df_last['nasdaq_ma20_gap_percent']

    index_ma_gap_df_last['nasdaq_ma60_gap_percent'] = index_ma_gap_df_last['nasdaq_ma60_gap'] / index_ma_gap_df_last['Nasdaq'] * 100
    index_ma_gap_df_last['nasdaq_ma60_gap_percent'] = index_ma_gap_df_last['nasdaq_ma60_gap_percent'].astype(str)
    index_ma_gap_df_last['nasdaq_ma60_gap_percent'] = index_ma_gap_df_last['nasdaq_ma60_gap_percent'] + '%'
    index_ma_gap_df_last['nasdaq_ma60_gap_percent'] = index_ma_gap_df_last['nasdaq_ma60_gap_percent'].str[:5]
    index_ma_gap_df_last['nasdaq_ma60_gap_percent'] = ' (' + index_ma_gap_df_last['nasdaq_ma60_gap_percent'] + ')'
    index_ma_gap_df_last['nasdaq_ma60_gap'] = index_ma_gap_df_last['nasdaq_ma60_gap'].astype(str) + index_ma_gap_df_last['nasdaq_ma60_gap_percent']

    index_ma_gap_df_last['nasdaq_ma120_gap_percent'] = index_ma_gap_df_last['nasdaq_ma120_gap'] / index_ma_gap_df_last['Nasdaq'] * 100
    index_ma_gap_df_last['nasdaq_ma120_gap_percent'] = index_ma_gap_df_last['nasdaq_ma120_gap_percent'].astype(str)
    index_ma_gap_df_last['nasdaq_ma120_gap_percent'] = index_ma_gap_df_last['nasdaq_ma120_gap_percent'] + '%'
    index_ma_gap_df_last['nasdaq_ma120_gap_percent'] = index_ma_gap_df_last['nasdaq_ma120_gap_percent'].str[:5]
    index_ma_gap_df_last['nasdaq_ma120_gap_percent'] = ' (' + index_ma_gap_df_last['nasdaq_ma120_gap_percent'] + ')'
    index_ma_gap_df_last['nasdaq_ma120_gap'] = index_ma_gap_df_last['nasdaq_ma120_gap'].astype(str) + index_ma_gap_df_last['nasdaq_ma120_gap_percent']

    index_ma_gap_df_last['nasdaq_ma200_gap_percent'] = index_ma_gap_df_last['nasdaq_ma200_gap'] / index_ma_gap_df_last['Nasdaq'] * 100
    index_ma_gap_df_last['nasdaq_ma200_gap_percent'] = index_ma_gap_df_last['nasdaq_ma200_gap_percent'].astype(str)
    index_ma_gap_df_last['nasdaq_ma200_gap_percent'] = index_ma_gap_df_last['nasdaq_ma200_gap_percent'] + '%'
    index_ma_gap_df_last['nasdaq_ma200_gap_percent'] = index_ma_gap_df_last['nasdaq_ma200_gap_percent'].str[:5]
    index_ma_gap_df_last['nasdaq_ma200_gap_percent'] = ' (' + index_ma_gap_df_last['nasdaq_ma200_gap_percent'] + ')'
    index_ma_gap_df_last['nasdaq_ma200_gap'] = index_ma_gap_df_last['nasdaq_ma200_gap'].astype(str) + index_ma_gap_df_last['nasdaq_ma200_gap_percent']

    #dow
    index_ma_gap_df_last['dow_ma5_gap_percent'] = index_ma_gap_df_last['dow_ma5_gap'] / index_ma_gap_df_last['DJIA'] * 100
    index_ma_gap_df_last['dow_ma5_gap_percent'] = index_ma_gap_df_last['dow_ma5_gap_percent'].astype(str)
    index_ma_gap_df_last['dow_ma5_gap_percent'] = index_ma_gap_df_last['dow_ma5_gap_percent'] + '%'
    index_ma_gap_df_last['dow_ma5_gap_percent'] = index_ma_gap_df_last['dow_ma5_gap_percent'].str[:5]
    index_ma_gap_df_last['dow_ma5_gap_percent'] = ' (' + index_ma_gap_df_last['dow_ma5_gap_percent'] + ')'
    index_ma_gap_df_last['dow_ma5_gap'] = index_ma_gap_df_last['dow_ma5_gap'].astype(str) + index_ma_gap_df_last['dow_ma5_gap_percent']

    index_ma_gap_df_last['dow_ma20_gap_percent'] = index_ma_gap_df_last['dow_ma20_gap'] / index_ma_gap_df_last['DJIA'] * 100
    index_ma_gap_df_last['dow_ma20_gap_percent'] = index_ma_gap_df_last['dow_ma20_gap_percent'].astype(str)
    index_ma_gap_df_last['dow_ma20_gap_percent'] = index_ma_gap_df_last['dow_ma20_gap_percent'] + '%'
    index_ma_gap_df_last['dow_ma20_gap_percent'] = index_ma_gap_df_last['dow_ma20_gap_percent'].str[:5]
    index_ma_gap_df_last['dow_ma20_gap_percent'] = ' (' + index_ma_gap_df_last['dow_ma20_gap_percent'] + ')'
    index_ma_gap_df_last['dow_ma20_gap'] = index_ma_gap_df_last['dow_ma20_gap'].astype(str) + index_ma_gap_df_last['dow_ma20_gap_percent']

    index_ma_gap_df_last['dow_ma60_gap_percent'] = index_ma_gap_df_last['dow_ma60_gap'] / index_ma_gap_df_last['DJIA'] * 100
    index_ma_gap_df_last['dow_ma60_gap_percent'] = index_ma_gap_df_last['dow_ma60_gap_percent'].astype(str)
    index_ma_gap_df_last['dow_ma60_gap_percent'] = index_ma_gap_df_last['dow_ma60_gap_percent'] + '%'
    index_ma_gap_df_last['dow_ma60_gap_percent'] = index_ma_gap_df_last['dow_ma60_gap_percent'].str[:5]
    index_ma_gap_df_last['dow_ma60_gap_percent'] = ' (' + index_ma_gap_df_last['dow_ma60_gap_percent'] + ')'
    index_ma_gap_df_last['dow_ma60_gap'] = index_ma_gap_df_last['dow_ma60_gap'].astype(str) + index_ma_gap_df_last['dow_ma60_gap_percent']

    index_ma_gap_df_last['dow_ma120_gap_percent'] = index_ma_gap_df_last['dow_ma120_gap'] / index_ma_gap_df_last['DJIA'] * 100
    index_ma_gap_df_last['dow_ma120_gap_percent'] = index_ma_gap_df_last['dow_ma120_gap_percent'].astype(str)
    index_ma_gap_df_last['dow_ma120_gap_percent'] = index_ma_gap_df_last['dow_ma120_gap_percent'] + '%'
    index_ma_gap_df_last['dow_ma120_gap_percent'] = index_ma_gap_df_last['dow_ma120_gap_percent'].str[:5]
    index_ma_gap_df_last['dow_ma120_gap_percent'] = ' (' + index_ma_gap_df_last['dow_ma120_gap_percent'] + ')'
    index_ma_gap_df_last['dow_ma120_gap'] = index_ma_gap_df_last['dow_ma120_gap'].astype(str) + index_ma_gap_df_last['dow_ma120_gap_percent']

    index_ma_gap_df_last['dow_ma200_gap_percent'] = index_ma_gap_df_last['dow_ma200_gap'] / index_ma_gap_df_last['DJIA'] * 100
    index_ma_gap_df_last['dow_ma200_gap_percent'] = index_ma_gap_df_last['dow_ma200_gap_percent'].astype(str)
    index_ma_gap_df_last['dow_ma200_gap_percent'] = index_ma_gap_df_last['dow_ma200_gap_percent'] + '%'
    index_ma_gap_df_last['dow_ma200_gap_percent'] = index_ma_gap_df_last['dow_ma200_gap_percent'].str[:5]
    index_ma_gap_df_last['dow_ma200_gap_percent'] = ' (' + index_ma_gap_df_last['dow_ma200_gap_percent'] + ')'
    index_ma_gap_df_last['dow_ma200_gap'] = index_ma_gap_df_last['dow_ma200_gap'].astype(str) + index_ma_gap_df_last['dow_ma200_gap_percent']

    #s_p
    index_ma_gap_df_last['s_p_ma5_gap_percent'] = index_ma_gap_df_last['s_p_ma5_gap'] / index_ma_gap_df_last['S&P500'] * 100
    index_ma_gap_df_last['s_p_ma5_gap_percent'] = index_ma_gap_df_last['s_p_ma5_gap_percent'].astype(str)
    index_ma_gap_df_last['s_p_ma5_gap_percent'] = index_ma_gap_df_last['s_p_ma5_gap_percent'] + '%'
    index_ma_gap_df_last['s_p_ma5_gap_percent'] = index_ma_gap_df_last['s_p_ma5_gap_percent'].str[:5]
    index_ma_gap_df_last['s_p_ma5_gap_percent'] = ' (' + index_ma_gap_df_last['s_p_ma5_gap_percent'] + ')'
    index_ma_gap_df_last['s_p_ma5_gap'] = index_ma_gap_df_last['s_p_ma5_gap'].astype(str) + index_ma_gap_df_last['s_p_ma5_gap_percent']

    index_ma_gap_df_last['s_p_ma20_gap_percent'] = index_ma_gap_df_last['s_p_ma20_gap'] / index_ma_gap_df_last['S&P500'] * 100
    index_ma_gap_df_last['s_p_ma20_gap_percent'] = index_ma_gap_df_last['s_p_ma20_gap_percent'].astype(str)
    index_ma_gap_df_last['s_p_ma20_gap_percent'] = index_ma_gap_df_last['s_p_ma20_gap_percent'] + '%'
    index_ma_gap_df_last['s_p_ma20_gap_percent'] = index_ma_gap_df_last['s_p_ma20_gap_percent'].str[:5]
    index_ma_gap_df_last['s_p_ma20_gap_percent'] = ' (' + index_ma_gap_df_last['s_p_ma20_gap_percent'] + ')'
    index_ma_gap_df_last['s_p_ma20_gap'] = index_ma_gap_df_last['s_p_ma20_gap'].astype(str) + index_ma_gap_df_last['s_p_ma20_gap_percent']

    index_ma_gap_df_last['s_p_ma60_gap_percent'] = index_ma_gap_df_last['s_p_ma60_gap'] / index_ma_gap_df_last['S&P500'] * 100
    index_ma_gap_df_last['s_p_ma60_gap_percent'] = index_ma_gap_df_last['s_p_ma60_gap_percent'].astype(str)
    index_ma_gap_df_last['s_p_ma60_gap_percent'] = index_ma_gap_df_last['s_p_ma60_gap_percent'] + '%'
    index_ma_gap_df_last['s_p_ma60_gap_percent'] = index_ma_gap_df_last['s_p_ma60_gap_percent'].str[:5]
    index_ma_gap_df_last['s_p_ma60_gap_percent'] = ' (' + index_ma_gap_df_last['s_p_ma60_gap_percent'] + ')'
    index_ma_gap_df_last['s_p_ma60_gap'] = index_ma_gap_df_last['s_p_ma60_gap'].astype(str) + index_ma_gap_df_last['s_p_ma60_gap_percent']

    index_ma_gap_df_last['s_p_ma120_gap_percent'] = index_ma_gap_df_last['s_p_ma120_gap'] / index_ma_gap_df_last['S&P500'] * 100
    index_ma_gap_df_last['s_p_ma120_gap_percent'] = index_ma_gap_df_last['s_p_ma120_gap_percent'].astype(str)
    index_ma_gap_df_last['s_p_ma120_gap_percent'] = index_ma_gap_df_last['s_p_ma120_gap_percent'] + '%'
    index_ma_gap_df_last['s_p_ma120_gap_percent'] = index_ma_gap_df_last['s_p_ma120_gap_percent'].str[:5]
    index_ma_gap_df_last['s_p_ma120_gap_percent'] = ' (' + index_ma_gap_df_last['s_p_ma120_gap_percent'] + ')'
    index_ma_gap_df_last['s_p_ma120_gap'] = index_ma_gap_df_last['s_p_ma120_gap'].astype(str) + index_ma_gap_df_last['s_p_ma120_gap_percent']

    index_ma_gap_df_last['s_p_ma200_gap_percent'] = index_ma_gap_df_last['s_p_ma200_gap'] / index_ma_gap_df_last['S&P500'] * 100
    index_ma_gap_df_last['s_p_ma200_gap_percent'] = index_ma_gap_df_last['s_p_ma200_gap_percent'].astype(str)
    index_ma_gap_df_last['s_p_ma200_gap_percent'] = index_ma_gap_df_last['s_p_ma200_gap_percent'] + '%'
    index_ma_gap_df_last['s_p_ma200_gap_percent'] = index_ma_gap_df_last['s_p_ma200_gap_percent'].str[:5]
    index_ma_gap_df_last['s_p_ma200_gap_percent'] = ' (' + index_ma_gap_df_last['s_p_ma200_gap_percent'] + ')'
    index_ma_gap_df_last['s_p_ma200_gap'] = index_ma_gap_df_last['s_p_ma200_gap'].astype(str) + index_ma_gap_df_last['s_p_ma200_gap_percent']

    #index_ma_gap_df를 나스닥, 다우, s&p 칼럼으로 나누기
    nasdq_ma_gap_df = index_ma_gap_df_last[['nasdaq_ma5_gap', 'nasdaq_ma20_gap', 'nasdaq_ma60_gap', 'nasdaq_ma120_gap', 'nasdaq_ma200_gap']]
    dow_ma_gap_df = index_ma_gap_df_last[['dow_ma5_gap', 'dow_ma20_gap', 'dow_ma60_gap', 'dow_ma120_gap', 'dow_ma200_gap']]
    s_p_ma_gap_df = index_ma_gap_df_last[['s_p_ma5_gap', 's_p_ma20_gap', 's_p_ma60_gap', 's_p_ma120_gap', 's_p_ma200_gap']]
    #열이름 바꾸기
    nasdq_ma_gap_df.columns = ['MA5', 'MA20', 'MA60', 'MA120', 'MA200']
    dow_ma_gap_df.columns = ['MA5', 'MA20', 'MA60', 'MA120', 'MA200']
    s_p_ma_gap_df.columns = ['MA5', 'MA20', 'MA60', 'MA120', 'MA200']
    
    #행으로 합치기
    index_ma_gap_df = pd.concat([nasdq_ma_gap_df, dow_ma_gap_df, s_p_ma_gap_df])
   
    #행이름 바꾸기 나스닥, 다우, s&p500
    index_ma_gap_df.index = ['Nasdaq', 'DJIA', 'S&P500']
    
    #csv파일로 저장
    index_ma_gap_df.to_csv('public/index_ma_gap.csv')
    print('index_ma_gap.csv 파일 저장 완료')
    
    #index.csv파일. 뒤에서 200개 row만 남기기
    index_df = index_df.tail(200)
    #D200index.csv파일로 저장
    index_df.to_csv('public/D200index.csv')
    print('D200index.csv 파일 저장 완료')


#함수 정의  QQQ, SOXX, XBI, XOP, IYH 차트 데이터를 2012~ 오늘까지 가져옴

def get_data():
    #QQQ, SOXX, XBI, XOP, IYH ticker
    tickers = ['QQQ', 'SOXX', 'XBI', 'XOP', 'IYH']
    #오늘 날짜
    today = dt.date.today()
    #2012년 1월 1일
    start = dt.date(2012,1,1)
    #ticker별로 데이터 가져오기
    for ticker in tickers:
        globals()[ticker] = yf.download(ticker, start, today)
        #데이터 프레임으로 변환
        globals()[ticker] = pd.DataFrame(globals()[ticker])
        #종가만 가져오기
        globals()[ticker] = globals()[ticker]['Close']
        #컬럼 이름 변경
        globals()[ticker].name = ticker
        #컬럼 이름 변경
        globals()[ticker].columns = [ticker]
        #컬럼 이름 변경
        globals()[ticker].index.name = 'Date'
        #1초 쉬기
        time.sleep(1)
    #데이터프레임 합치기
    df = pd.concat([QQQ, SOXX, XBI, XOP, IYH], axis=1)
    #데이터프레임 저장
    df.to_csv('public/ETF.csv')
    #데이터프레임 출력
    print(df)

    #전일 대비 변화율 구하기
    df['QQQ_chg'] = df['QQQ'].pct_change() * 100
    df['SOXX_chg'] = df['SOXX'].pct_change() * 100
    df['XBI_chg'] = df['XBI'].pct_change() * 100
    df['XOP_chg'] = df['XOP'].pct_change() * 100
    df['IYH_chg'] = df['IYH'].pct_change() * 100

    #위 칼럼들만 가져오기
    df = df[['QQQ_chg', 'SOXX_chg', 'XBI_chg', 'XOP_chg', 'IYH_chg']]
    #칼럼명 변경
    df.columns = ['QQQ', 'SOXX', 'XBI', 'XOP', 'IYH']
    #데이터프레임 아래 10개만 자르기
    df = df.tail(10)
    
    #날짜 %Y-%m-%d 형식으로 변경
    df.index = df.index.strftime('%Y-%m-%d')

    #소수점 2자리 반올림
    df = df.round(2)

    #% 표시
    df = df.astype(str) + '%'


    #데이터프레임 저장
    df.to_csv('public/ETF_chg.csv')
    #저장 완료
    print('저장 완료')

    #ETF.csv 파일 읽기
    df = pd.read_csv('public/ETF.csv')
    #자르기 아래 365개
    df = df.tail(365)
    #날짜 %Y-%m-%d 형식으로 변경
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    #날짜를 인덱스로 설정
    df.set_index('Date', inplace=True)
    #-1-1 사이로 scale 하기
    df = (df - df.min()) / (df.max() - df.min()) * 2 - 1
    #데이터프레임 저장
    df.to_csv('public/ETF_scale.csv')
    #저장 완료
    print('저장 완료')


#함수 정의 shy, iet, tlt 차트 데이터를 2012~ 오늘까지 가져옴
def get_bond_data():
    #shy, iet, tlt ticker
    tickers = ['SHY', 'IEF', 'TLT']
    #오늘 날짜
    today = dt.date.today()
    #2012년 1월 1일
    start = dt.date(2012,1,1)
    #ticker별로 데이터 가져오기
    for ticker in tickers:
        globals()[ticker] = yf.download(ticker, start, today)
        #데이터 프레임으로 변환
        globals()[ticker] = pd.DataFrame(globals()[ticker])
        #종가만 가져오기
        globals()[ticker] = globals()[ticker]['Close']
        #컬럼 이름 변경
        globals()[ticker].name = ticker
        #컬럼 이름 변경
        globals()[ticker].columns = [ticker]
        #컬럼 이름 변경
        globals()[ticker].index.name = 'Date'
        #1초 쉬기
        time.sleep(1)
    #데이터프레임 합치기
    df = pd.concat([SHY, IEF, TLT], axis=1)
    #데이터프레임 저장
    df.to_csv('public/bond.csv')
    #데이터프레임 출력
    print(df)

    #전일 대비 변화율 구하기
    df['SHY_chg'] = df['SHY'].pct_change() * 100
    df['IEF_chg'] = df['IEF'].pct_change() * 100
    df['TLT_chg'] = df['TLT'].pct_change() * 100

    #위 칼럼들만 가져오기
    df = df[['SHY_chg', 'IEF_chg', 'TLT_chg']]
    #칼럼명 변경
    df.columns = ['SHY', 'IEF', 'TLT']
    #데이터프레임 아래 10개만 자르기
    df = df.tail(10)
    print(df)
    
    #소수점 2자리까지 표시
    df = df.round(2)

    #%기호 붙이기
    df = df.astype(str) + '%'

    #데이터프레임 저장
    df.to_csv('public/bond_chg.csv')
    #데이터프레임 출력
    print(df)

    #기준금리 읽어오기
    df = pd.read_csv('public/baseRate.csv')
    #'발표일' 컬럼을 'Date'로 변경
    df = df.rename(columns={'발표일':'Date'})
    #'년 '을 -로 변경, '월 '도 -로 변경, 일은 공백으로 변경
    df['Date'] = df['Date'].str.replace('년 ', '-')
    df['Date'] = df['Date'].str.replace('월 ', '-')
    df['Date'] = df['Date'].str.replace('일', '')
    #Date 컬럼을 인덱스로 변경
    df = df.set_index('Date')

    #bond.csv도 읽어오기
    df2 = pd.read_csv('public/bond.csv')
    
    #Date를 인덱스로 변경
    df2 = df2.set_index('Date')
    #데이터프레임 합치기
    df = pd.concat([df, df2], axis=1)
    
    #데이터프레임 날짜 순서대로 정렬
    df = df.sort_index()

    #칼럼 '실제'를 '기준금리'로 변경
    df = df.rename(columns={'실제':'기준금리'})

    #칼럼 고르기
    df = df[['기준금리', 'SHY', 'IEF', 'TLT']]

    #NAN 앞으로  값으로 쭉 채우기
    df = df.fillna(method='ffill')

    #오늘보다 앞선 값 제거
    #df = df[df.index <= today]
    #'<=' not supported between instances of 'str' and 'datetime.date'
    #문자열과 날짜를 비교할 수 없다는 에러가 뜸
    #문자열로 바꿔주기
    df = df[df.index <= str(today)]

    #NaN값 있는 행제거
    df = df.dropna()

    #데이터프레임 저장
    df.to_csv('public/bond_rate.csv')
    #출력
    print(df)

    
       
#함수실행    
get_index()
get_ma()
get_index_ma()
    
#실행
get_data()

#함수 실행
get_bond_data()

#상관계수 구하기
def get_corr():
    #index_2012.csv 읽어오기
    df = pd.read_csv('public/index_2012.csv')
    #Date를 인덱스로 변경
    df = df.set_index('Date')
    #ETF.csv 읽어오기
    df2 = pd.read_csv('public/ETF.csv')
    #Date를 인덱스로 변경
    df2 = df2.set_index('Date')
    #bond_rate.csv 읽어오기
    df3 = pd.read_csv('public/bond_rate.csv')
    #Date를 인덱스로 변경
    df3 = df3.set_index('Date')
    #'기준금리' 칼럼 제거
    df3 = df3.drop('기준금리', axis=1)
    #데이터프레임 합치기
    df = pd.concat([df, df2, df3], axis=1)
    print(df)
    #상관계수 구하기
    df = df.corr()
    print(df)
    #소수점 2자리까지 표시
    df = df.round(2)
    
    #데이터프레임 저장
    df.to_csv('public/corr.csv')
get_corr()