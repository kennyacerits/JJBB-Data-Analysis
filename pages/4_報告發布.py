"""報告發布頁面 - 產生並下載 Markdown / HTML 報告"""
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="報告發布", page_icon="📄", layout="wide")
st.title("📄 報告發布")

if "df" not in st.session_state or st.session_state.df is None:
    st.warning("請先至「數據上傳」頁面載入資料。")
    st.stop()

df = st.session_state.df

report_title = st.text_input("報告標題", value="數據分析報告")
include_stats = st.checkbox("包含基本統計", True)
include_preview = st.checkbox("包含資料預覽（前 20 筆）", True)
include_missing = st.checkbox("包含缺失值摘要", True)

format_choice = st.radio("匯出格式", ["Markdown (.md)", "HTML (.html)"])

def build_md():
    lines = [
        f"# {report_title}",
        "",
        f"*產生時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
        "## 資料概覽",
        f"- 筆數：{len(df):,}",
        f"- 欄位數：{len(df.columns)}",
        "",
    ]
    if include_stats:
        lines.append("## 基本統計")
        lines.append("")
        numeric = df.select_dtypes(include=["number"])
        if not numeric.empty:
            lines.append(numeric.describe().to_markdown())
            lines.append("")
    if include_missing:
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        if not missing.empty:
            lines.append("## 缺失值")
            lines.append("")
            for col, cnt in missing.items():
                lines.append(f"- **{col}**：{cnt} 筆")
            lines.append("")
    if include_preview:
        lines.append("## 資料預覽")
        lines.append("")
        lines.append(df.head(20).to_markdown(index=False))
    return "\n".join(lines)

def build_html():
    html = """<html><head><meta charset='utf-8'><style>body{font-family:sans-serif;max-width:900px;margin:2rem auto;padding:1rem;} table{border-collapse:collapse;width:100%;} th,td{border:1px solid #ddd;padding:8px;} th{background:#1E88E5;color:white;}</style></head><body>"""
    html += f"<h1>{report_title}</h1><p><em>產生時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}</em></p>"
    html += "<h2>資料概覽</h2><ul><li>筆數：" + f"{len(df):,}" + "</li><li>欄位數：" + str(len(df.columns)) + "</li></ul>"
    if include_stats:
        numeric = df.select_dtypes(include=["number"])
        if not numeric.empty:
            html += "<h2>基本統計</h2>" + numeric.describe().to_html()
    if include_missing:
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        if not missing.empty:
            html += "<h2>缺失值</h2><ul>"
            for col, cnt in missing.items():
                html += f"<li><strong>{col}</strong>：{cnt} 筆</li>"
            html += "</ul>"
    if include_preview:
        html += "<h2>資料預覽</h2>" + df.head(20).to_html(index=False)
    html += "</body></html>"
    return html

if st.button("產生報告"):
    if format_choice.startswith("Markdown"):
        content = build_md()
        suffix = "md"
        mime = "text/markdown"
    else:
        content = build_html()
        suffix = "html"
        mime = "text/html"
    st.download_button(
        "下載報告",
        data=content,
        file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.{suffix}",
        mime=mime,
        key="dl_report",
    )
    with st.expander("預覽內容"):
        if suffix == "md":
            st.markdown(content)
        else:
            st.components.v1.html(content, height=400, scrolling=True)
