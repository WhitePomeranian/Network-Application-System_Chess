## 期末專題
### 系統功能

#### Server 模組
1. 管理成員的註冊、登入、離開、…等作業。
2. Server端程式負責組合參與的成員（Server能讓登入的成員了解目前還缺多少人才能進行）。
3. 負責初始化應用的作業，將棋子放定位。
5. 控制參與成員的動作，於回合制的遊戲中讓成員了解是否該進行動作。
6. 轉送其他參與者的動作。
7. 維護各組運行中的資訊，如有幾組遊戲正在進行中，每組的成員及目前的狀態。
8. 偵測並處理 Client 不正常離線的情況。

#### Client 模組
1. Client 端以圖形化介面來呈現。
2. 成員的註冊、登入、離開…等介面。
3. 從 Server 端接收其他 Client 的動作並顯示。
4. 讀取參與者進行的動作，確認進行的合法性後，傳送給 Server 端。
5. 偵測並處理與 Server 連線不正常中斷的情形。

### 如何使用
<b>1st: 請先安裝PyCharm Community(https://www.jetbrains.com/pycharm/download/?section=windows):</b>
<div align=left><img width="500" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/5f164087-f293-4106-83e6-3f5a3bd5a593">
<br><br>
<b>2nd: 下載project後，將其解壓縮並使用PyCharm Community開啟專案:</b>
<div align=left><img width="500" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/a336e090-c00f-4dff-a690-e6e4d26f7693">
<br><br>
<b>3rd: 開啟"Server.py"和"Client.py":</b>
<div align=left><img width="500" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/f13e0ada-26cc-4b87-b081-adb982a40349">
<br><br>
<b>4th: 啟動伺服器，執行"Server.py"</b>
<div align=left><img width="500" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/20acc15b-01c1-400f-9212-a46d34c56207">
<br><br>
<b>5th: 開啟兩個terminal視窗，待會各自作為用戶登入伺服器</b>
<div align=left><img width="500" src="https://github.com/WhitePomeranian/3-tier_course-registration-system/assets/125969536/36590be6-714b-4457-b5f1-6d9d135b8262">
<br><br>
<b>6th: 輸入"py Client.py"，執行用戶端程式</b>
<div align=left><img width="500" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/39a63f18-4d0e-486f-940f-ca459324b5e1">
<br><br>
<b>7th: 註冊兩個使用者帳號</b>
<div align=left><img width="500" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/e6f0bae5-f48e-47f0-a2b4-87a37513f294">
<br><br>
<b>8th: 各自登入以進入遊戲大廳</b>
<div align=left><img width="500" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/522977fd-f51c-45e6-b8fc-c42d847f9b9a">
<br><br>
<b>8th: 玩家A建立遊戲房間，自訂規則。(思考時間代表對弈可使用的思考時間，耗盡判負；獎勵時間代表每走一步棋可增加的思考時間)</b>
<div align=left><img width="500" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/f1afe38d-932d-4614-872f-aee638d04384">
<br><br>
<b>9th: 此時玩家A會進入房間等待對手加入，而玩家B會在大廳看到玩家A所建立的房間</b>
<div align=left><img width="600" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/e144f009-8b05-4d4a-9ecc-c59ec680dea6">
<br><br>
<img width="600" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/d973042b-c8cd-4f9f-b5e2-c3d56fbddb83"  style="float:left;">
<br><br>
<b>10th: 玩家B點擊"等待"加入玩家A所建立的房間，此時其他使用者在大廳上會看到該房間已有其他玩家</b>
<div align=left><img width="600" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/b0507d45-8d6d-4299-9a4a-fd9fd2f37444">
<br><br>
<img width="600" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/4ff872a9-14b7-47cb-a155-7a6f41cf9fde" style="float:left;">
<br><br>
<b>11th: 玩家A需等待玩家B準備完成後才能開始。玩家B準備完成就點擊"準備"；玩家A則點擊開始遊戲</b>
<div align=left><img width="600" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/05b028f5-a40b-401f-96fa-528eace631e8">
<br><br>
<div align=left><img width="600" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/52903363-d511-4971-8fef-47c4837fad3c">
<br><br>
<b>12th: 對弈開始，玩家B是白色；玩家A是黑色。由白棋先走，玩家B的思考時間開始流逝，待白方出子完成，再輪到黑方，不斷循還直到分出勝負</b>
<div align=left><img width="600" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/2bb5d68c-5f31-4cbc-a2a7-be74e1b0fd50">
<br><br>
<div align=left><img width="600" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/b8b3a168-e842-40d2-9edc-19f8a2144d22">
<br><br>
<b>13th: 國王被將軍時出現警示，被吃掉的子顯示在右邊</b>
<div align=left><img width="600" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/21429035-c83e-4509-ae23-7964c4a4b3ed">
<br><br>
<div align=left><img width="600" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/1f3bfc13-9f49-4293-ac0f-ea6769f3476b">
<br><br>
<b>14th: 國王被吃，黑方勝，遊戲結束，按Enter鍵可返回遊戲大廳</b>
<div align=left><img width="600" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/ebc394e3-c2e7-46e9-a479-2634d86d86c1">
<br><br>
<br><br>
<b>註: 1. 本遊戲與現實西洋棋規則不同，待未來開發技術更成熟時補強，差異如下:<br>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. 缺少"國王入堡"、"吃過路兵"和"升變"三個特殊規則<br>
         &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii. 缺少完善的判定和棋機制<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;iii. 國王被將死時便判負，但本遊戲是國王被吃才判負<br>
         &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;iv. 可行棋致使自己的國王被攻擊，也可以不應將，這在現實西洋棋中是不允許的<br>
  <br>
  <br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp2. 伺服器可同時支援多組玩家進行對弈:
  <div align=left><img width="600" src="https://github.com/WhitePomeranian/Network-Application-System_Chess/assets/125969536/1b4e4119-4563-4444-8c51-17aae0e4d706">

<b>


