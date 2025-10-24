import streamlit as st
import pandas as pd
import plotly.express  as px
from streamlit_folium import folium_static
# 지도 라이브러리 folium을 import 합니다.
import folium

st.set_page_config(layout="wide")
# cache 적용
@st.cache_data
def bar_chart(*geo):
    bar_df = edited_df[edited_df["선택"]]
    fig = px.bar(bar_df, 
                 title="서울시 구별 미세먼지",
                 y='미세먼지',
                 color="지역구",
                 hover_data='미세먼지')
    return fig

@st.cache_data
def line_chart(*geo):
    line_df = df[df["구분"].apply(lambda x: x in geo)]
    fig = px.line(line_df,x="일시",y="초미세먼지(PM2.5)",
              title="서울시 구별 미세먼지",
              color='구분',
              line_group='구분',
              hover_name="구분")
    return fig


# 페이지 구성
df = pd.read_csv("seoul.csv")

pivot_table = pd.pivot_table(df,index="구분",values=["미세먼지(PM10)","초미세먼지(PM2.5)"],aggfunc="mean")
pivot_table["선택"] = pivot_table["미세먼지(PM10)"].apply(lambda x: False)
pivot_table[["미세먼지","초미세먼지"]] = pivot_table[["미세먼지(PM10)","초미세먼지(PM2.5)"]]
del pivot_table["미세먼지(PM10)"]
del pivot_table["초미세먼지(PM2.5)"]


col1, col2 = st.columns([0.4,0.6])

with col1:
    st.title("서울시 미세먼지 분포")
    st.write("\n\n")
    edited_df = st.data_editor(pivot_table)

edited_df["지역구"] = edited_df.index
select = list(edited_df[edited_df["선택"]]["지역구"])

with col2:
    tab1,tab2,tab3 = st.tabs(["Bar chart","Line chart","Map chart"])
    
    with tab1:
        st.plotly_chart(bar_chart(*select))
        
    with tab2:
        st.plotly_chart(line_chart(*select))

    with tab3:

        st.header("서울시 미세먼지 현황")
        m = folium.Map([37.58, 127.0], zoom_start=11)

        # [TODO] 지도위에 데이터를 탑재하여 블럭단위 시각화를 진행해봅니다.
        # 블럭 단위 구성을 위해 Seoul_Gu.json 데이터를 사용합니다.
        geo_data='./Seoul_Gu.json'
        folium.Choropleth(
            geo_data=_________, # 경계선 좌표값이 담긴 데이터
            data=edited_df[edited_df["선택"]], # Series or DataFrame 넣으면 된다
            columns=['지역구','미세먼지'], # DataFrame의 어떤 columns을 넣을지
            key_on='feature.properties.SIG_KOR_NM', # SIG_KOR_NM 값을 가져오겠다.
            fill_color='BuPu',
            fill_opacity=0.5, # 색 투명도
            line_opacity=0.5, # 선 투명도
            legend_name='미세먼지 수치 (PM10)' # 범례
        ).add_to(m)
        _________________
