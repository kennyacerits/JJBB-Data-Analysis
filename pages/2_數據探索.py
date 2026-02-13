"""數據探索頁面 - 預覽、統計、缺失值、相關性"""
import streamlit as st
import pandas as pd

st.set_page_config(page_title="數據探索", page_icon="🔍", layout="wide")
st.title("🔍 數據探索")

if "df" not in st.session_state or st.session_state.df is None:
    st.warning("請先至「數據上傳」頁面載入資料。")
    st.stop()

df = st.session_state.df

tab1, tab2, tab3, tab4 = st.tabs(["資料預覽", "基本統計", "缺失值", "相關性"])

with tab1:
    st.subheader("資料表")
    rows = st.slider("顯示筆數", 5, min(100, len(df)), 20)
    st.dataframe(df.head(rows), use_container_width=True)
    st.caption(f"總筆數：{len(df):,} | 總欄位：{len(df.columns)}")

with tab2:
    st.subheader("數值型統計")
    numeric = df.select_dtypes(include=["number"])
    if numeric.empty:
        st.info("沒有數值型欄位。")
    else:
        st.dataframe(numeric.describe(), use_container_width=True)
    st.subheader("物件/類別型")
    obj = df.select_dtypes(include=["object"])
    if not obj.empty:
        for col in obj.columns:
            st.write(f"**{col}**：{obj[col].nunique()} 個相異值，範例：{list(obj[col].dropna().head(3).values)}")

with tab3:
    st.subheader("缺失值")
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if missing.empty:
        st.success("沒有缺失值。")
    else:
        st.dataframe(missing.to_frame("缺失數"), use_container_width=True)
        st.bar_chart(missing)

with tab4:
    st.subheader("數值欄位相關性")
    numeric = df.select_dtypes(include=["number"])
    if numeric.shape[1] < 2:
        st.info("至少需要兩個數值欄位才能計算相關性。")
    else:
        corr = numeric.corr()
        st.dataframe(corr.round(3), use_container_width=True)
        try:
            import plotly.express as px
            fig = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale="RdBu_r")
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            pass
