import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO  # text 파일을 제외한 binary 파일을 저장할 때 필요

def ex_rate():
    def get_exchange(currency_code):
        #currency_code = 'USD'
        last_page_num = 10
        df = pd.DataFrame()

        for page_no in range(1, last_page_num+1):
            url = f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{currency_code}KRW&page={page_no}"
            dfs = pd.read_html(url, encoding='cp949', header=1)  # 2행을 헤더로. 1행은 안가져온다

            if dfs[0].empty:
                if (page_no == 1):
                    print(f"통합코드({currency_code})가 잘못 지정되었습니다")
                else:
                    print(f"{page_no} Page : 마지막 페이지입니다")
                break

            #print(dfs[0])
            df = pd.concat([df, dfs[0]], ignore_index=False)
        return df

    currency_name_dict = {'미국 달러' : 'USD', '유럽연합 유로' : 'EUR', '일본 엔화' : 'JPY', '배트남 동화':'VND'}
    # currency_name = st.sidebar.selectbox('통화선택', currency_name_dict.keys())
    # clicked = st.sidebar.button('환율데이터 가져오기')
    currency_name = st.selectbox('통화선택', currency_name_dict.keys())
    clicked = st.button('환율데이터 가져오기')

    if clicked:
        currency_code = currency_name_dict[currency_name]
        df_exchange = get_exchange(currency_code)
        #print(df_exchange)

        #원하는 열만 선택
        df_exchange_rate = df_exchange[['날짜', '매매기준율', '사실 때','파실 때', '보내실 때', '받으실 때']]
        df_exchange_rate2 = df_exchange_rate.set_index('날짜')

        #날짜데이터 타입 변경
        df_exchange_rate2.index = pd.to_datetime(df_exchange_rate2.index)

        # 환율 데이터 표시
        st.subheader(f"{currency_name}의 환율 데이터")
        st.dataframe(df_exchange_rate2)

        #한글
        matplotlib.rcParams['font.family'] = 'Malgun Gothic'

        # 차트(선 그래프) 그리기
        ax = df_exchange_rate2['매매기준율'].plot(figsize=(15,6), grid=True)
        ax.set_title("환율(매매기준율 그래프)", fontsize=13)
        ax.set_xlabel("기간", fontsize=10)
        ax.set_ylabel(f"원화 / {currency_name}", fontsize=10)
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        fig = ax.get_figure()   # fig 객체 가져오기
        st.pyplot(fig)

        # 파일 다운로드
        st.text("** 환율 데이터 파일 다운로드 **")
        # 데이터프레임 데이터를 csv 데이터로 변환    
        save_csv = df_exchange_rate.to_csv()
        # 데이터프레임 데이터를 excel 데이터로 변환
        save_excel = BytesIO()  # 메모리 버퍼에 바이너리 객체 생성
        df_exchange_rate.to_excel(save_excel)  # 엑셀형식으로 버퍼에 쓰기

        col = st.columns(2)  # 2개의 세로단 생성
        with col[0]:
            st.download_button("csv file 다운로드", save_csv, file_name=f"{currency_name}_환율데이터.csv")
        
        with col[1]:
            st.download_button("excel file 다운로드", save_excel, file_name=f"{currency_name}_환율데이터.xlsx")

    else:
        pass