# Restoration-Guided Kuzushiji Character Recognition under Red Seal Interference

## :o: Kuzushiji Character Detection Dataset 

<p align="center">
  <img src="img/fig_detection_data.png" width="1024" title="details">
</p>

You can download our constructed dataset for **Kuzushiji Character Detection** from [here](https://1drv.ms/f/c/56c255dd1bb9ae9e/IgCkDlP7XG_rS6xpc1Kgbt_7Aaw8cbbKyWJLVW6dbljB69k).

### :one: Data Collection

The dataset is available from the [Center for Open Data in the Humanities (CODH)](https://codh.rois.ac.jp/char-shape/book/), and the raw data is held by [National Institute of Japanese Literature (NIJL)](https://www.nijl.ac.jp/db/).

| Index | NIJL Book ID | Book Title | Total Images | Annotated Images |
| :--: | :--: | :--: | :--: | :--: |
| 1 | 100241706 | 虚南留別志 | 77 | 67 |
| 2 | 100249376 | 御前菓子秘伝抄 | 112 | 104 |
| 3 | 100249416 | 餅菓子即席/手製集 | 70 | 58 |
| 4 | 100249476 | 飯百珍伝 | 54 | 46 |
| 5 | 200006663 | ぢぐち | 12 | 8 |
| 6 | 200015843 | 日本永代蔵 | 244 | 180 |
| 7 | 200017458 | 曾我物語 | 102 | 78 |
| 8 | 200020019 | 竹斎 | 162 | 146 |
| 9 | 200021086 | 伊曾保物語 | 62 | 60 |
| 10 | 200021763 | 膳部料理抄 | 100 | 94 |
| 11 | 200021802 | 料理物語 | 111 | 105 |
| 12 | 200021869 | 料理方心得之事 | 35 | 30 |
| 13 | 200022050 | 料理秘伝抄 | 30 | 24 |

### :two: Data Correction

Among the **1,000** annotated images, we found that **268** images contained incomplete annotations. 
These missing labels were manually corrected, and the corresponding image names are listed below：

<details>
<summary>100241706 (5 images)</summary>
<ul>
<li>100241706_00002_1</li>
<li>100241706_00006_1</li>
<li>100241706_00016_1</li>
<li>100241706_00033_1</li>
<li>100241706_00038_1</li>
</ul>
</details>

<details>
<summary>100249376 (10 images)</summary>
<ul>
<li>100249376_00012_1</li>
<li>100249376_00013_2</li>
<li>100249376_00026_1</li>
<li>100249376_00029_1</li>
<li>100249376_00030_2</li>
<li>100249376_00034_1</li>
<li>100249376_00034_2</li>
<li>100249376_00036_2</li>
<li>100249376_00038_2</li>
<li>100249376_00043_2</li>
</ul>
</details>

<details>
<summary>100249416 (9 images)</summary>
<ul>
<li>100249416_00002_2</li>
<li>100249416_00003_2</li>
<li>100249416_00004_1</li>
<li>100249416_00004_2</li>
<li>100249416_00006_1</li>  
<li>100249416_00014_1</li> 
<li>100249416_00014_2</li> 
<li>100249416_00017_1</li>   
<li>100249416_00018_1</li>   
</ul>
</details>

<details>
<summary>100249476 (3 images)</summary>
<ul>
<li>100249476_00016_1</li>
<li>100249476_00016_2</li>
<li>100249476_00018_1</li>
</ul>
</details>

<details>
<summary>200015843 (65 images)</summary>
<ul>
<li>200015843_00002_2</li> 
<li>200015843_00003_1</li>   
<li>200015843_00004_2</li>
<li>200015843_00011_1</li>
<li>200015843_00016_1</li>
<li>200015843_00016_2</li>
<li>200015843_00018_1</li>
<li>200015843_00019_1</li>
<li>200015843_00024_2</li>
<li>200015843_00025_1</li>  
<li>200015843_00028_2</li>
<li>200015843_00029_2</li>  
<li>200015843_00030_1</li>   
<li>200015843_00034_2</li>     
<li>200015843_00035_1</li>     
<li>200015843_00037_1</li>   
<li>200015843_00037_2</li>   
<li>200015843_00041_2</li>  
<li>200015843_00047_2</li>
<li>200015843_00048_1</li>    
<li>200015843_00049_1</li>  
<li>200015843_00049_2</li>  
<li>200015843_00051_2</li> 
<li>200015843_00054_1</li>   
<li>200015843_00055_1</li>    
<li>200015843_00056_1</li>   
<li>200015843_00058_1</li> 
<li>200015843_00058_2</li>   
<li>200015843_00060_2</li>     
<li>200015843_00062_1</li>     
<li>200015843_00062_2</li>   
<li>200015843_00063_1</li>   
<li>200015843_00063_2</li>  
<li>200015843_00069_2</li>
<li>200015843_00070_1</li>    
<li>200015843_00071_1</li>   
<li>200015843_00079_2</li>   
<li>200015843_00086_1</li>    
<li>200015843_00088_1</li>   
<li>200015843_00088_2</li>   
<li>200015843_00092_2</li> 
<li>200015843_00093_1</li> 
<li>200015843_00094_1</li>   
<li>200015843_00096_2</li>   
<li>200015843_00097_1</li>   
<li>200015843_00097_2</li>     
<li>200015843_00098_1</li>   
<li>200015843_00099_2</li>    
<li>200015843_00100_2</li>    
<li>200015843_00104_1</li>      
<li>200015843_00104_2</li>   
<li>200015843_00110_2</li>   
<li>200015843_00112_1</li>   
<li>200015843_00115_2</li> 
<li>200015843_00116_1</li>   
<li>200015843_00116_2</li>    
<li>200015843_00117_1</li>   
<li>200015843_00120_2</li> 
<li>200015843_00126_1</li> 
<li>200015843_00127_2</li>   
<li>200015843_00128_1</li>   
<li>200015843_00129_1</li>  
<li>200015843_00129_2</li>    
<li>200015843_00130_2</li>   
<li>200015843_00132_1</li>     
</ul>
</details>

<details>
<summary>200017458 (27 images)</summary>
<ul>
<li>200017458_00003_2</li>
<li>200017458_00004_1</li> 
<li>200017458_00004_2</li>   
<li>200017458_00011_2</li>   
<li>200017458_00012_2</li>     
<li>200017458_00013_1</li>       
<li>200017458_00015_2</li>      
<li>200017458_00016_1</li>    
<li>200017458_00016_2</li>    
<li>200017458_00017_1</li>    
<li>200017458_00018_2</li> 
<li>200017458_00019_2</li>   
<li>200017458_00021_2</li>   
<li>200017458_00027_2</li>     
<li>200017458_00030_1</li>     
<li>200017458_00030_2</li>   
<li>200017458_00031_1</li>   
<li>200017458_00032_2</li>   
<li>200017458_00036_2</li>   
<li>200017458_00037_1</li>    
<li>200017458_00043_1</li>  
<li>200017458_00044_2</li>   
<li>200017458_00048_2</li>   
<li>200017458_00049_1</li>   
<li>200017458_00049_2</li>   
<li>200017458_00050_1</li>  
<li>200017458_00051_2</li>    
</ul>
</details>

<details>
<summary>200020019 (48 images)</summary>
<ul>
<li>200020019_00003_1</li>
<li>200020019_00006_1</li>  
<li>200020019_00008_2</li>   
<li>200020019_00009_1</li>    
<li>200020019_00011_1</li> 
<li>200020019_00012_1</li>   
<li>200020019_00013_1</li>    
<li>200020019_00014_1</li>    
<li>200020019_00014_2</li>    
<li>200020019_00015_1</li>   
<li>200020019_00017_2</li>  
<li>200020019_00018_1</li>    
<li>200020019_00018_2</li> 
<li>200020019_00019_1</li>  
<li>200020019_00020_1</li>  
<li>200020019_00023_1</li>  
<li>200020019_00026_1</li>  
<li>200020019_00028_2</li>    
<li>200020019_00031_1</li>  
<li>200020019_00032_2</li>  
<li>200020019_00033_2</li>   
<li>200020019_00037_2</li>  
<li>200020019_00038_1</li>  
<li>200020019_00038_2</li>  
<li>200020019_00040_1</li>  
<li>200020019_00041_2</li>  
<li>200020019_00043_1</li>   
<li>200020019_00043_2</li> 
<li>200020019_00046_1</li>  
<li>200020019_00046_2</li>    
<li>200020019_00048_2</li>  
<li>200020019_00049_1</li>    
<li>200020019_00049_2</li>  
<li>200020019_00057_1</li> 
<li>200020019_00058_2</li> 
<li>200020019_00059_1</li>   
<li>200020019_00060_1</li>    
<li>200020019_00062_1</li> 
<li>200020019_00063_1</li>   
<li>200020019_00064_1</li>   
<li>200020019_00067_1</li>     
<li>200020019_00070_1</li>  
<li>200020019_00071_1</li>
<li>200020019_00071_2</li>
<li>200020019_00072_1</li>  
<li>200020019_00073_2</li>  
<li>200020019_00075_2</li>   
<li>200020019_00079_2</li>     
</ul>
</details>

<details>
<summary>200021086 (46 images)</summary>
<ul>
<li>200021086_00003_1</li>
<li>200021086_00004_1</li>  
<li>200021086_00004_2</li>  
<li>200021086_00005_1</li>   
<li>200021086_00005_2</li>  
<li>200021086_00006_1</li>   
<li>200021086_00007_2</li>    
<li>200021086_00008_2</li> 
<li>200021086_00009_1</li>   
<li>200021086_00009_2</li>  
<li>200021086_00010_1</li>    
<li>200021086_00010_2</li>   
<li>200021086_00011_1</li>     
<li>200021086_00011_2</li>     
<li>200021086_00012_1</li>    
<li>200021086_00013_1</li>  
<li>200021086_00013_2</li>  
<li>200021086_00014_1</li>   
<li>200021086_00014_2</li>  
<li>200021086_00015_1</li>  
<li>200021086_00015_2</li>  
<li>200021086_00016_1</li>    
<li>200021086_00016_2</li>  
<li>200021086_00017_1</li>
<li>200021086_00017_2</li>  
<li>200021086_00018_1</li>  
<li>200021086_00019_1</li>    
<li>200021086_00019_2</li>     
<li>200021086_00020_1</li>  
<li>200021086_00020_2</li>    
<li>200021086_00021_1</li>   
<li>200021086_00021_2</li>    
<li>200021086_00022_1</li>    
<li>200021086_00023_1</li>   
<li>200021086_00023_2</li>     
<li>200021086_00025_1</li> 
<li>200021086_00026_1</li>   
<li>200021086_00026_2</li>     
<li>200021086_00027_1</li>  
<li>200021086_00027_2</li>    
<li>200021086_00028_1</li>    
<li>200021086_00028_2</li> 
<li>200021086_00030_1</li>     
<li>200021086_00031_1</li>       
<li>200021086_00031_2</li>  
<li>200021086_00032_1</li>    
</ul>
</details>

<details>
<summary>200021763 (22 images)</summary>
<ul>
<li>200021763_00014_2</li>
<li>200021763_00017_1</li>  
<li>200021763_00019_2</li>  
<li>200021763_00020_1</li>   
<li>200021763_00020_2</li>  
<li>200021763_00021_1</li>  
<li>200021763_00022_2</li>  
<li>200021763_00023_1</li>  
<li>200021763_00023_2</li>  
<li>200021763_00026_2</li>  
<li>200021763_00030_1</li>  
<li>200021763_00032_2</li> 
<li>200021763_00035_1</li>  
<li>200021763_00035_2</li>   
<li>200021763_00036_1</li> 
<li>200021763_00036_2</li>   
<li>200021763_00038_2</li>   
<li>200021763_00039_2</li> 
<li>200021763_00040_1</li>   
<li>200021763_00041_1</li>  
<li>200021763_00043_2</li> 
<li>200021763_00047_2</li>   
</ul>
</details>

<details>
<summary>200021802 (23 images)</summary>
<ul>
<li>200021802_00005_2</li>
<li>200021802_00006_1</li>  
<li>200021802_00011_2</li>   
<li>200021802_00017_1</li>     
<li>200021802_00026_2</li> 
<li>200021802_00027_1</li>   
<li>200021802_00030_1</li>   
<li>200021802_00031_1</li>  
<li>200021802_00033_1</li>   
<li>200021802_00033_2</li> 
<li>200021802_00034_1</li>   
<li>200021802_00034_2</li>     
<li>200021802_00035_1</li>   
<li>200021802_00035_2</li>
<li>200021802_00040_2</li>  
<li>200021802_00042_1</li>  
<li>200021802_00044_1</li> 
<li>200021802_00048_2</li>
<li>200021802_00049_1</li>  
<li>200021802_00051_1</li>   
<li>200021802_00052_1</li>  
<li>200021802_00055_1</li>    
<li>200021802_00055_2</li>      
</ul>
</details>

<details>
<summary>200021869 (3 images)</summary>
<ul>
<li>200021869_00004_2</li>
<li>200021869_00008_2</li>  
<li>200021869_00014_1</li>    
</ul>
</details>

<details>
<summary>200022050 (7 images)</summary>
<ul>
<li>200022050_00005_2</li> 
<li>200022050_00009_2</li>   
<li>200022050_00010_2</li>   
<li>200022050_00011_2</li> 
<li>200022050_00012_2</li>   
<li>200022050_00013_2</li>    
<li>200022050_00020_2</li>      
</ul>
</details>

### Data Annotation (Unicode Label)

<details>
<summary>Test Set (21 images)</summary>
<ul>
<li>100249376_00034_1</li>  
<li>100249416_00017_1</li>  
<li>200015843_00003_1</li>  
<li>200015843_00049_1</li>  
<li>200015843_00062_2</li>  
<li>200015843_00069_2</li>  
<li>200015843_00079_2</li>  
<li>200015843_00130_2</li>  
<li>200020019_00012_1</li>  
<li>200020019_00020_1</li>  
<li>200020019_00028_2</li>  
<li>200020019_00057_1</li>  
<li>200020019_00064_1</li>  
<li>200021086_00005_1</li>  
<li>200021086_00016_1</li>  
<li>200021086_00018_1</li>  
<li>200021086_00019_2</li>  
<li>200021763_00020_1</li>  
<li>200021763_00043_2</li>  
<li>200021802_00026_2</li>  
<li>200022050_00010_2</li>  
</ul>
</details>

### Synthetic Data Generation

## Preprocess
```
  python preprocess.py --r_min 90 --rg_ratio 1.2 --rb_ratio 1.2
```

## Kuzushiji Character Detection
### Ultralytics YOLO
* Train
```
  yolo detect train model=yolov9m.pt data=./yolo_dataset/meta.yaml epochs=100 batch=16 imgsz=640 device=0 workers=8 optimizer=SGD lr0=0.01 name=train_yolov9m
  yolo detect train model=yolov10m.pt data=./yolo_dataset/meta.yaml epochs=100 batch=16 imgsz=640 device=0 workers=8 optimizer=SGD lr0=0.01 name=train_yolov10m
  yolo detect train model=yolo11m.pt data=./yolo_dataset/meta.yaml epochs=100 batch=16 imgsz=640 device=0 workers=8 optimizer=SGD lr0=0.01 name=train_yolo11m
  yolo detect train model=yolo12m.pt data=./yolo_dataset/meta.yaml epochs=100 batch=16 imgsz=640 device=0 workers=8 optimizer=SGD lr0=0.01 name=train_yolo12m
  yolo detect train model=rtdetr-l.pt data=./yolo_dataset/meta.yaml epochs=100 batch=8 imgsz=640 device=0 workers=8 optimizer=SGD lr0=0.01 name=train_rtdetr-l
```
* Test
```
  yolo val model='./runs/detect/train_yolov9m/weights/best.pt' data=./yolo_dataset/meta.yaml split='test' save_txt=True save_conf=True conf=0.1 name=test_yolov9m
  yolo val model='./runs/detect/train_yolov10m/weights/best.pt' data=./yolo_dataset/meta.yaml split='test' save_txt=True save_conf=True conf=0.1 name=test_yolov10m
  yolo val model='./runs/detect/train_yolo11m/weights/best.pt' data=./yolo_dataset/meta.yaml split='test' save_txt=True save_conf=True conf=0.1 name=test_yolo11m
  yolo val model='./runs/detect/train_yolo12m/weights/best.pt' data=./yolo_dataset/meta.yaml split='test' save_txt=True save_conf=True conf=0.1 name=test_yolo12m
  yolo val model='./runs/detect/train_rtdetr-l/weights/best.pt' data=./yolo_dataset/meta.yaml split='test' save_txt=True save_conf=True conf=0.1 name=test_rtdetr-l
```

# License
<img src="./img/CC-BY-SA.png" alt="CC BY-SA 4.0 License" width="100" style="vertical-align: middle;">  

This benchmark dataset is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).

### Original Kuzushiji Dataset

The original Kuzushiji dataset used in this work is based on **『日本古典籍くずし字データセット』** (National Institute of Japanese Literature / CODH), provided by [ROIS-DS Center for Open Data in the Humanities (CODH)](https://codh.rois.ac.jp/), which is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).

The following is the citation of the original Kuzushiji dataset; please cite it when using our benchmark dataset:
```
  『日本古典籍くずし字データセット』 （国文研所蔵／CODH加工） doi:10.20676/00000340
```

