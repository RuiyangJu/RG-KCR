#!/bin/bash
set -e

START_TIME=$(date +%s)

# Input Root
TEST_SET="test_aug"
RUN_EVAL="false"
MONITOR_GPU="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        --test_set)
            TEST_SET="$2"
            shift 2
            ;;
        --run_eval)
            RUN_EVAL="$2"
            shift 2
            ;;
        --monitor_gpu)
            MONITOR_GPU="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: bash run_pipeline.sh --test_set [test_raw|test_aug] --run_eval [true|false] --monitor_gpu [true|false]"
            exit 1
            ;;
    esac
done

if [[ "$TEST_SET" != "test_raw" && "$TEST_SET" != "test_aug" ]]; then
    echo "TEST_SET must be test_raw or test_aug"
    exit 1
fi

if [[ "$RUN_EVAL" != "true" && "$RUN_EVAL" != "false" ]]; then
    echo "RUN_EVAL must be true or false"
    exit 1
fi

if [[ "$MONITOR_GPU" != "true" && "$MONITOR_GPU" != "false" ]]; then
    echo "MONITOR_GPU must be true or false"
    exit 1
fi

# GPU Memory Monitor
GPU_ID=0
GPU_MONITOR_INTERVAL=0.05
GPU_MEMORY_LOG="./peak_gpu_memory.log"
GPU_MONITOR_PID=""

monitor_gpu_memory() {
    while true; do
        MEM=$(nvidia-smi --id=${GPU_ID} \
            --query-gpu=memory.used \
            --format=csv,noheader,nounits 2>/dev/null | head -n 1)

        if [[ -n "$MEM" ]]; then
            echo "$MEM" >> ${GPU_MEMORY_LOG}
        fi

        sleep ${GPU_MONITOR_INTERVAL}
    done
}

cleanup() {
    if [[ -n "$GPU_MONITOR_PID" ]]; then
        kill ${GPU_MONITOR_PID} 2>/dev/null || true
    fi
}
trap cleanup EXIT

if [[ "$MONITOR_GPU" = "true" ]]; then
    echo "0" > ${GPU_MEMORY_LOG}
    monitor_gpu_memory &
    GPU_MONITOR_PID=$!
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

echo "Seal-Robust-KCR Inference Pipeline"
echo "Test Set: ${TEST_SET}"
echo "Evaluation: ${RUN_EVAL}"
echo "Monitor GPU: ${MONITOR_GPU}"
echo "GPU ID: ${GPU_ID}"

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
wait ${DET_PID} || exit 1
wait ${REST_PID} || exit 1

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
    --out_dir ${CLS_OUTPUT}

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

END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))

echo "Pipeline Finished"
echo "Final TXT results are saved in: ${ORDER_OUTPUT}"
echo "Total Pipeline Time: ${TOTAL_TIME} sec"

if [[ "$MONITOR_GPU" = "true" ]]; then
    kill ${GPU_MONITOR_PID} 2>/dev/null || true
    trap - EXIT

    PEAK_GPU_MEMORY_MB=$(sort -nr ${GPU_MEMORY_LOG} | head -n 1)
    PEAK_GPU_MEMORY_GB=$(awk "BEGIN {printf \"%.4f\", ${PEAK_GPU_MEMORY_MB}/1024}")

    echo "Peak GPU Memory Used: ${PEAK_GPU_MEMORY_GB} GB (${PEAK_GPU_MEMORY_MB} MiB)"
fi
