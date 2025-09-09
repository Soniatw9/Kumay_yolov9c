# **🐻 YOLOv9c 台灣黑熊物件偵測模型**
本專案使用YOLOv9c最新架構，結合Optuna超參數調優，專為台灣黑熊在野外環境中的影像辨識、保育與預警而設計。
研究歷程完整紀錄於效能分析報告並集結多輪訓練經驗，透過資料精選、典型負樣本加入與多種資料增強，使模型泛化能力、精準率與實用性大幅提升。
🔽 Yoolov9c模型檔案太大，最終版本放在Huggingface 🔽
https://huggingface.co/sonia2025/3kumay-yolov9c-lastpt/tree/main

# **專案特色**
- 先進架構：採用 YOLOv9c，較 YOLOv8s 更適應小目標、遮蔽物偵測與真實場域多變環境。
- 超參數優化：訓練參數依據 Optuna 尋找最佳解並結合前人經驗微調，追求更高精熟度。
- 重視泛化實力：加入多類背景負樣本與多樣場景，兼顧 Recall 與 Precision 實戰應用表現。
- 完整記錄分析：訓練過程、指標曲線與調參心得皆收錄於專案文件及效能報告中。

# **數據集簡介**
- 來源：台灣野生動物保育協會、新聞影音、野外拍攝圖、網路公開資料
- 內容：主題以台灣黑熊為主，正樣本涵蓋原生棲地影像，負樣本增添相似動物（如猴、山羌）及不同場景動物
- 標註規範：大量人工多輪質檢、框選規格統一，確保訓練資料品質
- 規模：最終訓練集超過 20,000 張圖片

# **重要訓練超參數與優化策略**
- 核心訓練指令（可參考訓練 notebook 或 Ultralytics 命令格式）：
yolo task=detect mode=train model=yolov9c.pt data=blackbear_aug.yaml \
epochs=300 patience=40 time=10 imgsz=640 batch=32 device=0,1 workers=16 \
optimizer=AdamW lr0=0.00038 lrf=0.08 cos_lr=True weight_decay=0.0006 momentum=0.937 \
warmup_epochs=5 warmup_momentum=0.8 warmup_bias_lr=0.1 \
single_cls=True pretrained=True deterministic=True \
degrees=5 translate=0.3 scale=0.24 fliplr=0.25 flipud=0.0 \
mosaic=0.125 mixup=0.08 close_mosaic=50 auto_augment=randaugment erasing=0.4 \
box=0.05 cls=1.2 dfl=1.5 name=kumay_v9c_optuna project=5Kumay_yolov9c
- 優化器 AdamW：使收斂更穩定，較 SGD 表現優
- 低學習率 lr0=0.00038：結合餘弦退火，避免震盪與過快收斂
- 資料增強：mosaic、mixup、RandAugment、Cutout 增強多樣性且避免過度擬合
- 損失權重調整：box=0.05（抑定位誤差）、cls=1.2（提高目標判別）、dfl=1.5
- 正/負樣本調和：訓練集加入多場景負樣本，有效降低誤報

# **模型效能指標**
| 指標            | 第一次訓練 | 第二次訓練 | 第三次訓練 | 第四次訓練 |
| --------------- | ---------- | ---------- | ---------- | ---------- |
| mAP@0.5         | 0.9692     | 0.9800     | 0.9549     | 0.9532     |
| mAP@0.5:0.95    | 0.7918     | 0.8062     | 0.7763     | 0.7638     |
| Precision       | 0.9723     | 0.9732     | 0.9596     | 0.9255     |
| Recall          | 0.9505     | 0.9362     | 0.9211     | 0.9116     |
- mAP、Precision、Recall：多次訓練均維持高水準，加入負樣本後誤報率明顯降低、泛化能力明顯提升。
- F1 Score：O.6532（第四次驗證），顯著超過過往版本

# **部署建議**
- Kaggle 雙 GPU，batch 設 32 符合 VRAM 限制，workers 設為 16 加速資料分派
- 可串接 Wandb 監控訓練曲線與早停收斂
- 部署到 HuggingFace、Github、Render 形成可擴充前後端架構
- 支援前端 Flask、HTML、Firebase 等多平台部署方式

# **貢獻與參考資料**
- YOLO官方文件、Ultralytics社群
- Optuna最佳化調參經驗分享
- 台灣野生動物保育協會、研究者團隊自蒐資料
- 完整訓練日誌與手稿心得收錄於專案資料夾

# **本專案歡迎有興趣投身野生動物AI應用領域的夥伴參與與討論！**
Made with ❤️ for Taiwan's Black Bear Conservation.
