#!/usr/bin/env python
from __future__ import print_function
import os
import subprocess
import argparse

def ensure_directory_exists(directory):
    """Ensure the directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)

def fx_upscale_smart(src_file, dst_file):
    """Apply the fx_upscale_smart effect to the source file and save the result."""
    gmic_command = [
        "gmic",
        src_file,
        "-fx_upscale_smart", "1280,720,1,0,0.4,21",
        "-o", dst_file
    ]
    process = subprocess.Popen(gmic_command)
    process.communicate()

def iain_constrained_sharpen(src_file, dst_file):
    """Apply the iain_constrained_sharpen effect to the source file and save the result."""
    sharp_radius = 0.75
    sharp_amount = 2
    sharp_threshold = 1
    constrain_radius = 5
    overshoot = 0

    gmic_command = [
        "gmic",
        src_file,
        "-iain_constrained_sharpen",
        "%s,%s,%s,%s,%s,0,1" % (sharp_radius, sharp_amount, sharp_threshold, constrain_radius, overshoot),
        "-o", dst_file
    ]
    process = subprocess.Popen(gmic_command)
    process.communicate()

def process_images(sharpen_order):
    """Iterate through image files, process them with gmic, and save the result."""
    output_dir = "gmic-output"
    ensure_directory_exists(output_dir)

    i = 1
    while True:
        input_file = "blues%s.png" % i
        if not os.path.exists(input_file):
            break

        upscale_folder = os.path.join(output_dir, "fx_upscale_smart")
        ensure_directory_exists(upscale_folder)

        if sharpen_order == -1:
            # iain_constrained_sharpen first
            sharpen_folder = os.path.join(output_dir, "iain_constrained_sharpen")
            ensure_directory_exists(sharpen_folder)
            sharpened_file = os.path.join(sharpen_folder, input_file)

            iain_constrained_sharpen(input_file, sharpened_file)

            # Then fx_upscale_smart
            final_file = os.path.join(upscale_folder, input_file)

            fx_upscale_smart(sharpened_file, final_file)

            # Move the final file to iain_constrained_sharpen+fx_upscale_smart
            final_output_folder = os.path.join(output_dir, "iain_constrained_sharpen+fx_upscale_smart")
            ensure_directory_exists(final_output_folder)
            final_file = os.path.join(final_output_folder, input_file)

            # Rename the processed file to the final destination
            os.rename(final_file, final_file)

        elif sharpen_order == 1:
            # fx_upscale_smart first
            upscaled_file = os.path.join(upscale_folder, input_file)

            fx_upscale_smart(input_file, upscaled_file)

            # Then iain_constrained_sharpen
            sharpen_folder = os.path.join(output_dir, "fx_upscale_smart+iain_constrained_sharpen")
            ensure_directory_exists(sharpen_folder)
            final_file = os.path.join(sharpen_folder, input_file)

            iain_constrained_sharpen(upscaled_file, final_file)

        elif sharpen_order == 0:
            # Use fx_upscale_smart for no sharpening
            final_file = os.path.join(upscale_folder, input_file)
            fx_upscale_smart(input_file, final_file)

        print("Processed:", final_file)

        i += 1

def main():
    parser = argparse.ArgumentParser(description="Process images using gmic with optional sharpening.")
    parser.add_argument(
        '-n', '--sharpen-order', type=int, choices=[-1, 0, 1], default=-1,
        help="Order of sharpen filter: -1 for before scaling (default), 1 for after scaling, 0 to skip sharpening."
    )
    args = parser.parse_args()

    process_images(args.sharpen_order)

if __name__ == "__main__":
    main()
