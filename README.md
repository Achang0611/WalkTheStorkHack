# WalkTheStorkHack
## 介紹
Walk The Stork 是一款考驗玩家平衡感的遊戲，玩家需要使用左、右箭頭按鍵控制遊戲角色保持平衡，避免跌倒。

本專案 是 Walk The Stork 的輔助程式，使用 Python 編寫，透過 OpenCV 的物件追蹤功能，實現以下功能：
 - 自動偵測遊戲角色在畫面中的位置
 - 計算遊戲角色的平衡狀態
 - 提供遊戲角色的平衡控制

## 需求
本專案使用[Python 3.11.7](https://www.python.org/downloads/release/python-3117/)，未測試其他版本的Python，如果無法使用本專案，請確認使用的版本正確。

## 入門
### 取得專案
請先克隆本專案並移動到專案資料夾：
```
git clone https://github.com/Achang0611/WalkTheStorkHack
cd WalkTheStorkHack
```
### 安裝依賴
執行本專案前，請先安裝依賴套件，使用以下指令安裝所有依賴套件：
```
pip install -r requirements.txt
```
### 執行專案
安裝好依賴後，執行程式
```
python start.py
```

### 使用程式
 - 執行程式後，會打開一個視窗，該視窗是全螢幕的截圖，透過滑鼠左鍵拖曳，選擇遊戲視窗的區域，
 - 拖曳完成後使用確認鍵(Enter)或空白鍵(Space)確認遊戲視窗的區域。
 - 第二個視窗請選擇鴨子的頭部，讓程式可以偵測鴨子頭部並追蹤，
 - 經過程式計算，會自動控制左右按鍵，達到平衡功能。
 - 按下'q'鍵退出程式。

## 科技
OpenCV - 物件追蹤
Mss - 畫面擷取
PyDirectInput - 按鍵模擬
Pillow (PIL) - 圖片轉換
