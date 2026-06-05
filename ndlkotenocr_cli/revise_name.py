from pathlib import Path
import argparse


def main(input_dir):
    folder = Path(input_dir)

    if not folder.exists():
        print(f"Error: {folder} does not exist.")
        return

    for txt_file in folder.glob("*_main.txt"):
        new_name = txt_file.name.replace("_main.txt", ".txt")
        new_path = txt_file.with_name(new_name)

        txt_file.rename(new_path)
        print(f"Renamed: {txt_file.name} -> {new_name}")

    print("Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rename *_main.txt files to *.txt"
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Input directory containing txt files"
    )

    args = parser.parse_args()

    main(args.input)