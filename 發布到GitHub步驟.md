# 把專案推到 GitHub — 一步一步做

「用 Git 推到 GitHub」的意思是：**把你電腦裡的 Web 專案，上傳到 GitHub 網站，變成一個「儲存庫」（repository）**。  
Streamlit 要部署時，需要從這個儲存庫讀取你的程式。

---

## 第一步：確認電腦有 Git

1. 打開 **終端機**（Terminal）。
2. 輸入：`git --version`，按 Enter。
3. 若出現版本號（例如 `git version 2.x.x`）代表已安裝。
4. 若顯示「command not found」，請先安裝：[git-scm.com](https://git-scm.com) 下載安裝後再繼續。

---

## 第二步：在 GitHub 網站建立一個「空的」儲存庫

1. 打開瀏覽器，到 **[github.com](https://github.com)**，登入你的帳號。
2. 點右上角 **+** → **New repository**。
3. **Repository name** 自己取一個，例如：`streamlit-data-app`。
4. 選 **Public**。
5. **不要**勾選 "Add a README file"（保持空白儲存庫）。
6. 點 **Create repository**。
7. 建立好後，畫面上會有一個網址，長得像：  
   `https://github.com/你的帳號名稱/streamlit-data-app.git`  
   **先複製這個網址，等一下會用到。**

---

## 第三步：在「專案目錄」裡用 Git 上傳

「專案目錄」就是放 `app.py`、`requirements.txt` 的那個資料夾（Web）。

1. 打開終端機。
2. 用 `cd` 進入你的 Web 專案目錄，例如：
   ```bash
   cd "/Users/kennymacm4/Library/CloudStorage/GoogleDrive-kenny.acerits@gmail.com/我的雲端硬碟/Web"
   ```
   （路徑要改成你電腦裡 Web 資料夾的真實位置。）

3. 依序輸入下面每一行，每輸入一行就按 Enter：

   ```bash
   git init
   ```
   **意思**：在這個資料夾裡「開始用 Git 管理」，會多一個隱藏的 `.git` 資料夾。

   ```bash
   git add .
   ```
   **意思**：把目前資料夾裡「所有檔案」都列入等一下要上傳的內容。

   ```bash
   git commit -m "Initial"
   ```
   **意思**：把上面選好的檔案，打成一個「版本」，名稱叫 Initial。

   ```bash
   git remote add origin https://github.com/你的帳號名稱/streamlit-data-app.git
   ```
   **意思**：告訴電腦「等一下要上傳到哪一個 GitHub 網址」。  
   **注意**：要把 `你的帳號名稱` 和 `streamlit-data-app` 換成你第二步建立的 repo 名稱與帳號。

   ```bash
   git branch -M main
   ```
   **意思**：把目前分支取名為 `main`（GitHub 預設主分支名稱）。

   ```bash
   git push -u origin main
   ```
   **意思**：真的把檔案「推」上 GitHub。  
   **若被問密碼卻無法通過**：請看下一節「用權杖代替密碼」。

---

## 被問密碼卻無法執行時：用「權杖」代替密碼

GitHub **已經不接受用帳號密碼**在終端機登入，必須改用 **Personal Access Token（個人存取權杖）**。

### 一、在 GitHub 建立權杖

1. 登入 **[github.com](https://github.com)**。
2. 點右上角 **頭像** → **Settings**。
3. 左側最下面點 **Developer settings**。
4. 左側點 **Personal access tokens** → **Tokens (classic)**。
5. 點 **Generate new token** → **Generate new token (classic)**。
6. **Note** 隨便填（例如：`streamlit push`），**Expiration** 選 90 天或 No expiration。
7. 勾選 **repo**（會自動勾選底下子項目）。
8. 拉到最下面點 **Generate token**。
9. 畫面上會出現一串字（例如 `ghp_xxxxxxxxxxxx`），**只會顯示一次**，請**立刻複製**並貼到記事本暫存。

### 二、推送到 GitHub 時改用權杖

當你執行 `git push -u origin main` 時：

- **Username**：填你的 **GitHub 帳號**（不是 email）。
- **Password**：**不要填登入密碼**，改貼剛才複製的 **權杖（Token）**。

終端機不會顯示你輸入的內容，貼上權杖後直接按 Enter 即可。  
若成功，就會看到 `Writing objects: 100%` 等訊息，代表已上傳完成。

### 三、之後不想每次都輸入（選用）

可讓電腦「記住」權杖（以 macOS 為例）：

1. 打開 **鑰匙圈存取**（Keychain Access）。
2. 搜尋 `github`，找到 `github.com` 的項目。
3. 雙擊 → 把「密碼」改成你的 **權杖**，儲存。

之後再執行 `git push` 就不會再問密碼（除非權杖過期或刪除）。

---

## 完成之後

- 到 GitHub 網頁重新整理你的儲存庫，應該會看到 `app.py`、`requirements.txt`、`pages/` 等檔案。
- 接下來就可以到 **[share.streamlit.io](https://share.streamlit.io)** 用「Deploy」選這個儲存庫來發布 Streamlit。

---

## 到 Streamlit 部署時：「選 Repository、Branch」是什麼意思？

在 share.streamlit.io 點 **Deploy an app** 後，畫面上會要你選兩樣東西：

### Repository（儲存庫）

- **是什麼**：就是你在 GitHub 上的「那一個專案」、那一個 repo。
- **怎麼選**：下拉選單會列出你 GitHub 帳號底下的**所有儲存庫**（或你有權限的）。  
  選你**剛剛推上去、放 Streamlit 程式的那一個**，例如 `streamlit-data-app` 或你取的名字。
- **一句話**：**選「要部署的那個 GitHub 專案」**。

### Branch（分支）

- **是什麼**：同一個儲存庫裡，可以有多條「版本線」，每一條叫一個 branch。  
  預設通常只有一條，叫做 **main**（以前有些專案叫 **master**）。
- **怎麼選**：若你沒有自己建過其他分支，就選 **main** 即可。  
  選單裡會列出該 repo 的所有分支（例如 `main`、`develop`），選 **main** 代表「用主線上的程式來部署」。
- **一句話**：**選「要用哪一條版本線的程式」**，一般選 **main**。

### 對照表

| 欄位 | 意思 | 通常填什麼 |
|------|------|------------|
| **Repository** | 要部署的 GitHub 專案（哪一個 repo） | 你放 `app.py` 的那個 repo 名稱 |
| **Branch** | 要用該專案的哪一條版本線 | **main**（若你沒特別建其他分支） |

選好 Repository 和 Branch 後，**Main file path** 填 `app.py`，再按 **Deploy** 就會開始建置並產生公開網址。

---

## 之後修改再發布怎麼做？

程式改完後，只要**再推送到同一個 GitHub 儲存庫的同一個分支**（例如 `main`），Streamlit Cloud 會**自動重新建置並更新**，不用在 share.streamlit.io 再按一次 Deploy。

### 步驟（每次改完都做這三行）

1. 在終端機 **cd** 到你的 Web 專案目錄（和第一次一樣）。
2. 依序執行：

   ```bash
   git add .
   ```
   把「有改動的檔案」都標記起來。

   ```bash
   git commit -m "這裡寫你做了什麼改動"
   ```
   例如：`git commit -m "新增說明文字"` 或 `git commit -m "修正圖表選單"`。

   ```bash
   git push origin main
   ```
   推送到 GitHub（若之前有存過權杖，通常不會再問密碼）。

3. 到 **[share.streamlit.io](https://share.streamlit.io)** 點進你的 app，畫面上會顯示正在重新建置；完成後重新整理網址就會看到新版本。

### 一句話

**改程式 → `git add .` → `git commit -m "說明"` → `git push origin main` → 等 Streamlit 自動重建。**

---

## Deploy 之後頁面無顯示？排查步驟

若部署完成、點開網址卻**一片空白**或**一直轉圈**，依下面順序檢查。

### 1. 先看「建置／執行」有沒有錯誤（最重要）

1. 登入 **[share.streamlit.io](https://share.streamlit.io)**，點進你部署的那個 app。
2. 點上方 **Manage app** 或 **Settings**，找到 **Build logs** 與 **App logs**（或 **Logs**）。
3. **Build logs**：建置時若失敗（例如套件裝不起來），這裡會有紅色錯誤訊息。
4. **App logs**：程式啟動後若當掉（例如 `ModuleNotFoundError`、`FileNotFoundError`），這裡會印出錯誤。

若有錯誤，把訊息複製下來，對照下面常見原因修改。

---

### 2. 常見原因一：Repository 根目錄與 Main file 不符

**狀況**：你的 GitHub 儲存庫**根目錄**長這樣：

- 根目錄**直接**有 `app.py`、`config.py`、`pages/`  
  → **Main file path** 填 `app.py` 即可，**不要**設 Root directory。

- 根目錄底下**還有一層資料夾**（例如 `Web/`），`app.py` 在 `Web/` 裡面：
  ```
  你的 repo 根目錄/
  └── Web/
      ├── app.py
      ├── config.py
      ├── pages/
      └── requirements.txt
  ```
  → 必須在 Streamlit 的 **Advanced settings** 裡設：
  - **Root directory**：`Web`
  - **Main file path**：`app.py`

沒設 Root directory 時，雲端會以「repo 根目錄」當工作目錄，找不到 `config.py` 或 `pages/` 會導致錯誤或空白頁。

---

### 3. 常見原因二：免費方案冷啟動

- 免費方案一段時間沒人用，app 會**休眠**。
- 第一次點開網址可能要等 **30 秒～1 分鐘** 才會出現畫面，期間可能一直轉圈或「Please wait」。
- **做法**：多等一會或再重新整理一次。

---

### 4. 常見原因三：瀏覽器快取或擴充功能

- 試試**無痕模式**或**另一種瀏覽器**（Chrome / Safari / Edge）。
- 或清除該網址的快取後再開。

---

### 5. 快速對照

| 現象 | 先做什麼 |
|------|----------|
| 完全空白、沒錯誤訊息 | 看 App logs 是否有 Python 錯誤；檢查 Root directory 是否為 `Web`（若 app 在 Web 資料夾內）。 |
| 建置失敗 | 看 Build logs，確認 `requirements.txt` 與 Python 版本（如 `runtime.txt`）是否正確。 |
| 一直轉圈、稍等才出現 | 多半是冷啟動，等 30 秒～1 分鐘或重新整理。 |
| 本機正常、雲端空白 | 多半是「路徑／Root directory」或依賴問題，以 Build logs 與 App logs 為準。 |

排查時**以 Build logs 和 App logs 的錯誤訊息為準**，改完程式後在 GitHub 再 push 一次，Streamlit Cloud 會自動重新部署。

---

## 一句話對照

| 指令 | 一句話說明 |
|------|------------|
| `git init` | 在這個資料夾開始用 Git |
| `git add .` | 把目前所有檔案標記成「要上傳」 |
| `git commit -m "Initial"` | 把要上傳的內容打成一個版本 |
| `git remote add origin 網址` | 設定「要上傳到哪一個 GitHub 儲存庫」 |
| `git push -u origin main` | 真的上傳到 GitHub |

**整體流程**：先在 GitHub 建立「空 repo」→ 在專案目錄用上面指令把本地專案「推」上去。
