"""視覺化頁面 - 長條圖、折線圖、散點圖、圓餅圖"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="視覺化", page_icon="📈", layout="wide")
st.title("📈 視覺化")

if "df" not in st.session_state or st.session_state.df is None:
    st.warning("請先至「數據上傳」頁面載入資料。")
    st.stop()

df = st.session_state.df
numeric_cols = list(df.select_dtypes(include=["number"]).columns)
object_cols = list(df.select_dtypes(include=["object"]).columns)

chart_type = st.selectbox(
    "圖表類型",
    ["長條圖", "折線圖", "散點圖", "圓餅圖", "直方圖"],
)

if chart_type == "長條圖":
    x_col = st.selectbox("X 軸（類別）", object_cols or list(df.columns), key="bar_x")
    y_col = st.selectbox("Y 軸（數值）", numeric_cols or list(df.columns), key="bar_y")
    if x_col and y_col:
        agg = df.groupby(x_col)[y_col].agg(["sum", "mean", "count"]).reset_index()
        agg_choice = st.radio("聚合方式", ["sum", "mean", "count"])
        fig = px.bar(agg, x=x_col, y=agg_choice, title=f"{y_col} by {x_col}")
        st.plotly_chart(fig, use_container_width=True)

elif chart_type == "折線圖":
    x_col = st.selectbox("X 軸", df.columns.tolist(), key="line_x")
    y_cols = st.multiselect("Y 軸（可多選）", numeric_cols, default=numeric_cols[:1] if numeric_cols else [])
    if x_col and y_cols:
        fig = px.line(df, x=x_col, y=y_cols, title="折線圖")
        st.plotly_chart(fig, use_container_width=True)

elif chart_type == "散點圖":
    x_col = st.selectbox("X 軸", numeric_cols or df.columns.tolist(), key="scatter_x")
    y_col = st.selectbox("Y 軸", numeric_cols or df.columns.tolist(), key="scatter_y")
    color_col = st.selectbox("顏色（選填）", [None] + list(df.columns), key="scatter_c")
    if x_col and y_col:
        fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title="散點圖")
        st.plotly_chart(fig, use_container_width=True)

elif chart_type == "圓餅圖":
    col = st.selectbox("類別欄位", object_cols or list(df.columns), key="pie_c")
    val_col = st.selectbox("數值欄位（選填）", [None] + numeric_cols, key="pie_v")
    if col:
        if val_col:
            series = df.groupby(col)[val_col].sum()
        else:
            series = df[col].value_counts()
        fig = px.pie(values=series.values, names=series.index, title=f"{col} 分布")
        st.plotly_chart(fig, use_container_width=True)

elif chart_type == "直方圖":
    col = st.selectbox("數值欄位", numeric_cols or list(df.columns), key="hist_c")
    if col:
        fig = px.histogram(df, x=col, nbins=30, title=f"{col} 分布")
        st.plotly_chart(fig, use_container_width=True)
