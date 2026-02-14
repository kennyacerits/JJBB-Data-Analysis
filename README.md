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

- **主要資料來源（設計目標）**：**`../數據分析/BI_希利創新/output/希利創新娃娃機_每日交易明細.csv`**（或 `../數據分析/希利創新/output/` 同檔名）
  - 此檔案為**已彙總**之每日交易明細，內容已統計**各門市、各支付別之筆數與金額**，儀表板僅需讀取單一 CSV 並依日期／門市／支付別呈現圖表與資料重整表，**無需再從原始逐筆交易檔匯入與重算**，可大幅降低匯入與運算資源。
- 路徑說明：以 `Web` 專案目錄為基準，程式會依序嘗試 `../數據分析/BI_希利創新/output/`、`../數據分析/希利創新/output/`、專案內對應路徑；亦可設環境變數 `HILI_DATA_FILE` 指定彙總檔絕對路徑。
- 資料亦可經「數據上傳」或由儀表板指定路徑／上傳同格式 CSV 載入。

#### 每日交易明細欄位與計算邏輯

- 彙總檔欄位（程式對應）：`交易日期` → 日期、`商店通稱` → 店名、`支付工具` → 支付別、`金額` → 金額（選用：`筆數`）。儀表板依日期、門市、支付別聚合或篩選即可。
- **資料重整表計算**：依篩選後之日期範圍，按店名加總金額得「累積營收」；統計日數 = 篩選區間天數；平均日營收 = 累積營收／統計日數；預估月營收 = 平均日營收 × 30；預估年營收 = 平均日營收 × 365。營運通路數 = 有交易之門市數。

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

實作：`pages/希利創新_交易分析儀表板.py` 讀取 **`../數據分析/希利創新/output/希利創新娃娃機_每日交易明細.csv`**（已彙總各門市各支付別筆數與金額），依欄位對應實作「依店名／支付別／日期」的專用版面與計算邏輯；單一檔案即可支應儀表板，降低匯入與運算負擔。  
**自動化**：若偵測到上述路徑或專案內對應路徑存在該 CSV，開啟儀表板頁面時可**自動載入**；仍可於側邊欄「重新載入」或改為「上傳 CSV」。

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
├── 數據分析/           # 選用：本機與 Web 同層時，儀表板讀取 ../數據分析/希利創新/output/希利創新娃娃機_每日交易明細.csv
│   └── 希利創新/
│       └── output/
│           └── 希利創新娃娃機_每日交易明細.csv
├── scripts/
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

### 部署前檢查（一直未部署上去時請依序確認）

1. **程式已推送到 GitHub**  
   本機改動不會自動同步到雲端，必須 push 才會更新部署。
   ```bash
   cd Web
   git status          # 若有 "Your branch is ahead of 'origin/main'" 表示尚未 push
   git add .
   git commit -m "更新希利創新儀表板與說明"
   git push origin main
   ```
2. **Streamlit Cloud 設定**  
   開啟 [share.streamlit.io](https://share.streamlit.io) → 你的 app → **Settings**：
   - **Repository**：選 `kennyacerits/JJBB-Data-Analysis`（或你的 repo）
   - **Branch**：`main`
   - **Main file path**：`app.py`
   - **Root directory**：若 repo 根目錄就是 Web 專案（裡面直接有 app.py、pages/），留空；若 repo 裡有 `Web` 資料夾、app 在 `Web/app.py`，填 `Web`。
3. **觸發重新部署**  
   Push 後若未自動重建，到該 app 頁面點 **Reboot app** 或 **Redeploy**。

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

### 5. 希利創新儀表板在雲端顯示「未偵測到」時

儀表板設計為讀取 **`../數據分析/希利創新/output/希利創新娃娃機_每日交易明細.csv`**（單一彙總檔）。雲端主機僅有 GitHub 儲存庫內檔案，不會有本機的 `數據分析` 目錄。

**可採做法：**

| 做法 | 說明 |
|------|------|
| **A. 把彙總檔放進 GitHub** | 在 Web 專案內建立對應路徑（例如 `數據分析/希利創新/output/`），放入 `希利創新娃娃機_每日交易明細.csv`，再 `git add`、`commit`、`push`。部署後程式可偵測專案內該檔。若 repo 為 public，CSV 會公開。 |
| **B. 環境變數指定路徑** | 在 Streamlit Cloud **Settings → General → Environment variables** 新增 `HILI_DATA_FILE` 或 `HILI_DATA_DIR`，指向雲端上該 CSV 的絕對路徑或所在目錄（需自行於雲端提供檔案）。 |
| **C. 上傳 CSV** | 雲端直接使用儀表板左側「上傳 CSV」，手動上傳 `希利創新娃娃機_每日交易明細.csv`（或同格式彙總檔）即可分析。 |

- **本機**：若 `Web` 與 `數據分析` 在同一層（例如都在「我的雲端硬碟」下），程式會讀取 `../數據分析/希利創新/output/希利創新娃娃機_每日交易明細.csv`，無需複製。每日更新該彙總檔後重新整理儀表板即可。
- 若不想在 repo 裡放資料，雲端改為使用「上傳 CSV」即可。

## 授權

僅供學習與內部使用。
