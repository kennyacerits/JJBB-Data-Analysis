"""
環境與路徑設定 — 支援本機與 Google Colab
"""
import os
import sys

def _is_colab():
    """是否在 Google Colab 環境執行"""
    try:
        import google.colab
        return True
    except ImportError:
        pass
    return os.environ.get("COLAB_GPU") is not None or "google.colab" in sys.modules

def get_base_dir():
    """
    取得工作目錄（base directory）。
    優先順序：環境變數 > Colab 預設 > 目前工作目錄。
    """
    # 1. 明確由環境變數指定（Colab 或本機都可設定）
    env_base = os.environ.get("STREAMLIT_BASE_DIR") or os.environ.get("BASE_DIR")
    if env_base:
        path = os.path.abspath(os.path.expanduser(env_base))
        if os.path.isdir(path):
            return path
        # 若路徑不存在，嘗試建立或回退到 cwd
        try:
            os.makedirs(path, exist_ok=True)
            return path
        except OSError:
            pass
    # 2. Colab：預設用 /content（可寫入），若已掛載 Drive 可改設 BASE_DIR=/content/drive/MyDrive/...
    if _is_colab():
        for candidate in ["/content", os.getcwd()]:
            if os.path.isdir(candidate):
                return os.path.abspath(candidate)
    # 3. 本機：使用目前工作目錄（執行 streamlit run 的目錄）
    return os.path.abspath(os.getcwd())

# 模組載入時就決定，之後可透過 config 或 session_state 覆寫
BASE_DIR = get_base_dir()
IS_COLAB = _is_colab()

def path_under_base(*parts):
    """組合 BASE_DIR 與傳入的路徑片段，回傳絕對路徑"""
    return os.path.join(BASE_DIR, *parts)
