import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# -----------------------------------
# 페이지 설정
# -----------------------------------
st.set_page_config(
    page_title="쉬었음 청년 분석 대시보드",
    page_icon="📊",
    layout="wide"
)

st.title("📊 쉬었음 청년 분석 대시보드")
st.markdown("""
본 대시보드는 청년층의 경제활동참가율과 쉬었음 인구 현황을 분석하기 위해 제작되었습니다.
""")

# -----------------------------------
# DB 연결
# -----------------------------------
conn = sqlite3.connect("쉬었음 청년.db")

# ===================================
# 차트 1
# 경제활동참가율 추이
# ===================================

st.header("① 청년층 경제활동참가율 추이")

sql1 = """
SELECT
    연도,
    경제활동참가율
FROM 경제활동참가율
ORDER BY 연도
"""

df1 = pd.read_sql(sql1, conn)

fig1 = px.line(
    df1,
    x="연도",
    y="경제활동참가율",
    markers=True,
    title="연도별 경제활동참가율 추이"
)

st.plotly_chart(fig1, use_container_width=True)

with st.expander("사용한 SQL 보기"):

    st.code(sql1, language="sql")

st.subheader("인사이트")

st.info("""
경제활동참가율의 연도별 변화를 통해 청년층이 노동시장에 얼마나 적극적으로 참여하고 있는지 확인할 수 있다.

그래프가 하락 추세라면 취업 포기, 구직 단념 등의 현상이 증가하고 있을 가능성을 시사한다.
""")

st.divider()

# ===================================
# 차트 2
# 전체 비경제활동인구 대비
# 청년 쉬었음 인구 비율
# ===================================

st.header("② 전체 비경제활동인구 중 청년 쉬었음 인구 비율")

sql2 = """
SELECT
    a.연도,
    a.합계 AS 비경제활동인구,
    b.쉬었음인구,
    ROUND(
        CAST(b.쉬었음인구 AS REAL)
        / a.합계 * 100,
        2
    ) AS 비율
FROM 연령별경제활동인구 a
JOIN 청년쉬었음인구 b
ON a.연도 = b.연도
ORDER BY a.연도
"""

df2 = pd.read_sql(sql2, conn)

fig2 = px.line(
    df2,
    x="연도",
    y="비율",
    markers=True,
    title="전체 비경제활동인구 대비 청년 쉬었음 인구 비율(%)"
)

st.plotly_chart(fig2, use_container_width=True)

with st.expander("사용한 SQL 보기"):

    st.code(sql2, language="sql")

st.subheader("인사이트")

st.info("""
비경제활동인구 가운데 청년 쉬었음 인구가 차지하는 비중을 확인할 수 있다.

비율이 지속적으로 증가한다면 청년층의 노동시장 이탈 현상이 심화되고 있음을 의미할 수 있다.
""")

st.divider()

# ===================================
# 차트 3
# 쉬었음 이유 분석
# ===================================

st.header("③ 연령별 쉬었음 이유 차이")

sql3 = """
SELECT
    연도,
    유형,
    연령층,
    인원수
FROM 연령별쉬었음이유
ORDER BY 연도
"""

df3 = pd.read_sql(sql3, conn)

year_list = sorted(df3["연도"].unique())

selected_year = st.selectbox(
    "연도 선택",
    year_list
)

filtered_df = df3[df3["연도"] == selected_year]

fig3 = px.bar(
    filtered_df,
    x="유형",
    y="인원수",
    color="연령층",
    barmode="group",
    title=f"{selected_year}년 연령별 쉬었음 이유"
)

st.plotly_chart(fig3, use_container_width=True)

with st.expander("사용한 SQL 보기"):

    st.code(sql3, language="sql")

st.subheader("인사이트")

st.info("""
연령대별로 쉬었음 상태에 진입하는 주요 원인을 비교할 수 있다.

청년층은 취업 준비나 진로 탐색의 비중이 높을 수 있으며,
장년층과 노년층은 건강 또는 가사 관련 이유가 상대적으로 높게 나타날 수 있다.
""")

# -----------------------------------
# 데이터 미리보기
# -----------------------------------

st.header("원본 데이터 확인")

table_option = st.selectbox(
    "테이블 선택",
    [
        "경제활동참가율",
        "연령별경제활동인구",
        "청년쉬었음인구",
        "연령별쉬었음이유"
    ]
)

preview = pd.read_sql(
    f"SELECT * FROM {table_option}",
    conn
)

st.dataframe(preview, use_container_width=True)

conn.close()