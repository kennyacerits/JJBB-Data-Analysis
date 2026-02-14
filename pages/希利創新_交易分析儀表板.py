"""
希利創新娃娃機 交易分析儀表板
資料來源：../數據分析/BI_希利創新/output/ 或 ../數據分析/希利創新/output/ 之「希利創新娃娃機_每日交易明細.csv」（已彙總各門市各支付別筆數與金額）
"""
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

try:
    from config import BASE_DIR
except ImportError:
    BASE_DIR = os.path.abspath(os.getcwd())

# 彙總檔檔名
HILI_SUMMARY_FILENAME = "希利創新娃娃機_每日交易明細.csv"
# 彙總檔必要欄位（對應儀表板：店名、日期、支付別、金額）
REQUIRED_COLS = ["交易日期", "商店通稱", "支付工具", "金額"]


def _resolve_hili_summary_path():
    """解析彙總檔路徑：環境變數 > 數據分析/BI_希利創新/output > 數據分析/希利創新/output > 專案內"""
    env_file = os.environ.get("HILI_DATA_FILE")
    if env_file:
        p = os.path.abspath(os.path.expanduser(env_file))
        if os.path.isfile(p):
            return p
    candidates = [
        os.path.join(BASE_DIR, "..", "數據分析", "BI_希利創新", "output", HILI_SUMMARY_FILENAME),
        os.path.join(BASE_DIR, "..", "數據分析", "希利創新", "output", HILI_SUMMARY_FILENAME),
        os.path.join(BASE_DIR, "..", "..", "數據分析", "BI_希利創新", "output", HILI_SUMMARY_FILENAME),
        os.path.join(BASE_DIR, "..", "..", "數據分析", "希利創新", "output", HILI_SUMMARY_FILENAME),
        os.path.join(BASE_DIR, "數據分析", "希利創新", "output", HILI_SUMMARY_FILENAME),
        os.path.join(BASE_DIR, "數據分析", "BI_希利創新", "output", HILI_SUMMARY_FILENAME),
    ]
    for p in candidates:
        resolved = os.path.abspath(p)
        if os.path.isfile(resolved):
            return resolved
    return os.path.abspath(candidates[0])


def load_summary_csv(path_or_file, encoding="utf-8"):
    """載入每日交易明細彙總檔，回傳標準化 DataFrame（店名、日期、支付別、金額）。"""
    if hasattr(path_or_file, "read"):
        df = pd.read_csv(path_or_file, encoding=encoding)
    else:
        df = pd.read_csv(path_or_file, encoding=encoding)
    if not all(c in df.columns for c in REQUIRED_COLS):
        return None, f"缺少欄位，需含：{', '.join(REQUIRED_COLS)}"
    df = df.copy()
    df["日期"] = pd.to_datetime(df["交易日期"], errors="coerce")
    df = df.dropna(subset=["日期"])
    df["店名"] = df["商店通稱"].astype(str).str.strip()
    df["支付別"] = df["支付工具"].fillna("現金").astype(str).str.strip().replace("", "現金")
    df["金額"] = pd.to_numeric(df["金額"], errors="coerce").fillna(0)
    return df[["店名", "日期", "支付別", "金額"]], None


def load_hili_data(file_path=None, uploaded_file=None):
    """載入希利創新資料。file_path 為彙總檔路徑，或 uploaded_file 為上傳檔案。回傳 (df, error_msg)。"""
    if uploaded_file is not None:
        return load_summary_csv(uploaded_file)
    if file_path and os.path.isfile(file_path):
        return load_summary_csv(file_path)
    return None, None


