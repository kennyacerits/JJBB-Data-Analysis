# 交接清單（HANDSHAKE）

> 用途：在不同機器間「手動同步」時，快速了解進度與待辦。
> 使用時機：每次開始/結束一段修改都更新一次。
> 本專案 Cursor 規則位於 `.cursor/rules/workflow-confirm-first.mdc`，隨專案同步即可在另一台設備生效。

---

日期：YYYY-MM-DD  
目前版本：YYYY-MM-DD-V#  
本次目標：  
已完成：  
未完成 / 下一步：  
注意事項 / 風險：  
相關檔案：  

---

## 最近一次交接

日期：2026-03-25  
目前版本：2026-03-25-V2  
本次目標：釐清 runOnSave 與資料檔更新；希利儀表板依 CSV mtime 自動重載  
已完成：`pages/希利創新_交易分析儀表板.py` 以 `st.fragment(run_every=…)` 輪詢彙總檔 mtime，變更時清空 `hili_raw_df` 並 `st.rerun()`；`HILI_CSV_POLL_SEC`（預設 30，0＝停用）；`requirements.txt` 的 `streamlit>=1.50.0`（支援 fragment 定時 rerun）  
未完成 / 下一步：若需更即時可縮短輪詢間隔；遠端部署若不想背景輪詢可設 `HILI_CSV_POLL_SEC=0`  
注意事項 / 風險：`server.runOnSave` 仍僅對應用程式碼存檔，與 CSV 更新無關；僅在側邊欄選「使用已載入資料」時啟用 mtime 輪詢，避免覆寫「上傳 CSV」模式  
相關檔案：`pages/希利創新_交易分析儀表板.py`、`requirements.txt`、`.streamlit/config.toml`  

（把最新的一次寫在這裡）
