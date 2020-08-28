新規ファイルは
mAP/
original_code/
original_detect.py
command.md



`./original_code/image_move.py`   
../annotation_data内の画像を　../billboard/images/　にコピーする    
**新しいデータが入ってきたときだけでいい**



`./original_code/save_image_path.py`   
../annotation_data内のアノテーション範囲を../billboard/model_data/に記録する  
**LabelListの変更を忘れずに**  
**新しいデータが入ってきたときだけでいい**



`./original_code/make_darknet_format_file.py`  
yolov3用のlabelファイルの作成
../../billboard/model_data/　内のテキストファイルから　../../billboard/labels/{one, all}/　以下にLabelListに沿ったフォーマットで記録  
**LabelListの変更を忘れずに**  



====== ここまでは各モデル一緒にできる ======  


`./original_code/make_dataset.py`  
最初に
../../billboard/images/　ないの画像ファイルを../../billboard/images/{train, val, test}　に分配する  
../../billboard/labels/　ないのテキストファイルを../../billboard/labels/{train, val, test}　に分配する
**LabelListの変更を忘れずに**  
**過去のモデルの再現時には実行しない**  



`./train.py`  
学習を行う。コマンドは↓  

python -m torch.distributed.launch --nproc_per_node 4 train.py --img 640 --batch 64 --epochs 150 --data ./data/billboard_all.yaml --cfg ./models/billboard_all_5l.yaml --weights 'weights/yolov5l.pt'
python -m torch.distributed.launch --nproc_per_node 4 train.py --img 640 --batch 64 --epochs 150 --data ./data/billboard_one.yaml --cfg ./models/billboard_one_5l.yaml --weights 'weights/yolov5l.pt'



`./original_detect.py`  
./mAP/input/***/detection-resultsに結果を保存する  
**LabelListの変更を忘れずに**  
学習モデルを使ってtestを行う。コマンドは↓  
python original_detect.py --source ../billboard/images/test --weights weights/all_best.pt --device 0,1,2,3 --save-txt --augment



`./mAP/make_ground_truth.py`  
test評価用のground-truthファイルの作成
./mAP/input/***/ground-truth 以下に記録
**billboard/model_data/*.txtを参考にするのでフォルダの中身に注意**  
**LabelListの変更を忘れずに**  



`./mAP/main.py`  
testデータの検出結果とground_truthからmAPを算出する  
**LabelListの変更を忘れずに**  
