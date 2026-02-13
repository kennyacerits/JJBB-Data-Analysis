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
   這時可能會要你登入 GitHub（或輸入 Personal Access Token），照畫面指示完成即可。

---

## 完成之後

- 到 GitHub 網頁重新整理你的儲存庫，應該會看到 `app.py`、`requirements.txt`、`pages/` 等檔案。
- 接下來就可以到 **[share.streamlit.io](https://share.streamlit.io)** 用「Deploy」選這個儲存庫來發布 Streamlit。

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
