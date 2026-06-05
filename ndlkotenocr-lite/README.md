# NDLKotenOCR-Lite
This is for reference only. Please refer to the [original GitHub repository](https://github.com/ndl-lab/ndlkotenocr-lite) for details.

## Environment
```
  git clone https://github.com/ndl-lab/ndlkotenocr-lite
  cd ndlkotenocr-lite
  pip install -r requirements.txt
  cd src
```

## Run
* For calculating the speed and GPU memory, after cloning the repository, replace the cloned `ocr.py` with the `ocr.py` provided here.
```
  python3 ocr.py --sourcedir input_root --output output_dir
```

## Evaluate
* Evaluate the performance (CER):
```
  python evaluate.py --gt_dir gt_folder --pred output_dir/txt --output_csv output
```
