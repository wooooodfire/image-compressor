import os
from PIL import Image
from zipfile import ZipFile
# from tkinter import Tk, filedialog, messagebox, Label, Button, StringVar, Scale, HORIZONTAL, Text
from tkinter import Tk, filedialog, messagebox, HORIZONTAL, Text
import shutil
from ttkbootstrap import Window, Label, Button, Scale, IntVar, Entry, StringVar, DoubleVar
from ttkbootstrap.constants import *

# 壓縮單張圖片
def compress_image(image_path, output_folder, quality=70):
    """
    壓縮單張圖片並將其儲存在指定的輸出資料夾中。
    :param image_path: 圖片的路徑
    :param output_folder: 壓縮後圖片的輸出資料夾
    :param quality: 壓縮的品質，數值越低壓縮越多，預設為70
    """
    img = Image.open(image_path)
    img_name = os.path.basename(image_path)
    compressed_image_path = os.path.join(output_folder, img_name)
    img.save(compressed_image_path, "JPEG", quality=quality)

# 壓縮資料夾中的所有圖片
def compress_images_in_folder(input_folder, output_folder, quality=70):
    """
    壓縮指定資料夾中的所有圖片，並將它們儲存在指定的輸出資料夾中。
    :param input_folder: 包含要壓縮圖片的資料夾
    :param output_folder: 壓縮後圖片的輸出資料夾
    :param quality: 壓縮品質，預設為70
    """
    # 如果輸出資料夾不存在，則創建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍歷資料夾中的所有檔案
    for root, _, files in os.walk(input_folder):
        for file in files:
            # 過濾圖片檔案（只壓縮 .png, .jpg, .jpeg 格式）
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                compress_image(os.path.join(root, file), output_folder, quality)

# 將壓縮後的圖片打包成ZIP檔案
def zip_folder(folder_path, output_zip):
    """
    將指定資料夾中的所有內容壓縮成ZIP檔案。
    :param folder_path: 要壓縮的資料夾路徑
    :param output_zip: 輸出的ZIP檔案路徑
    """
    with ZipFile(output_zip, 'w') as zipf:
        # 遍歷資料夾中的所有檔案並加入到ZIP中
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # 將檔案加入到ZIP檔案中，並去除絕對路徑
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

# 選擇輸入資料夾（圖片所在位置）
def select_input_folder():
    """
    打開對話框讓使用者選擇包含圖片的資料夾，並將其路徑儲存到 input_folder 變數中。
    """
    folder_selected = filedialog.askdirectory(title="Select Folder Containing Images")
    input_folder.set(folder_selected)  # 更新選擇的資料夾路徑

# 選擇輸出的ZIP檔案位置
def select_output_zip():
    """
    打開對話框讓使用者選擇壓縮後ZIP檔案的儲存位置，並將其路徑儲存到 output_zip 變數中。
    """
    zip_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP files", "*.zip")])
    output_zip.set(zip_path)  # 更新選擇的ZIP檔案儲存位置

# 開始壓縮圖片並打包成ZIP檔案
def start_compression():
    """
    開始壓縮圖片的過程：首先檢查輸入資料夾和輸出ZIP檔案是否已選擇，
    然後壓縮圖片並將它們打包成ZIP檔案。
    """
    input_folder_value = input_folder.get()  # 獲取選擇的圖片資料夾
    output_zip_value = output_zip.get()  # 獲取選擇的ZIP輸出路徑
    quality_value = int(quality_var.get())  # 從輸入框獲取使用者輸入的壓縮品質

    # 檢查是否已選擇圖片資料夾
    if not input_folder_value:
        messagebox.showwarning("Warning", "No input folder selected!")
        return

    # 檢查是否已選擇ZIP檔案位置
    if not output_zip_value:
        messagebox.showwarning("Warning", "No output ZIP file selected!")
        return

    output_folder = "compressed_images"  # 暫存壓縮後圖片的資料夾
    compress_images_in_folder(input_folder_value, output_folder, quality=quality_value)  # 壓縮圖片

    zip_folder(output_folder, output_zip_value)  # 將壓縮後的圖片打包成ZIP檔案

    shutil.rmtree(output_folder)  # 刪除暫存的壓縮圖片資料夾
    messagebox.showinfo("Success", f"Images compressed with quality {quality_value} and saved to {output_zip_value}!")  # 彈出成功訊息

