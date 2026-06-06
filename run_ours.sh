#!/bin/bash
set -e

# Input Root
TEST_SET=${1:-test_aug}
RUN_EVAL=${2:-false}

if [[ "$TEST_SET" != "test_raw" && "$TEST_SET" != "test_aug" ]]; then
    echo "Usage: bash run_pipeline.sh [test_raw|test_aug] [true|false]"
    exit 1
fi

if [[ "$RUN_EVAL" != "true" && "$RUN_EVAL" != "false" ]]; then
    echo "RUN_EVAL must be true or false"
    exit 1
fi

DATASET_DIR="./dataset"
REAL_YAML="${DATASET_DIR}/meta_raw.yaml"
SYNTH_YAML="${DATASET_DIR}/meta_aug.yaml"

MODEL="./detection/models/YOLO11L_SDA.pt"
IMAGE_DIR="${DATASET_DIR}/images/${TEST_SET}"

# Output Root
DET_OUTPUT="./detection/runs/detect/test_YOLO11L_SDA"
REST_OUTPUT="./restoration/output"
CROP_OUTPUT="./crop/output"
CLS_OUTPUT="./classification/output"
ORDER_OUTPUT="./ordering/output_ours"
ORDER_CSV="./evaluation_results"

# Hyperparameters
R_MIN=90
RG_RATIO=1.3
RB_RATIO=1.3

echo " Seal-Robust-KCR Inference Pipeline"
echo " Test Set: ${TEST_SET}"
echo " Evaluation: ${RUN_EVAL}"

# Check model
if [ ! -f "${MODEL}" ]; then
    echo "Model not found: ${MODEL}"
    exit 1
fi

# Select YAML
if [ "$TEST_SET" = "test_raw" ]; then
    DATA_YAML=${REAL_YAML}
else
    DATA_YAML=${SYNTH_YAML}
fi

# (1) Character Detection + (2) Document Restoration (Parallel)
echo "(1) Character Detection"
python ./detection/test.py \
    --model ${MODEL} \
    --data ${DATA_YAML} &
DET_PID=$!

echo "(2) Document Restoration"
python ./restoration/run.py \
    --input_dir ${IMAGE_DIR} \
    --output_dir ${REST_OUTPUT} \
    --r_min ${R_MIN} \
    --rg_ratio ${RG_RATIO} \
    --rb_ratio ${RB_RATIO} &
REST_PID=$!

echo "Waiting for detection and restoration..."
wait ${DET_PID}
wait ${REST_PID}

echo "Detection and restoration finished."

# (3) Character Cropping
echo "(3) Character Cropping"

python ./crop/run.py \
    --image_dir ${REST_OUTPUT} \
    --labels_dir ${DET_OUTPUT}/labels \
    --save_root ${CROP_OUTPUT}

# (4) Character Classification
echo "(4) Character Classification"

python ./classification/run.py \
    --root_dir ${CROP_OUTPUT}/crops \
    --out_dir ${CLS_OUTPUT} \

# (5) Character Ordering
echo "(5) Character Ordering"

python ./ordering/run_ours.py \
    --input_dir ${CLS_OUTPUT} \
    --output_dir ${ORDER_OUTPUT}

# (6) CER Evaluation (Optional)
if [ "$RUN_EVAL" = "true" ]; then
    echo "(6) CER Evaluation (Optional)"

    python ./ordering/evaluate.py \
        --gt_dir ./ordering/gt \
        --pred_dir ${ORDER_OUTPUT} \
        --out_csv ${ORDER_CSV}
fi

echo "Pipeline Finished"
echo "Final TXT results are saved in: ${ORDER_OUTPUT}"
