#!/usr/bin/env python3
"""
將 ../SEGA_TX/希利創新/ 的 URS-*.csv 同步到 Web/SEGA_TX/希利創新/
供推送至 GitHub 後，雲端儀表板可載入最新報表。
在 Web 專案根目錄執行：python3 scripts/sync_hili_urs.py
"""
import os
import shutil
import glob

WEB_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(WEB_ROOT, "..", "SEGA_TX", "希利創新")
TARGET = os.path.join(WEB_ROOT, "SEGA_TX", "希利創新")

def main():
    if not os.path.isdir(SOURCE):
        print(f"來源目錄不存在：{SOURCE}")
        return 1
    os.makedirs(TARGET, exist_ok=True)
    pattern = os.path.join(SOURCE, "URS-*.csv")
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"來源目錄內沒有 URS-*.csv：{SOURCE}")
        return 1
    for path in files:
        name = os.path.basename(path)
        dest = os.path.join(TARGET, name)
        shutil.copy2(path, dest)
        print(f"  已同步 {name}")
    print(f"共同步 {len(files)} 個檔案 → {TARGET}")
    print("請執行：git add SEGA_TX && git commit -m '同步希利創新 URS 報表' && git push")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
