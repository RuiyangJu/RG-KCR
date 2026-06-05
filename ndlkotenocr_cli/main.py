# Copyright (c) 2022, National Diet Library, Japan
#
# This software is released under the CC BY 4.0.
# https://creativecommons.org/licenses/by/4.0/

import click
import json
import os
import sys
import time
import torch
import subprocess
import threading

from cli.core import OcrInferencer
from cli.core import utils


class GPUMemoryMonitor:
    def __init__(self, gpu_id=0, interval=0.05):
        self.gpu_id = gpu_id
        self.interval = interval
        self.max_memory_mb = 0
        self.running = False
        self.thread = None

    def _query_memory(self):
        try:
            result = subprocess.check_output(
                [
                    "nvidia-smi",
                    f"--id={self.gpu_id}",
                    "--query-gpu=memory.used",
                    "--format=csv,noheader,nounits"
                ],
                encoding="utf-8"
            )
            return int(result.strip().split("\n")[0])
        except Exception:
            return 0

    def _monitor(self):
        while self.running:
            mem_mb = self._query_memory()
            self.max_memory_mb = max(self.max_memory_mb, mem_mb)
            time.sleep(self.interval)

    def start(self):
        self.running = True
        self.max_memory_mb = self._query_memory()
        self.thread = threading.Thread(target=self._monitor, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()
        self.max_memory_mb = max(self.max_memory_mb, self._query_memory())

    def max_memory_gb(self):
        return self.max_memory_mb / 1024


@click.group()
@click.option('--debug', is_flag=True)
@click.pass_context
def cmd(ctx, debug):
    ctx.obj['DEBUG'] = debug


@cmd.command()
@click.pass_context
def help(ctx):
    if ctx.obj['DEBUG']:
        click.echo('DEBUG MODE!')
    click.echo('help!')


@cmd.command()
@click.pass_context
@click.argument('input_root')
@click.argument('output_root')
@click.option(
    '-s',
    '--input_structure',
    type=click.Choice(['s', 'b', 'f', 'i'], case_sensitive=True),
    default='s',
    help='Input directory structure type. s(single) and f(image_file).'
)
@click.option(
    '-c',
    '--config_file',
    type=str,
    default='config.yml',
    help='Configuration yml file for inference. Default is "config.yml".'
)
@click.option(
    '-a',
    '--add_info',
    is_flag=True,
    help='Record information about the source image in the output json file. (Note that the json format will change.)'
)
@click.option(
    '--gpu_id',
    type=int,
    default=0,
    help='GPU ID used for nvidia-smi memory monitoring.'
)
def infer(ctx, input_root, output_root, config_file, input_structure, add_info, gpu_id):
    """
    \b
    INPUT_ROOT    : Input data directory for inference.
    OUTPUT_ROOT   : Output directory for inference result.
    """

    click.echo('start inference !')
    click.echo(f'input_root : {input_root}')
    click.echo(f'output_root : {output_root}')
    click.echo(f'config_file : {config_file}')
    click.echo(f'add_info : {add_info}')
    click.echo(f'gpu_id : {gpu_id}')

    cfg = {
        'input_root': input_root,
        'output_root': output_root,
        'config_file': config_file,
        'input_structure': input_structure,
        'add_info': add_info
    }

    if not os.path.exists(input_root):
        print(f'INPUT_ROOT not found : {input_root}', file=sys.stderr)
        sys.exit(0)

    infer_cfg = utils.parse_cfg(cfg)

    if infer_cfg is None:
        print(f'[ERROR] Config parse error : {input_root}', file=sys.stderr)
        sys.exit(1)

    print(
        "ndl_kotenseki_layout checkpoint_path:",
        infer_cfg.get("ndl_kotenseki_layout", {}).get("checkpoint_path")
    )

    print(
        "text_kotenseki_recognition saved_ocr_model:",
        infer_cfg.get("text_kotenseki_recognition", {}).get("saved_ocr_model")
    )

    infer_cfg['output_root'] = utils.mkdir_with_duplication_check(
        infer_cfg['output_root']
    )

    with open(
        os.path.join(infer_cfg['output_root'], 'opt.json'),
        'w',
        encoding='utf-8'
    ) as fp:
        json.dump(
            infer_cfg,
            fp,
            ensure_ascii=False,
            indent=4,
            sort_keys=True,
            separators=(',', ': ')
        )

    image_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp')

    num_images = 0
    for root, _, files in os.walk(input_root):
        for file in files:
            if file.lower().endswith(image_exts):
                num_images += 1

    print(f'[INFO] Number of images : {num_images}')

    if num_images == 0:
        print('[ERROR] No images found.', file=sys.stderr)
        sys.exit(1)

    inferencer = OcrInferencer(infer_cfg)

    gpu_monitor = None

    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

        gpu_monitor = GPUMemoryMonitor(gpu_id=gpu_id)
        gpu_monitor.start()

    start_time = time.perf_counter()

    inferencer.run()

    if torch.cuda.is_available():
        torch.cuda.synchronize()

    if gpu_monitor is not None:
        gpu_monitor.stop()

    end_time = time.perf_counter()

    total_time = end_time - start_time
    avg_time = total_time / num_images
    fps = num_images / total_time

    print(f'Total Inference Time: {total_time:.4f} sec')
    print(f'Average Inference Time: {avg_time:.4f} sec')
    print(f'Average Inference Speed: {fps:.2f} fps')

    gpu_result = {}

    if gpu_monitor is not None:
        peak_gpu_memory_gb = gpu_monitor.max_memory_gb()

        print(f'Peak GPU Memory Used: {peak_gpu_memory_gb:.4f} GB')

        gpu_result = {
            "peak_gpu_memory_used_GB": round(peak_gpu_memory_gb, 4)
        }

    speed_result = {
        "num_images": num_images,
        "total_time_sec": round(total_time, 4),
        "avg_time_per_image_sec": round(avg_time, 4),
        "fps": round(fps, 2),
        **gpu_result
    }

    with open(
        os.path.join(infer_cfg['output_root'], 'speed.json'),
        'w',
        encoding='utf-8'
    ) as f:
        json.dump(speed_result, f, ensure_ascii=False, indent=4)


def main():
    cmd(obj={})


if __name__ == '__main__':
    main()
