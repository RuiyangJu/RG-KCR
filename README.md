# RG-KCR
Restoration-Guided Kuzushiji Character Recognition Framework under Seal Interference
>[arXiv](https://arxiv.org/)
>[Project](https://ruiyangju.github.io/RG-KCR/)

# Motivation
* Existing Kuzushiji character recognition systems, including [Fuminoha](https://camera.fuminoha.jp/), [NDLkotenOCR-Lite](https://ndlkotenocr-lite-web.netlify.app/), and [Metom](https://huggingface.co/SakanaAI/Metom), fail to deliver satisfactory performance when recognizing Kuzushiji characters with overlapping seals.
  <p align="center">
    <img src="img/fig_intro.png" width="1024" title="details">
  </p>

# Pipeline
* The proposed framework consists of three main stages: Kuzushiji Character Detection, Kuzushiji Document Restoration, and Kuzushiji Character Classification. The overall pipeline is shown below:
  <p align="center">
    <img src="img/fig_pipeline.png" width="1024" title="details">
  </p>

# Citation
* If you find our paper useful in your research, please consider citing:
  ```
    
  ```

# Dataset
## :one: Kuzushiji Character Detection Dataset 
### Data Collection
* The original dataset is available from the [Center for Open Data in the Humanities (CODH)](https://codh.rois.ac.jp/char-shape/book/), and the raw data is held by [National Institute of Japanese Literature (NIJL)](https://www.nijl.ac.jp/db/).

  | Index | NIJL Bibliographic ID | Book Title | Total Images | Annotated Images |
  | :--: | :--: | :--: | :--: | :--: |
  | 1 | 100241706 | Usonarubeshi (虚南留別志) | 77 | 67 |
  | 2 | 100249376 | Gozenkashi Hiden-shou (御前菓子秘伝抄) | 112 | 104 |
  | 3 | 100249416 | Mochigashi Sokuseki Teseishuu (餅菓子即席手製集) | 70 | 58 |
  | 4 | 100249476 | Meshi Hyakuchin Den (飯百珍伝) | 54 | 46 |
  | 5 | 200006663 | Diguchi (ぢぐち) | 12 | 8 |
  | 6 | 200015843 | Nippon Eitaigura (日本永代蔵) | 244 | 180 |
  | 7 | 200017458 | Soga Monogatari (曾我物語) | 102 | 78 |
  | 8 | 200020019 | Chikusai (竹斎) | 162 | 146 |
  | 9 | 200021086 | Isoho Monogatari (伊曾保物語) | 62 | 60 |
  | 10 | 200021763 | Zenbu Ryouri-shou (膳部料理抄) | 100 | 94 |
  | 11 | 200021802 | Ryouri Monogatari (料理物語) | 111 | 105 |
  | 12 | 200021869 | Ryourikata Kokoroenokoto (料理方心得之事) | 35 | 30 |
  | 13 | 200022050 | Ryouri Hiden-shou (料理秘伝抄) | 30 | 24 |

### Data Correction
* Among the **1,000** annotated images, we found that **267** images contained incomplete annotations.
* As shown below, the red bounding boxes are annotated by us, while the green bounding boxes are from the original annotations:
  <p align="center">
    <img src="img/fig_correction.png" width="1024" title="details">
  </p>
* These missing labels were manually corrected, and the corresponding image names are listed below：

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
  <summary>200022050 (6 images)</summary>
  <ul>
  <li>200022050_00005_2</li> 
  <li>200022050_00009_2</li>   
  <li>200022050_00010_2</li>   
  <li>200022050_00011_2</li> 
  <li>200022050_00012_2</li>   
  <li>200022050_00013_2</li>        
  </ul>
  </details>

### Synthetic Data Generation
* Based on the 1,000 corrected images, we synthesized data using 128 high-quality red seal images.
* Real documents with seals versus synthetic documents with seals:
  <p align="center">
    <img src="img/fig_synthetic.png" width="1024" title="details">
  </p>
  
* The resulting dataset was randomly split into training, validation, and test sets with a ratio of 8:1:1, consisting of 800 training images, 100 validation images, and 100 test images.
* Our constructed dataset for **Kuzushiji character detection** can be downloaded from [here](https://1drv.ms/f/c/56c255dd1bb9ae9e/IgCkDlP7XG_rS6xpc1Kgbt_7Aaw8cbbKyWJLVW6dbljB69k).

## :two: Kuzushiji Character Classification 
* Details of the dataset are summarized as follows：

  | Test set #Images | Total GT Bounding Boxes | Total Pred Bounding Boxes | Total Matched Pairs (IoU>=0.5) |
  | :--: | :--: | :--: | :--: |
  | 100 | 19,035 | 18,656 | 17,982 |

* The ground-truth data for the test set can be accessed at the following [link](https://1drv.ms/f/c/56c255dd1bb9ae9e/IgDDpS626Jn_RqpJcP7bLY2OAR9Eascelseepquchb3bOXk?e=TdsKac).

# Experiments
## Environment
  ```
    conda create -n Kuzushiji python=3.10
    pip install -r requirements.txt
  ```

## :one: Kuzushiji Character Detection
* The evaluation results on the test set are presented as follows:

  | Method | Params | FLOPs | Precision | Recall | AP<sub>50</sub> | AP<sub>50:95</sub> |
  | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
  | RT-DETR (CVPR'24) | 31.99M | 103.4G | 86.2% | 79.2% | 84.1% | 57.0% |
  | YOLOv9 (ECCV'24) | 20.01M | 76.5G | 97.7% | 93.0% | 96.6% | 80.9% |
  | YOLOv10 (NeurIPS'24) | 15.31M | 58.9G | 97.7% | 92.3% | 96.5% | 80.5% |
  | YOLO11 (Ultralytics'24) | 20.03M | 67.6G | 98.1% | 93.3% | 96.7% | 81.7% |
  | YOLOv12 (NeurIPS'25) | 20.11M | 67.1G | 98.0% | 93.9% | 97.0% | 82.3% |

* Visual examples of the detection results generated by YOLOv12-medium:
  <p align="center">
    <img src="img/fig_yolo12.png" width="1024" title="details">
  </p>

### Train:
* Please download the `Kuzushiji_Character_Detection_Dataset` and place it in this directory.
* Please revise the `/path/to/data` in `./Kuzushiji_Character_Detection_Dataset/meta.yaml`.
  ```
    yolo detect train model=yolov9m.pt data=./Kuzushiji_Character_Detection_Dataset/meta.yaml epochs=100 batch=16 imgsz=640 device=0 workers=8 optimizer=SGD lr0=0.01 name=train_yolov9m
    yolo detect train model=yolov10m.pt data=./Kuzushiji_Character_Detection_Dataset/meta.yaml epochs=100 batch=16 imgsz=640 device=0 workers=8 optimizer=SGD lr0=0.01 name=train_yolov10m
    yolo detect train model=yolo11m.pt data=./Kuzushiji_Character_Detection_Dataset/meta.yaml epochs=100 batch=16 imgsz=640 device=0 workers=8 optimizer=SGD lr0=0.01 name=train_yolo11m
    yolo detect train model=yolo12m.pt data=./Kuzushiji_Character_Detection_Dataset/meta.yaml epochs=100 batch=16 imgsz=640 device=0 workers=8 optimizer=SGD lr0=0.01 name=train_yolo12m
    yolo detect train model=rtdetr-l.pt data=./Kuzushiji_Character_Detection_Dataset/meta.yaml epochs=100 batch=8 imgsz=640 device=0 workers=8 optimizer=SGD lr0=0.01 name=train_rtdetr-l
  ```

### Test:
* You can download our pretrained models [here](https://1drv.ms/f/c/56c255dd1bb9ae9e/IgBw5aIxd2jAS5oB9VxuHdWkAfPXzCM62l_L0YrVi5YG5l0).
* Please place the folder `Pretrained_Model_Kuzushiji_Detection` in `./`.
  ```
    yolo val model='./Pretrained_Model_Kuzushiji_Detection/yolov9m.pt' data=./Kuzushiji_Character_Detection_Dataset/meta.yaml split='test' save_txt=True save_conf=True conf=0.1 name=test_yolov9m
    yolo val model='./Pretrained_Model_Kuzushiji_Detection/yolov10m.pt' data=./Kuzushiji_Character_Detection_Dataset/meta.yaml split='test' save_txt=True save_conf=True conf=0.1 name=test_yolov10m
    yolo val model='./Pretrained_Model_Kuzushiji_Detection/yolo11m.pt' data=./Kuzushiji_Character_Detection_Dataset/meta.yaml split='test' save_txt=True save_conf=True conf=0.1 name=test_yolo11m
    yolo val model='./Pretrained_Model_Kuzushiji_Detection/yolo12m.pt' data=./Kuzushiji_Character_Detection_Dataset/meta.yaml split='test' save_txt=True save_conf=True conf=0.1 name=test_yolo12m
    yolo val model='./Pretrained_Model_Kuzushiji_Detection/rtdetr-l.pt' data=./Kuzushiji_Character_Detection_Dataset/meta.yaml split='test' save_txt=True save_conf=True conf=0.1 name=test_rtdetr-l
  ```

## :two: Kuzushiji Document Restoration
* The results of the parameter study are presented as follows:
  
  | τ<sub>r</sub> | (τ<sub>rg</sub>,τ<sub>rb</sub>) | PSNR<sub>Valid</sub> | SSIM<sub>Valid</sub> | PSNR<sub>Test</sub> | SSIM<sub>Test</sub> |
  | :--: | :--: | :--: | :--: | :--: | :--: |
  | -  | -   | 29.15dB | 0.9655 | 28.71dB | 0.9639 |
  | 80 | 1.2 | 29.76dB | 0.9470 | 29.61dB | 0.9465 |
  | 80 | 1.3 | 33.64dB | 0.9736 | 33.73dB | 0.9731 |
  | 80 | 1.4 | 33.87dB | 0.9756 | 33.77dB | 0.9745 |
  | 80 | 1.5 | 31.97dB | 0.9717 | 31.68dB | 0.9706 |
  | 90 | 1.2 | 30.37dB | 0.9522 | 30.19dB | 0.9519 |
  | 90 | 1.3 | 34.09dB | 0.9757 | 34.13dB | 0.9750 |
  | 90 | 1.4 | 34.05dB | 0.9763 | 33.94dB | 0.9753 |
  | 90 | 1.5 | 32.03dB | 0.9721 | 31.74dB | 0.9710 |

* Visual examples of document restoration results obtained with the parameters τ<sub>r</sub>=90, τ<sub>rg</sub>=τ<sub>rb</sub>=1.3:
  <p align="center">
    <img src="img/fig_restoration.png" width="1024" title="details">
  </p>

### Perform
* Example command for performing document restoration with `r_min = 90` and `rg_ratio & rb_ratio = 1.3`:
  ```
    python restoration.py --r_min 90 --rg_ratio 1.3 --rb_ratio 1.3
  ```

### Evaluate
* The ground-truth data (original document images) can be found at `Kuzushiji_Character_Detection_Dataset/images/test_raw`，available from [here](https://1drv.ms/f/c/56c255dd1bb9ae9e/IgCkDlP7XG_rS6xpc1Kgbt_7Aaw8cbbKyWJLVW6dbljB69k).
* Example command for evaluation using PSNR and SSIM is provided below:
  ```
    python restoration_metric.py
  ```
* The evaluation results will be saved to `./resotration_results`.

## :three: Kuzushiji Character Cropping
* To extract individual Kuzushiji character instances, we crop each character region based on the predicted bounding boxes：
  ```
    python crop.py
  ```
* The output directory `./visual_crop` contains: (1) Cropped images of individual Kuzushiji characters, and (2) Visualization results of the original images overlaid with the predicted bounding boxes.

## :four: Kuzushiji Character Classification
* The results of the ablation study are presented as follows:

  | Method | Document Restoration (Stage 2) | Top-1 Accuracy | Top-5 Accuracy | 
  | :--: | :--: | :--: | :--: |
  | Metom |  | 93.45% | 97.46% | 
  | Metom | ✔ | 95.33% | 98.62% |

* We employ [Metom](https://codh.rois.ac.jp/char-shape/app/metom/) for Kuzushiji character classification, and the official source code is available on [Hugging Face](https://huggingface.co/SakanaAI/Metom).
* To perform Kuzushiji character classification and evaluate the recognition performance, please run the following commands:
  ```
    python classification.py
    python classification_metric.py
  ```
* These scripts will generate the classification results and report the Top-1 Error and Top-5 Error metrics.

## :five: Final Mapping
  <p align="center">
    <img src="img/fig_final_output.png" width="1024" title="details">
  </p>
  
* After running `classification.py` to generate the `.json` file, please execute the following command to map the prediction results onto the restored document images:
  ```
    python final_map.py --image path/to/restored_image.jpg --json /path/to/classification_results.json --out ./final_output_image.jpg --font_size 64
  ```

# License
<img src="./img/CC-BY-SA.png" alt="CC BY-SA 4.0 License" width="100" style="vertical-align: middle;">  

This benchmark dataset is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).

### Original Kuzushiji Dataset

The original Kuzushiji dataset used in this work is based on **『日本古典籍くずし字データセット』** (National Institute of Japanese Literature / CODH), provided by [ROIS-DS Center for Open Data in the Humanities (CODH)](https://codh.rois.ac.jp/), which is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).

The following is the citation of the original Kuzushiji dataset; please cite it:
  ```
    『日本古典籍くずし字データセット』 （国文研所蔵／CODH加工） doi:10.20676/00000340
  ```
