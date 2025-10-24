import streamlit as st
import pandas as pd
import plotly.express  as px

# 페이지 구성
df = pd.read_csv("seoul.csv")
st.title("서울시 미세먼지 분포")

pivot_table = pd.pivot_table(df,index="구분",values=["미세먼지(PM10)","초미세먼지(PM2.5)"],aggfunc="mean")
pivot_table["선택"] = pivot_table["미세먼지(PM10)"].apply(lambda x: False)

# [TODO] 화면을 두개의 컬럼으로 구성하고, 두번째 컬럼을 다시 두개의 탭으로 구성해봅시다.

col1, col2 = ____________

with col1:
    edited_df = st.data_editor(pivot_table)
    
with col2:
    tab1,tab2 = st.tabs(["Bar chart","Line chart"])
    
    # [TODO] 아래 코드를 완성해주세요.
