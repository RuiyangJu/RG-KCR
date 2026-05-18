# Seal-Robust KCR
Seal-Robust KCR: A Framework for Stable Kuzushiji Character Recognition in Japanese Historical Documents
>[arXiv](https://arxiv.org/abs/2602.19086)
>[Project](https://ruiyangju.github.io/RG-KCR/)

# Pipeline
  <p align="left">
    <img src="img/fig_pipeline.png" width="1024" title="details">
  </p>
Conventional pipeline (blue flow) and the proposed pipeline (red flow) for seal-interference Kuzushiji document images.
Dashed arrows indicate additional processes performed in parallel with character detection without affecting the detection results.

# Citation
* If you find our paper useful in your research, please consider citing:
  ```
    @article{ju2026rgkcr,
      title={Restoration-Guided Kuzushiji Character Recognition Framework under Seal Interference},
      author={Ju, Rui-Yang and Yamashita, Kohei and Kameko, Hirotaka and Mori, Shinsuke},
      journal={arXiv preprint arXiv:2602.19086},
      year={2026}
    }
  ```

# Dataset
## ① Data Collection
* The original dataset is available from the [Center for Open Data in the Humanities (CODH)](https://codh.rois.ac.jp/char-shape/book/), and the raw data is held by [National Institute of Japanese Literature (NIJL)](https://www.nijl.ac.jp/db/).

| Index | NIJL ID | Book Title | Pages | Characters | Chars/Page |
| :--: | :--: | :--: | :--: | :--: | :--: |
| 1 | 100241706 | Usonarubeshi (虚南留別志) | 67 | 8,565 | 127.8 |
| 2 | 100249376 | Gozenkashi Hiden-shou (御前菓子秘伝抄) | 104 | 11,841 | 113.9 |
| 3 | 100249416 | Mochigashi Sokuseki Teseishuu (餅菓子即席手製集) | 58 | 7,967 | 137.4 |
| 4 | 100249476 | Meshi Hyakuchin Den (飯百珍伝) | 46 | 7,842 | 170.5 |
| 5 | 200006663 | Diguchi (ぢぐち) | 8 | 121 | 15.1 |
| 6 | 200015843 | Nippon Eitaigura (日本永代蔵) | 180 | 50,251 | 279.2 |
| 7 | 200017458 | Soga Monogatari (曾我物語) | 78 | 29,641 | 380.0 |
| 8 | 200020019 | Chikusai (竹斎) | 146 | 33,228 | 227.6 |
| 9 | 200021086 | Isoho Monogatari (伊曾保物語) | 60 | 15,410 | 256.8 |
| 10 | 200021763 | Zenbu Ryouri-shou (膳部料理抄) | 94 | 11,437 | 121.7 |
| 11 | 200021802 | Ryouri Monogatari (料理物語) | 105 | 19,609 | 186.8 |
| 12 | 200021869 | Ryourikata Kokoroenokoto (料理方心得之事) | 30 | 3,012 | 100.4 |
| 13 | 200022050 | Ryouri Hiden-shou (料理秘伝抄) | 24 | 9,558 | 398.3 |
| Total | N/A | N/A | 1,000 | 208,482 | 208.5 |

* Accordingly, we selected the **1,000** annotated images listed above as the benchmark dataset.

## ② Data Correction
* Among the **1,000** annotated images, we found that **267** images contained incomplete annotations.
* As shown below, the red bounding boxes are annotated by us, while the green bounding boxes are from the original annotations:
  <p align="left">
    <img src="img/fig_correction.png" width="1024" title="details">
  </p>
* These missing labels were manually corrected, and the corresponding image names are listed below:

  <table>
  <tr>
  <td valign="top">
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
  </td>
  
  <td valign="top">
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
  </td>
  
  <td valign="top">
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
  </td>
  </tr>
  
  
  <tr>
  <td valign="top">
  <details>
  <summary>100249476 (3 images)</summary>
  <ul>
  <li>100249476_00016_1</li>
  <li>100249476_00016_2</li>
  <li>100249476_00018_1</li>
  </ul>
  </details>
  </td>
  
  <td valign="top">
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
  </td>
  
  <td valign="top">
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
  </td>
  </tr>
  
  <tr>
  <td valign="top">
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
  </td>
  
  <td valign="top">
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
  </td>
  
  <td valign="top">
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
  </td>
  </tr>
  
  <tr>
  <td valign="top">
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
  </td>
  
  <td valign="top">
  <details>
  <summary>200021869 (3 images)</summary>
  <ul>
  <li>200021869_00004_2</li>
  <li>200021869_00008_2</li>
  <li>200021869_00014_1</li>
  </ul>
  </details>
  </td>
  
  <td valign="top">
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
  </td>
  </tr>
  </table>

## ③ Data Splitting
* The **1,000** annotated images were randomly split into training, validation, and test sets with a ratio of **8:1:1**, consisting of **800** training images, **100** validation images, and **100** test images.
* The **real dataset** can be downloaded from [here](https://1drv.ms/f/c/56c255dd1bb9ae9e/IgDiLBlaev4XQ46AdIStVkE2Ab97A9c0c9QBD5IabfERfuQ).

## ④ Synthetic Data Augmentation
* For the training set, **128** high-quality red seal images were used for synthetic data augmentation, thereby expanding the training set from **800** corrected images to **1,600** images.
* **Real** vs. **synthetic** seal-interfered documents:
  <p align="left">
    <img src="img/fig_synthetic.png" width="1024" title="details">
  </p>
* The **synthetic dataset** through synthetic data augmentation can be downloaded from [here](https://1drv.ms/f/c/56c255dd1bb9ae9e/IgCkDlP7XG_rS6xpc1Kgbt_7Aaw8cbbKyWJLVW6dbljB69k).
* Notably, if you want to train on both the real and synthetic datasets together, please make sure that the image names across the two datasets are different.

# Experiments
## Environment
  ```
    conda create -n Kuzushiji python=3.10
    pip install -r requirements.txt
  ```

## ① Kuzushiji Character Detection
* The evaluation results on the test set are presented as follows:

  | Method | Params | FLOPs | Epoch | FPS | P<sup>Real</sup> | R<sup>Real</sup> | AP<sub>50</sub><sup>Real</sup> | AP<sub>50:95</sub><sup>Real</sup> | P<sup>Synth.</sup> | R<sup>Synth.</sup> | AP<sub>50</sub><sup>Synth.</sup> | AP<sub>50:95</sub><sup>Synth.</sup> |
  | :-- | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
  | RT-DETR-R50 | 41.94M | 125.6G | 988 | 11.8 | 93.6% | 90.3% | 94.3% | 70.1% | 91.1% | 85.0% | 90.8% | 65.2% |
  | **+ SAD (Ours)** | 41.94M | 125.6G | 736 | 11.7 | 96.3% | 93.1% | 95.6% | 70.5% | 95.6% | 92.2% | 95.0% | 68.4% |
  | YOLOv10-L| 25.77M | 127.2G | 781 | 11.0 | 98.0% | 92.0% | 96.3% | 82.5% | 95.7% | 87.2% | 93.6% | 77.5% |
  | **+ SAD (Ours)** | 25.77M | 127.2G | 415 | 11.0 | 98.3% | 92.7% | 96.5% | 83.1% | 98.0% | 92.4% | 96.4% | 81.8% |
  | YOLO11-L | 25.28M | 86.6G | 549 | 10.5 | 97.9% | 92.9% | 96.4% | 83.0% | 95.8% | 87.7% | 93.7% | 78.1% |
  | **+ SAD (Ours)** | 25.28M | 86.6G | 440 | 10.5 | 98.0% | 93.5% | 96.5% | 83.3% | 97.6% | 93.1% | 96.4% | 82.1% |
  | YOLOv12-L | 26.39M | 82.1G | 909 | 10.5 | 97.4% | 93.4% | 96.4% | 82.7% | 95.5% | 87.7% | 93.7% | 77.6% |
  | **+ SAD (Ours)** | 26.39M | 82.1G | 408 | 10.4 | 97.5% | 93.6% | 96.5% | 83.2% | 97.5% | 92.8% | 96.3% | 81.9% |

### Train:
* Please ensure that the dataset is placed under `./yolov12/dataset` and organized as follows:

  ```
    yolov12
    └── dataset
        ├── meta_raw.yaml
        ├── meta_aug.yaml
        ├── images
        │   ├── train
        │   │   ├── train_img1.png
        │   │   └── ...
        │   ├── valid
        │   │   ├── valid_img1.png
        │   │   └── ...
        │   ├── test_raw
        │   │   ├── test_raw_img1.png
        │   │   └── ...
        │   └── test_aug
        │       ├── test_aug_img1.png
        │       └── ...
        └── labels
            ├── train
            │   ├── train_annotation1.txt
            │   └── ...
            ├── valid
            │   ├── valid_annotation1.txt
            │   └── ...
            ├── test_raw
            │   ├── test_raw_annotation1.txt
            │   └── ...
            └── test_aug
                ├── test_aug_annotation1.txt
                └── ...
    ```

* Please update the dataset path (`/path/to/data`) in both `./yolov12/dataset/meta_raw.yaml` and `./yolov12/dataset/meta_aug.yaml` before training.
* You can train the model by running the corresponding training script. For example, `train_yolo12l.py` can be used to train the model:

  ```
    from ultralytics import YOLO
    
    model = YOLO('./ultralytics/cfg/models/v12/yolov12l.yaml')
    
    # Train the model
    results = model.train(
      data='./dataset/meta_raw.yaml',
      epochs=1000, 
      batch=16, 
      imgsz=640,
      optimizer="SGD",
      lr0=0.01,
      device="0",
      name="train_yolo12l"
    )
    
    # Evaluate model performance on the validation set
    metrics = model.val()
  ```

* You can train the baseline models and our model as follows:

  ```
    cd Seal-Robust-KCR/yolov12
    python train_rtdetr_resnet50.py
    python train_yolov9c.py
    python train_yolov10l.py
    python train_yolo11l.py
    python train_yolo12l.py 
  ```

### Test_Raw:
  ```
    cd Seal-Robust-KCR/yolov12
    python test_raw_rtdetr_resnet50.py
    python test_raw_yolov9c.py
    python test_raw_yolov10l.py
    python test_raw_yolo11l.py
    python test_raw_yolo12l.py 
  ```

### Test_Aug:
  ```
    cd Seal-Robust-KCR/yolov12
    python test_aug_rtdetr_resnet50.py
    python test_aug_yolov9c.py
    python test_aug_yolov10l.py
    python test_aug_yolo11l.py
    python test_aug_yolo12l.py 
  ```
  
## ② Kuzushiji Document Restoration
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
  <p align="left">
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

## ③ Kuzushiji Character Cropping
* To extract individual Kuzushiji character instances, we crop each character region based on the predicted bounding boxes：
  ```
    python crop.py
  ```
* The output directory `./visual_crop` contains: (1) Cropped images of individual Kuzushiji characters, and (2) Visualization results of the original images overlaid with the predicted bounding boxes.

## ④ Kuzushiji Character Classification

## :two: Kuzushiji Character Classification 
* Details of the dataset are summarized as follows：

  | Test set #Images | Total GT Bounding Boxes | Total Pred Bounding Boxes | Total Matched Pairs (IoU>=0.5) |
  | :--: | :--: | :--: | :--: |
  | 100 | 19,035 | 18,656 | 17,982 |

* The ground-truth data for the test set can be accessed at the following [link](https://1drv.ms/f/c/56c255dd1bb9ae9e/IgDDpS626Jn_RqpJcP7bLY2OAR9Eascelseepquchb3bOXk?e=TdsKac).


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

## ⑤ Final Mapping
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
