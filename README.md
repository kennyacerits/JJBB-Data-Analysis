# 網頁數據分析與發布系統

以 **Streamlit** 建置的數據分析與報告發布系統，支援上傳 CSV/Excel、探索、視覺化與一鍵產生報告。

## 功能

### 第一層功能

- **揪吉嗶嗶整體數據分析**  
  陸續將所有 SEGA\* 及希利創新的報表檔（CSV、Excel）與統計圖表功能納入，呈現總體數據。
- **SEGA 寶可夢 數據分析**  
  待整合（目前檔案在 Google Drive 以外目錄）。
- **SEGA 星夢 數據分析**
- **SEGA Claw 數據分析**
- **希利創新 數據分析**
- **數據研究探討**
  - **數據上傳**：支援 CSV、Excel（.xlsx / .xls），自動解析欄位
  - **數據探索**：資料預覽、基本統計、缺失值、數值相關性熱力圖
  - **視覺化**：長條圖、折線圖、散點圖、圓餅圖、直方圖（Plotly 互動圖表）
  - **報告發布**：產生 Markdown 或 HTML 報告並下載

---

## 希利創新儀表板（首個實作目標）

以 **希利創新娃娃機 交易分析儀表板** 為第一個執行目標，目標產出與現有報表一致的互動式儀表板。

### 資料來源

- 希利創新娃娃機相關報表：CSV、Excel（.xlsx / .xls），可對接既有 `希利創新娃娃機_統計分析報表_內.xlsm` 或由其匯出之檔案。
- **每日交易報表（優先對接）**：實際檔案位於 **`./SEGA_TX/希利創新/`** 目錄下，檔名格式為 `URS-YYYY-MM-DD.csv`（例如 `URS-2026-02-13.csv`）。儀表板可支援單檔載入或依日期範圍合併多日 CSV。
- 資料可經「數據上傳」、從工作目錄選檔，或由儀表板內指定 `SEGA_TX/希利創新` 路徑載入。

#### 每日交易報表欄位對應與計算邏輯

| 儀表板維度 | 報表欄位 | 說明 |
|------------|----------|------|
| **店名** | `商店名稱` | 格式如「希利創新_7-11 愿橋」；可擷取後段作為門市簡稱（如「愿橋」）或保留全名。 |
| **交易日期** | `交易日期` | 整數 YYYYMMDD（如 `20260213`），需轉成日期型別供篩選與聚合。 |
| **支付別** | `發卡公司` | 如「現金」、「悠遊卡」、「一卡通」等；空值可視為現金。 |
| **金額** | `實際扣款金額` | 單筆交易金額，依店名／支付別／日期聚合後供圖表與資料重整表使用。 |

- **篩選規則**：排除 `是否退款` 為「是」的紀錄，僅統計有效銷售。
- **資料重整表計算**：依篩選後之日期範圍，按店名聚合「累積營收」；統計日數 = 篩選區間天數；平均日營收 = 累積營收／統計日數；預估月營收 = 平均日營收 × 30；預估年營收 = 平均日營收 × 365。營運通路數 = 有交易之店名數。

### 儀表板功能規格

| 區塊 | 內容 |
|------|------|
| **頂部篩選** | 交易日期篩選（年、月、日範圍）。 |
| **資料重整表** | 最後交易日、統計日數、營運通路數；依店名之累積營收、平均日營收、預估月營收、預估年營收；總計／平均值／平均值（營業中）。 |
| **各支付別交易金額比** | 圓餅圖：現金、悠遊卡、一卡通等支付方式金額占比。 |
| **各門市交易總金額比較** | 門市篩選（多選）；各門市交易總金額數字或長條比較。 |
| **每日交易金額** | 折線圖：希利創新娃娃機每日交易金額時間序列。 |
| **各支付別金額（時間）** | 百分比堆疊折線圖：依日期之現金／悠遊卡／一卡通占比。 |
| **單一門市細部** | 可選門市（如科有）：該門市每日交易金額折線圖、該門市各支付別金額長條圖。 |

