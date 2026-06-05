# NDLKotenOCR
This is for reference only. Please refer to the [original GitHub repository](https://github.com/ndl-lab/ndlkotenocr_cli) for details.

## Environment
```
  pip install -r requirements.txt
```
## Download
* For calculating the speed, after cloning the repository, replace the cloned `main.py` with the `main.py` provided here.
```
  git clone https://github.com/ndl-lab/ndlkotenocr_cli
```
* Download the NDLKotenOCR ver.3 pre-trained models [here](https://1drv.ms/f/c/56c255dd1bb9ae9e/IgDiLBlaev4XQ46AdIStVkE2Ab97A9c0c9QBD5IabfERfuQ).
* Put the pre-trained models as follows:
```
ndlocr_cli
  └── src 
      ├── ndl_kotenseki_layout/models/ndl_kotenseki_layout_ver3.pth
      └── text_kotenseki_recognition/model-ver2
```
## Run
```
  python main.py infer input_root output_dir
```
* `input_root` and `output_dir` are as follows:
