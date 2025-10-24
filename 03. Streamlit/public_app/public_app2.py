import streamlit as st
import pandas as pd
import plotly.express  as px

# [TODO] 아래 summary를 참고하여 막대 그래프와 라인 그래프를 그리는 함수를 구성해봅니다.
"""_summary_
fig = px.bar(bar_df, 
                title="",
                y='',
                color="",
                hover_data='')

fig = px.line(line_df,x="일시",y="",
            title="",
            color='',
            line_group='',
            hover_name="")
"""
def bar_chart(*geo):
    bar_df = edited_df[edited_df["선택"]]
    fig = _______
    return fig
    
def line_chart(*geo):
    line_df = df[df["구분"].apply(lambda x: x in geo)]
    fig = [TODO]
    return fig


# 페이지 구성
df = pd.read_csv("seoul.csv")
st.title("서울시 미세먼지 분포")

pivot_table = pd.pivot_table(df,index="구분",values=["미세먼지(PM10)","초미세먼지(PM2.5)"],aggfunc="mean")
pivot_table["선택"] = pivot_table["미세먼지(PM10)"].apply(lambda x: False)
pivot_table[["미세먼지","초미세먼지"]] = pivot_table[["미세먼지(PM10)","초미세먼지(PM2.5)"]]
del pivot_table["미세먼지(PM10)"]
del pivot_table["초미세먼지(PM2.5)"]


col1, col2 = st.columns([0.5,0.5])

with col1:
    st.write("\n\n")
    edited_df = st.data_editor(pivot_table)

edited_df["지역구"] = edited_df.index
select = list(edited_df[edited_df["선택"]]["지역구"])

with col2:
    tab1,tab2 = st.tabs(["Bar chart","Line chart"])
    
    with tab1:
        # [TODO] st.plotly_chart를 사용하여 bar chart를 해당 위치에 삽입합니다.
        __________
        
    with tab2:
        # [TODO] st.plotly_chart를 사용하여 line chart를 해당 위치에 삽입합니다.
        ___________
    
