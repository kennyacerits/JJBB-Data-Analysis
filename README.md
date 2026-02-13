# 網頁數據分析與發布系統

以 **Streamlit** 建置的數據分析與報告發布系統，支援上傳 CSV/Excel、探索、視覺化與一鍵產生報告。

## 功能

- **數據上傳**：支援 CSV、Excel（.xlsx / .xls），自動解析欄位
- **數據探索**：資料預覽、基本統計、缺失值、數值相關性熱力圖
- **視覺化**：長條圖、折線圖、散點圖、圓餅圖、直方圖（Plotly 互動圖表）
- **報告發布**：產生 Markdown 或 HTML 報告並下載

## 環境需求

- Python 3.9+
- 依賴見 `requirements.txt`

## 安裝與執行

```bash
# 進入專案目錄
cd Web

# 建立虛擬環境（建議）
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

# 啟動 Streamlit
streamlit run app.py
```

瀏覽器會自動開啟，若未開啟請至：**http://localhost:8501**

## 發布到 Google Colab

1. 將專案上傳到 Colab（或複製到 Google Drive 後掛載）。
2. 在 Colab 儲存格執行：

```python
# 安裝依賴
!pip install -q -r requirements.txt

# 指定工作目錄（選用）：預設為 /content；若檔案在 Drive 可設為掛載路徑
import os
os.environ["STREAMLIT_BASE_DIR"] = "/content"  # 或 "/content/drive/MyDrive/你的資料夾"

# 啟動 Streamlit（Colab 需用 headless 並配合 ngrok 或內建連結）
!streamlit run app.py --server.headless true --server.port 8501
```

3. 若使用 **ngrok** 取得對外網址：
   - `!pip install -q pyngrok`
   - 在 `streamlit run` 前執行 ngrok 指向 8501，並用產生的 URL 開啟。

**Base directory 說明**  
- 程式會自動判斷是否在 Colab 執行；工作目錄（base directory）預設為：
  - **本機**：執行 `streamlit run` 時的當前目錄（`os.getcwd()`）。
  - **Colab**：`/content`（可寫入），或由環境變數 `STREAMLIT_BASE_DIR`（或 `BASE_DIR`）指定。
- 在 Colab 若先把 CSV/Excel 放到該目錄，於「數據上傳」頁可選擇「從工作目錄選擇」載入，無需再上傳檔案。

## 專案結構

```
Web/
├── app.py              # 主程式（首頁）
├── config.py           # 環境與路徑（Colab/本機、BASE_DIR）
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml     # Streamlit 主題與設定
└── pages/
    ├── 1_數據上傳.py
    ├── 2_數據探索.py
    ├── 3_視覺化.py
    └── 4_報告發布.py
```

## 使用流程

1. 在 **數據上傳** 上傳 CSV 或 Excel 檔案
2. 在 **數據探索** 檢視表格、統計與缺失值
3. 在 **視覺化** 選擇圖表類型與欄位產出圖表
4. 在 **報告發布** 設定選項後產生並下載報告

## 發布到 Streamlit Community Cloud

發布前請先完成以下事項：

### 1. 事前準備

| 項目 | 說明 |
|------|------|
| **GitHub 帳號** | 到 [github.com](https://github.com) 註冊或登入 |
| **專案放上 GitHub** | 把此專案推送到一個 **public** 儲存庫（免費方案須為公開） |
| **必要檔案** | 專案根目錄要有 `app.py`、`requirements.txt`（已具備） |
| **選用** | `runtime.txt` 可指定 Python 版本（如 `python-3.11`），已加入 |

### 2. 推送到 GitHub 的步驟（若尚未使用 Git）

```bash
cd Web
git init
git add .
git commit -m "Initial: 數據分析與發布系統"
# 在 GitHub 建立新 repo（例如取名 streamlit-data-app），不要勾選 README
git remote add origin https://github.com/你的帳號/streamlit-data-app.git
git branch -M main
git push -u origin main
```

### 3. 在 Streamlit Cloud 部署

1. 開啟 **[share.streamlit.io](https://share.streamlit.io)**，用 **Sign in with GitHub** 登入。
2. 點 **Deploy an app**。
3. 選擇剛推送的 **Repository**、**Branch**（通常 `main`）。
4. **Main file path** 填：`app.py`（若 repo 根目錄就是此專案）。
   - 若 repo 根目錄是上一層、專案在 `Web/` 資料夾內，則在進階設定裡把 **Root directory** 設為 `Web`，Main file path 設為 `app.py`。
5. 點 **Deploy**，等待建置完成即可取得公開網址。

### 4. 注意事項

- 免費方案為 **public repo** 才能部署；若有敏感資訊請勿上傳。
- 機密設定可於 Streamlit Cloud 專案頁 **Settings → Secrets** 以 TOML 格式填入，程式內用 `st.secrets` 讀取。
- 部署後「從工作目錄選擇」會是雲端暫存目錄，使用者主要仍以上傳檔案方式使用即可。

## 授權

僅供學習與內部使用。
