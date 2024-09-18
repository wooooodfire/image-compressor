# image-compressor

這個工具可以幫助你壓縮資料夾中的所有圖片，並將它們打包成一個 ZIP 檔案，方便將所有相片直接上傳至學校 Rpage 官網（NDHU Arts Center），省去繁瑣的步驟，以便節省雲端空間。

## 使用步驟
1. 選擇圖片資料夾。
2. 選擇 ZIP 壓縮檔案的保存路徑，以及壓縮檔名稱。
3. 調整壓縮品質（1-100，數值越高品質越好）。
4. 點擊「開始壓縮」按鈕開始壓縮並打包成 ZIP 檔案。

## 1. 安裝必要的套件

首先需要安裝以下 Python 套件：

- `Pillow`：用來壓縮圖片。
- `zipfile`：用來將圖片壓縮成 ZIP 檔。
- `tkinter`：用來製作簡單的圖形介面，讓使用者能上傳資料夾和下載壓縮檔案。
- `PyInstaller`：用來將 Python 腳本打包成 Windows 的可執行檔（.exe）。

請執行以下命令來安裝這些套件：

```bash
pip install pillow pyinstaller
```

## 2. 執行

請使用以下命令執行程式：

```bash
python image_comporessor.py
```

## 3. 打包成 Windows 的可執行檔 (.exe) (optional)

要將這個 Python 程式轉換為 .exe 檔案，你可以使用 `PyInstaller`。

### 打包程式的步驟：

1. 先確保你的 Python 檔案（`image_compressor.py`）已經準備好。
2. 使用以下命令來打包程式：

```bash
pyinstaller --onefile --noconsole image_compressor.py
```

這條命令會生成一個不顯示終端機（`--noconsole`）的可執行檔案，並且將所有需要的依賴包打包進一個檔案中（`--onefile`）。

打包完成後，`dist` 資料夾中會生成一個 `image_compressor.exe` 檔案。你可以將這個檔案傳送給其他 Windows 用戶，他們可以直接執行這個檔案來壓縮圖片。
