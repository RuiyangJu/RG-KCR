# NDLKotenOCR-Lite
This is for reference only. Please refer to the [original GitHub repository](https://github.com/ndl-lab/ndlkotenocr-lite) for details.

## Environment
```
  git clone https://github.com/ndl-lab/ndlkotenocr-lite
  cd ndlkotenocr-lite
  pip install -r requirements.txt
```

## Run
* For calculating the inference speed, after cloning the repository, replace the cloned `ocr.py` with the `ocr.py` provided here.
```
  cd src
  python3 ocr.py --sourcedir input_root --output output_dir --device cpu
```

## Evaluate
* Evaluate the performance (CER):
```
  cd src
  python evaluate.py --gt_dir gt_folder --pred output_dir/txt --output_csv output
```