def build_summary_table(df, date_min, date_max):
    if df.empty:
        return pd.DataFrame()
    days = max(1, (date_max - date_min).days + 1)
    g = df.groupby("店名").agg(累積營收=("金額", "sum")).reset_index()
    g["平均日營收"] = (g["累積營收"] / days).round(0)
    g["預估月營收"] = (g["平均日營收"] * 30).round(0)
    g["預估年營收"] = (g["平均日營收"] * 365).round(0)
    cols = ["店名", "累積營收", "平均日營收", "預估月營收", "預估年營收"]
    total_row = {"店名": "總計", "累積營收": g["累積營收"].sum(), "平均日營收": g["平均日營收"].sum(),
                 "預估月營收": g["預估月營收"].sum(), "預估年營收": g["預估年營收"].sum()}
    g = pd.concat([g, pd.DataFrame([total_row])], ignore_index=True)
    store_only = g[g["店名"] != "總計"]
    avg_row = {"店名": "平均值", "累積營收": store_only["累積營收"].mean().round(0),
               "平均日營收": store_only["平均日營收"].mean().round(0),
               "預估月營收": store_only["預估月營收"].mean().round(0),
               "預估年營收": store_only["預估年營收"].mean().round(0)}
    g = pd.concat([g, pd.DataFrame([avg_row])], ignore_index=True)
    operating = store_only[store_only["累積營收"] > 0]
    if not operating.empty:
        avg_op_row = {"店名": "平均值（營業中）", "累積營收": operating["累積營收"].mean().round(0),
                      "平均日營收": operating["平均日營收"].mean().round(0),
                      "預估月營收": operating["預估月營收"].mean().round(0),
                      "預估年營收": operating["預估年營收"].mean().round(0)}
        g = pd.concat([g, pd.DataFrame([avg_op_row])], ignore_index=True)
    return g[cols]