def validate_quality_input(value):
    """
    驗證輸入框中的壓縮品質值是否在 1 到 100 之間。
    :param value: 輸入框中的值
    :return: True if valid, False otherwise
    """
    # 檢查是否為數字且在 1-100 之間
    if value.isdigit() and 1 <= int(value) <= 100:
        return True
    elif value == "":  # 允許空值，因為用戶可能正在輸入
        return True
    else:
        return False

def create_gui():
    """
    創建圖形使用者介面（GUI），包含使用說明、選擇資料夾、輸出位置、壓縮品質滑桿和壓縮按鈕。
    """
    root = Window(themename="darkly")     # 創建主視窗
    root.title("藝中圖片壓縮工具")  # 設定視窗標題

    # 定義 StringVar 用於顯示選擇的資料夾和輸出ZIP檔案
    global input_folder, output_zip, quality_var
    input_folder = StringVar()
    output_zip = StringVar()

    # 工具使用說明
    Label(root, text="藝中圖片壓縮工具使用說明", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, padx=10, pady=10)
    
    instructions = Text(root, height=7, width=60, wrap='word')
    instructions.insert('1.0', "這個工具可以幫助你壓縮資料夾中的所有圖片，並將它們打包成一個 ZIP 檔案。\n\n"
                              "使用步驟：\n"
                              "1. 選擇圖片資料夾。\n"
                              "2. 選擇 ZIP 壓縮檔案的保存路徑，以及壓縮檔名稱。\n"
                              "3. 調整壓縮品質（1-100，數值越高品質越好）。\n"
                              "4. 點擊「開始壓縮」按鈕開始壓縮並打包成 ZIP 檔案。")
    instructions.config(state='disabled')  # 禁止編輯
    instructions.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    # 圖片資料夾選擇
    Label(root, text="選擇圖片資料夾:").grid(row=2, column=0, padx=10, pady=10)  # 標籤
    Button(root, text="瀏覽", command=select_input_folder).grid(row=2, column=2, padx=10)  # 瀏覽按鈕
    Label(root, textvariable=input_folder, relief="sunken", width=50).grid(row=2, column=1, padx=10)  # 顯示選擇的資料夾

    # ZIP檔案輸出選擇
    Label(root, text="選擇壓縮檔案的保存路徑:").grid(row=3, column=0, padx=10, pady=10)  # 標籤
    Button(root, text="瀏覽", command=select_output_zip).grid(row=3, column=2, padx=10)  # 瀏覽按鈕
    Label(root, textvariable=output_zip, relief="sunken", width=50).grid(row=3, column=1, padx=10)  # 顯示選擇的ZIP檔案位置

    # 壓縮品質
    Label(root, text="選擇壓縮品質(1-100):").grid(row=4, column=0, padx=10, pady=10)  # 標籤 
    quality_var = StringVar()  # 創建一個字串變數來綁定輸入框
    vcmd = (root.register(validate_quality_input), '%P')  # 添加驗證函數來檢查輸入是否為1到100之間的數字
    quality_entry = Entry(root, textvariable=quality_var, validate='key', validatecommand=vcmd)   # 創建輸入框，並設置驗證機制
    quality_entry.grid(row=4, column=1, padx=10)
    quality_var.set('70')   # 預設壓縮品質設為70


    # 開始壓縮按鈕
    Button(root, text="開始壓縮", command=start_compression).grid(row=5, column=1, pady=20)  # 壓縮按鈕

    root.mainloop()  # 啟動GUI主迴圈

# 主函數
if __name__ == "__main__":
    create_gui()  # 呼叫創建GUI的函數
