"""
希利創新娃娃機 交易分析儀表板
資料來源：SEGA_TX/希利創新/ URS-YYYY-MM-DD.csv
- 自動化：若偵測到資料目錄且有 URS-*.csv，開啟頁面時自動載入，無需手動按鈕。
"""
import os
import glob
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

try:
    from config import BASE_DIR
except ImportError:
    BASE_DIR = os.path.abspath(os.getcwd())

# 希利創新每日報表目錄：嘗試多種相對路徑（本機 Web 與 SEGA_TX 同層；雲端可能為 src/Web 且 SEGA_TX 在 repo 根）
def _resolve_hili_data_dir():
    candidates = [
        os.path.join(BASE_DIR, "..", "SEGA_TX", "希利創新"),
        os.path.join(BASE_DIR, "..", "..", "SEGA_TX", "希利創新"),
    ]
    for p in candidates:
        resolved = os.path.abspath(p)
        if os.path.isdir(resolved):
            return resolved
    return os.path.abspath(candidates[0])

HILI_DATA_DIR = _resolve_hili_data_dir()
REQUIRED_COLS = ["商店名稱", "交易日期", "是否退款", "發卡公司", "實際扣款金額"]


def _store_short_name(full_name):
    if pd.isna(full_name) or not isinstance(full_name, str):
        return full_name
    s = full_name.strip()
    return s.split()[-1] if " " in s else s


def load_urs_csv(path_or_file, encoding="utf-8"):
    if hasattr(path_or_file, "read"):
        df = pd.read_csv(path_or_file, encoding=encoding)
    else:
        df = pd.read_csv(path_or_file, encoding=encoding)
    if not all(c in df.columns for c in REQUIRED_COLS):
        return None
    df = df[df["是否退款"].astype(str).str.strip() != "是"].copy()
    df["交易日期"] = pd.to_numeric(df["交易日期"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["交易日期"])
    df["日期"] = pd.to_datetime(df["交易日期"].astype(str), format="%Y%m%d", errors="coerce")
    df = df.dropna(subset=["日期"])
    df["店名"] = df["商店名稱"].map(_store_short_name)
    df["支付別"] = df["發卡公司"].fillna("現金").astype(str).str.strip().replace("", "現金")
    df["金額"] = pd.to_numeric(df["實際扣款金額"], errors="coerce").fillna(0)
    return df[["店名", "日期", "支付別", "金額", "交易日期"]]


def load_hili_data(data_dir=None, uploaded_files=None):
    if uploaded_files:
        dfs = []
        for f in uploaded_files:
            if f.name.lower().endswith(".csv"):
                try:
                    df = load_urs_csv(f)
                    if df is not None:
                        dfs.append(df)
                except Exception as e:
                    return None, f"讀取 {f.name} 失敗：{e}"
        if not dfs:
            return None, "沒有可用的 URS 格式 CSV"
        return pd.concat(dfs, ignore_index=True), None

    if not data_dir or not os.path.isdir(data_dir):
        return None, None
    files = sorted(glob.glob(os.path.join(data_dir, "URS-*.csv")))
    if not files:
        return None, f"目錄內沒有 URS-*.csv：{data_dir}"
    dfs = []
    for path in files:
        try:
            df = load_urs_csv(path)
            if df is not None:
                dfs.append(df)
        except Exception as e:
            return None, f"讀取 {os.path.basename(path)} 失敗：{e}"
    if not dfs:
        return None, "沒有符合欄位格式的檔案"
    return pd.concat(dfs, ignore_index=True), None


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

# 自動化：若尚無資料且資料目錄存在且有 URS-*.csv，自動載入
if "hili_raw_df" not in st.session_state or st.session_state["hili_raw_df"] is None:
    if os.path.isdir(HILI_DATA_DIR):
        files = glob.glob(os.path.join(HILI_DATA_DIR, "URS-*.csv"))
        if files:
            raw_df, err = load_hili_data(data_dir=HILI_DATA_DIR)
            if raw_df is not None and err is None:
                st.session_state["hili_raw_df"] = raw_df

# 側邊欄：資料來源與手動選項
with st.sidebar:
    st.subheader("資料來源")
    use_dir = os.path.isdir(HILI_DATA_DIR)
    if use_dir:
        st.caption(f"目錄：{HILI_DATA_DIR}")
        if st.button("重新從目錄載入"):
            raw_df, err = load_hili_data(data_dir=HILI_DATA_DIR)
            if raw_df is not None:
                st.session_state["hili_raw_df"] = raw_df
                st.success(f"已載入 {len(raw_df):,} 筆")
            elif err:
                st.error(err)
        source = st.radio("或", ["使用已載入資料", "上傳 CSV"], key="hili_src")
    else:
        st.caption(f"未偵測到目錄：{HILI_DATA_DIR}")
        source = "上傳 CSV"

    if source == "上傳 CSV":
        uploaded = st.file_uploader("上傳 URS-*.csv（可多檔）", type=["csv"], accept_multiple_files=True)
        if uploaded:
            raw_df, err = load_hili_data(uploaded_files=uploaded)
            if raw_df is not None:
                st.session_state["hili_raw_df"] = raw_df
                st.success(f"已載入 {len(raw_df):,} 筆")
            elif err:
                st.error(err)

if "hili_raw_df" not in st.session_state or st.session_state["hili_raw_df"] is None:
    st.info("請在左側「上傳 CSV」或確認資料目錄存在並按「重新從目錄載入」。")
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