# --- 頁面 ---
st.set_page_config(page_title="希利創新 交易分析儀表板", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
st.markdown("## 希利創新娃娃機 交易分析儀表板")

HILI_SUMMARY_PATH = _resolve_hili_summary_path()
file_exists = os.path.isfile(HILI_SUMMARY_PATH)

# 自動化：若尚無資料且彙總檔存在，自動載入
if "hili_raw_df" not in st.session_state or st.session_state["hili_raw_df"] is None:
    if file_exists:
        raw_df, err = load_hili_data(file_path=HILI_SUMMARY_PATH)
        if raw_df is not None and err is None:
            st.session_state["hili_raw_df"] = raw_df

# 側邊欄
with st.sidebar:
    st.subheader("資料來源")
    if file_exists:
        st.caption(f"已偵測到：{HILI_SUMMARY_FILENAME}")
        st.code(HILI_SUMMARY_PATH, language=None)
        if st.button("重新從預設路徑載入"):
            raw_df, err = load_hili_data(file_path=HILI_SUMMARY_PATH)
            if raw_df is not None:
                st.session_state["hili_raw_df"] = raw_df
                st.success(f"已載入 {len(raw_df):,} 筆")
            elif err:
                st.error(err)
        source = st.radio("或", ["使用已載入資料", "上傳 CSV"], key="hili_src")
    else:
        st.caption("未偵測到彙總檔。請在專案內或上一層建立 數據分析/BI_希利創新/output/（或 數據分析/希利創新/output/）並放入「希利創新娃娃機_每日交易明細.csv」，或使用「上傳 CSV」。")
        st.code(HILI_SUMMARY_PATH, language=None)
        source = "上傳 CSV"

    if source == "上傳 CSV":
        uploaded = st.file_uploader(f"上傳 {HILI_SUMMARY_FILENAME}（或同格式）", type=["csv"])
        if uploaded:
            raw_df, err = load_hili_data(uploaded_file=uploaded)
            if raw_df is not None:
                st.session_state["hili_raw_df"] = raw_df
                st.success(f"已載入 {len(raw_df):,} 筆")
            elif err:
                st.error(err)

if "hili_raw_df" not in st.session_state or st.session_state["hili_raw_df"] is None:
    st.info("請在左側上傳「希利創新娃娃機_每日交易明細.csv」，或確認預設路徑存在該檔並按「重新從預設路徑載入」。")
    st.stop()

df = st.session_state["hili_raw_df"]
date_min_all, date_max_all = df["日期"].min(), df["日期"].max()

st.subheader("交易日期篩選")
col_y1, col_m1, col_d1, col_y2, col_m2, col_d2 = st.columns(6)
with col_y1:
    y1 = st.number_input("起始年", value=date_min_all.year, min_value=date_min_all.year, max_value=date_max_all.year, key="y1")
with col_m1:
    m1 = st.number_input("起始月", value=date_min_all.month, min_value=1, max_value=12, key="m1")
with col_d1:
    d1 = st.number_input("起始日", value=date_min_all.day, min_value=1, max_value=31, key="d1")
with col_y2:
    y2 = st.number_input("結束年", value=date_max_all.year, min_value=date_min_all.year, max_value=date_max_all.year, key="y2")
with col_m2:
    m2 = st.number_input("結束月", value=date_max_all.month, min_value=1, max_value=12, key="m2")
with col_d2:
    d2 = st.number_input("結束日", value=date_max_all.day, min_value=1, max_value=31, key="d2")

try:
    filter_start = datetime(y1, m1, d1).date()
    filter_end = datetime(y2, m2, d2).date()
except ValueError:
    filter_start, filter_end = date_min_all.date(), date_max_all.date()

df_f = df[(df["日期"].dt.date >= filter_start) & (df["日期"].dt.date <= filter_end)].copy()
if df_f.empty:
    st.warning("篩選區間內無資料。")
    st.stop()

stat_days = max(1, (filter_end - filter_start).days + 1)
last_date = df_f["日期"].max().strftime("%Y-%m-%d")
store_count = df_f["店名"].nunique()
summary = build_summary_table(df_f, pd.Timestamp(filter_start), pd.Timestamp(filter_end))

st.subheader("資料重整")
c1, c2, c3 = st.columns(3)
c1.metric("最後交易日", last_date)
c2.metric("統計日數", stat_days)
c3.metric("營運通路數", store_count)
st.dataframe(summary, use_container_width=True, hide_index=True)

left, right = st.columns(2)
with left:
    st.subheader("各支付別交易金額比")
    pay_agg = df_f.groupby("支付別")["金額"].sum().reset_index(name="金額")
    if not pay_agg.empty:
        st.plotly_chart(px.pie(pay_agg, values="金額", names="支付別"), use_container_width=True)
with right:
    st.subheader("各門市交易總金額比較")
    store_options = sorted(df_f["店名"].unique())
    selected_stores = st.multiselect("門市篩選", store_options, default=store_options, key="store_filter")
    df_store = df_f[df_f["店名"].isin(selected_stores)].groupby("店名")["金額"].sum().sort_values(ascending=True)
    if not df_store.empty:
        st.plotly_chart(px.bar(x=df_store.values, y=df_store.index, orientation="h", labels={"x": "交易金額", "y": "門市"}), use_container_width=True)

st.subheader("希利創新娃娃機每日交易金額")
daily = df_f.groupby("日期")["金額"].sum().reset_index()
st.plotly_chart(px.line(daily, x="日期", y="金額"), use_container_width=True)

st.subheader("各支付別金額占比（依日期）")
pay_daily = df_f.pivot_table(index="日期", columns="支付別", values="金額", aggfunc="sum", fill_value=0)
pay_daily_pct = pay_daily.div(pay_daily.sum(axis=1), axis=0).fillna(0) * 100
pay_daily_pct = pay_daily_pct.reset_index()
fig_stack = go.Figure()
for col in pay_daily_pct.columns:
    if col == "日期":
        continue
    fig_stack.add_trace(go.Scatter(x=pay_daily_pct["日期"], y=pay_daily_pct[col], name=col, stackgroup="one", mode="lines"))
fig_stack.update_layout(yaxis_title="占比 (%)", xaxis_title="日期", hovermode="x unified")
st.plotly_chart(fig_stack, use_container_width=True)

st.subheader("單一門市細部")
store_detail = st.selectbox("選擇門市", ["（全部）"] + sorted(df_f["店名"].unique()), key="store_detail")
if store_detail != "（全部）":
    df_s = df_f[df_f["店名"] == store_detail]
    r1, r2 = st.columns(2)
    with r1:
        st.markdown(f"**{store_detail} 每日交易金額**")
        st.plotly_chart(px.line(df_s.groupby("日期")["金額"].sum().reset_index(), x="日期", y="金額"), use_container_width=True)
    with r2:
        st.markdown(f"**{store_detail} 各支付別金額**")
        st.plotly_chart(px.bar(df_s.groupby("支付別")["金額"].sum().reset_index(), x="支付別", y="金額"), use_container_width=True)