### 與現有架構的關係

- **希利創新 數據分析**（第一層功能）：專用儀表板，固定欄位與圖表邏輯，直接讀取希利創新報表格式。
- **數據研究探討**：通用流程（上傳 → 探索 → 視覺化 → 報告），適用任意 CSV/Excel，供彈性分析與研究。

實作：`pages/希利創新_交易分析儀表板.py` 讀取 `SEGA_TX/希利創新/` 下之 `URS-*.csv`，並依上表欄位對應實作「依店名／支付別／日期」的專用版面與計算邏輯。  
**自動化**：若偵測到資料目錄（依序嘗試 `../SEGA_TX/希利創新`、`../../SEGA_TX/希利創新`）且目錄內有 `URS-*.csv`，開啟儀表板頁面時會**自動載入**資料，無需手動按鈕；仍可於側邊欄「重新從目錄載入」或改為「上傳 CSV」。

---

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
├── SEGA_TX/            # 選用：同步後推送，雲端可自動載入（見 scripts/sync_hili_urs.py）
│   └── 希利創新/
│       └── URS-*.csv
├── scripts/
│   └── sync_hili_urs.py # 將 ../SEGA_TX/希利創新/ 同步到 Web/SEGA_TX/希利創新/
└── pages/
    ├── 1_數據上傳.py
    ├── 2_數據探索.py
    ├── 3_視覺化.py
    ├── 4_報告發布.py
    └── 希利創新_交易分析儀表板.py   # 希利創新娃娃機專用儀表板（首個實作目標）
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

### 5. 希利創新儀表板在雲端顯示「未偵測到目錄」時

雲端主機**只會有 GitHub 儲存庫裡的檔案**，不會有你本機的 `SEGA_TX` 資料夾，除非一併放進 repo。

**可採做法：**

| 做法 | 說明 |
|------|------|
| **A. 把資料放進 GitHub** | 在 **Web 專案內**建立 `SEGA_TX/希利創新/`，放入 `URS-*.csv`，再 `git add`、`commit`、`push`。部署後程式會自動偵測專案內的 `SEGA_TX/希利創新`。若 repo 為 public，CSV 會公開。詳見下方「做法 A：將 SEGA_TX 加入 repo」。 |
| **B. 用環境變數指定路徑** | 在 Streamlit Cloud 專案 **Settings → General → Environment variables** 新增 `HILI_DATA_DIR`，值為雲端上實際存在且含 URS-*.csv 的目錄絕對路徑（通常需自行在雲端掛載或建檔，免費方案較少此選項）。 |
| **C. 不改 GitHub / 設定** | 雲端上直接使用儀表板左側「上傳 CSV」，手動上傳一或多個 `URS-*.csv` 即可分析。 |

**做法 A：將 SEGA_TX 加入 repo（雲端自動載入）**

- **本機**：**不用手動複製**。程式會優先讀取「上一層」的 `../SEGA_TX/希利創新`（與 Web 同層的實際資料夾），每天更新的 CSV 會直接反映在儀表板。
- **雲端**：需把 `Web/SEGA_TX/希利創新/` 推上 GitHub，部署後才會自動載入。若 CSV 每天更新，要讓雲端也有最新資料時，可執行同步腳本後再 push：
  1. 在 `Web` 專案根目錄執行：
     ```bash
     cd Web
     python3 scripts/sync_hili_urs.py
     ```
  2. 腳本會把 `../SEGA_TX/希利創新/` 的 `URS-*.csv` 複製到 `Web/SEGA_TX/希利創新/`。
  3. 再執行：
     ```bash
     git add SEGA_TX
     git commit -m "同步希利創新 URS 報表"
     git push
     ```
  4. Streamlit Cloud 重新部署後即可看到最新資料。
- 若不想在 repo 裡放資料，雲端可改為使用儀表板左側「上傳 CSV」。

## 授權

僅供學習與內部使用。
