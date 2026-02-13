"""
網頁數據分析與發布系統 - 主程式
使用 Streamlit 建置，支援本機與 Google Colab。
"""
import streamlit as st

# 路徑與環境設定（Colab / 本機共用）
try:
    import config as env_config
    BASE_DIR = env_config.BASE_DIR
    IS_COLAB = env_config.IS_COLAB
except ImportError:
    import os
    BASE_DIR = os.path.abspath(os.getcwd())
    IS_COLAB = False

st.set_page_config(
    page_title="數據分析與發布系統",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 自訂樣式
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #9E9E9E;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #262730 0%, #1a1b26 100%);
        padding: 1.25rem;
        border-radius: 10px;
        border-left: 4px solid #1E88E5;
        margin-bottom: 1rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📊 揪吉嗶嗶數據分析系統</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">上傳數據、探索分析、視覺化圖表、生成報告 — 一站式數據工作台</p>', unsafe_allow_html=True)

# 若尚未載入資料，提示從側邊欄或「數據上傳」頁面開始
if "df" not in st.session_state:
    st.session_state.df = None
# 供各頁面使用的 base directory（Colab 可透過環境變數 STREAMLIT_BASE_DIR 設定）
if "base_dir" not in st.session_state:
    st.session_state.base_dir = BASE_DIR
if "is_colab" not in st.session_state:
    st.session_state.is_colab = IS_COLAB

# 側邊欄：環境與路徑資訊（Colab 時特別有用）
with st.sidebar:
    st.caption("環境與路徑")
    st.code(BASE_DIR, language=None)
    if IS_COLAB:
        st.success("Google Colab 環境")
        st.caption("可設環境變數 STREAMLIT_BASE_DIR 指定工作目錄")
    else:
        st.caption("本機環境")

st.info("👈 請從左側選單選擇功能：**數據上傳** → **數據探索** → **視覺化** → **報告發布**")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("步驟 1", "數據上傳", "CSV / Excel")
with col2:
    st.metric("步驟 2", "數據探索", "預覽與統計")
with col3:
    st.metric("步驟 3", "視覺化", "圖表分析")
with col4:
    st.metric("步驟 4", "報告發布", "匯出報告")

st.divider()
st.markdown("### 快速開始")
st.markdown("""
1. **數據上傳**：上傳 CSV 或 Excel 檔案，系統會自動解析欄位類型。
2. **數據探索**：檢視資料表、缺失值、基本統計量與相關性。
3. **視覺化**：依欄位類型選擇長條圖、折線圖、散點圖或圓餅圖。
4. **報告發布**：一鍵產生分析報告並下載（Markdown 或 HTML）。
""")
