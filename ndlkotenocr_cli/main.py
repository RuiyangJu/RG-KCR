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

from cli.core import OcrInferencer
from cli.core import utils


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
def infer(ctx, input_root, output_root, config_file, input_structure, add_info):
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

    cfg = {
        'input_root': input_root,
        'output_root': output_root,
        'config_file': config_file,
        'input_structure': input_structure,
        'add_info': add_info
    }

    # Check if input_root exists
    if not os.path.exists(input_root):
        print(f'INPUT_ROOT not found : {input_root}', file=sys.stderr)
        sys.exit(0)

    # Parse command line options
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

    # Prepare output root directory
    infer_cfg['output_root'] = utils.mkdir_with_duplication_check(
        infer_cfg['output_root']
    )

    # Save inference options
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

    # Initialize inferencer
    inferencer = OcrInferencer(infer_cfg)

    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.synchronize()

    start_time = time.perf_counter()

    inferencer.run()

    if torch.cuda.is_available():
        torch.cuda.synchronize()

    end_time = time.perf_counter()

    total_time = end_time - start_time
    avg_time = total_time / num_images
    fps = num_images / total_time

    print(f'Total Inference Time: {total_time:.4f} sec')
    print(f'Average Inference Time: {avg_time:.4f} sec')
    print(f'Average Inference Speed: {fps:.2f} fps')

    gpu_result = {}

    if torch.cuda.is_available():
        max_memory_allocated = torch.cuda.max_memory_allocated() / 1024**3
        max_memory_reserved = torch.cuda.max_memory_reserved() / 1024**3

        print(f'GPU Max Memory Allocated: {max_memory_allocated:.4f} GB')
        print(f'GPU Max Memory Reserved: {max_memory_reserved:.4f} GB')

        gpu_result = {
            "gpu_max_memory_allocated_GB": round(max_memory_allocated, 4),
            "gpu_max_memory_reserved_GB": round(max_memory_reserved, 4)
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
