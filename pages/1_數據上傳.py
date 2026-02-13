"""數據上傳頁面 - 支援 CSV、Excel；Colab 可從 base directory 選檔"""
import os
import streamlit as st
import pandas as pd

# 使用共用的 base directory（本機 / Colab）
try:
    from config import BASE_DIR, path_under_base
except ImportError:
    BASE_DIR = os.path.abspath(os.getcwd())
    def path_under_base(*parts):
        return os.path.join(BASE_DIR, *parts)

st.set_page_config(page_title="數據上傳", page_icon="📤", layout="wide")
st.title("📤 數據上傳")

if "df" not in st.session_state:
    st.session_state.df = None

# 從 base directory 列出可選的 CSV/Excel（Colab 或已放檔案的目錄時有用）
csv_ext = (".csv", ".xlsx", ".xls")
try:
    base_files = [f for f in os.listdir(BASE_DIR) if f.lower().endswith(csv_ext)]
except (OSError, PermissionError):
    base_files = []

use_path = False
if base_files:
    choice = st.radio("來源", ["上傳檔案", f"從工作目錄選擇（{BASE_DIR}）"], horizontal=True)
    use_path = choice.startswith("從工作目錄")
    if use_path:
        selected = st.selectbox("選擇檔案", base_files, key="upload_select")
        load_path = path_under_base(selected) if selected else None
    else:
        load_path = None
else:
    load_path = None

if load_path and os.path.isfile(load_path):
    try:
        if load_path.lower().endswith(".csv"):
            df = pd.read_csv(load_path, encoding="utf-8")
        else:
            df = pd.read_excel(load_path, engine="openpyxl")
        st.session_state.df = df
        st.success(f"已從工作目錄載入 {len(df):,} 筆資料、{len(df.columns)} 個欄位。")
        with st.expander("預覽資料（前 10 筆）"):
            st.dataframe(df.head(10), use_container_width=True)
    except Exception as e:
        st.error(f"讀取失敗：{e}")
        st.session_state.df = None
else:
    uploaded = st.file_uploader(
        "選擇 CSV 或 Excel 檔案",
        type=["csv", "xlsx", "xls"],
        help="支援 .csv、.xlsx、.xls；Colab 可改從工作目錄選檔",
    )

    if uploaded is not None:
        try:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded, encoding="utf-8")
            else:
                df = pd.read_excel(uploaded, engine="openpyxl")
            st.session_state.df = df
            st.success(f"已載入 {len(df):,} 筆資料、{len(df.columns)} 個欄位。")
            with st.expander("預覽資料（前 10 筆）"):
                st.dataframe(df.head(10), use_container_width=True)
        except Exception as e:
            st.error(f"讀取失敗：{e}")
            st.session_state.df = None
    else:
        if st.session_state.df is not None:
            st.info("目前已有載入的資料。若要更換，請重新上傳或從工作目錄選擇。")
            st.dataframe(st.session_state.df.head(20), use_container_width=True)
        else:
            st.warning("請上傳 CSV 或 Excel 檔案以開始分析。")
