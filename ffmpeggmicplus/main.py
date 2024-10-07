from __future__ import print_function
import argparse
import ffmpeg
import gmic
import numpy as np
import sys

# Default G'MIC plugin options
gmic_plugin_options = {
    'width_scale': 178,
    'height_scale': 150,
    'smoothness': 0,
    'anisotropy': 0.4,
    'sharpness': 21,
}


def main():
    """Main function to upscale video using G'MIC diffusion upscale."""
    parser = argparse.ArgumentParser(
        description="Upscale a 16:9 DVD video to 1280x720 using G'MIC."
    )
    parser.add_argument("input_file", help="Input video file")
    parser.add_argument("output_file", help="Output video file")
    parser.add_argument(
        "--width_scale", type=int, default=gmic_plugin_options['width_scale'],
        help="Percentage to upscale width (default: 178)"
    )
    parser.add_argument(
        "--height_scale", type=int, default=gmic_plugin_options['height_scale'],
        help="Percentage to upscale height (default: 150)"
    )
    parser.add_argument(
        "--smoothness", type=int, default=gmic_plugin_options['smoothness'],
        help="Smoothness level for G'MIC processing (default: 0)"
    )
    parser.add_argument(
        "--anisotropy", type=float, default=gmic_plugin_options['anisotropy'],
        help="Anisotropy level for G'MIC processing (default: 0.4)"
    )
    parser.add_argument(
        "--sharpness", type=int, default=gmic_plugin_options['sharpness'],
        help="Sharpness level for G'MIC processing (default: 21)"
    )

    args = parser.parse_args()

    # Update gmic_plugin_options dictionary with command-line arguments
    gmic_plugin_options['width_scale'] = args.width_scale
    gmic_plugin_options['height_scale'] = args.height_scale
    gmic_plugin_options['smoothness'] = args.smoothness
    gmic_plugin_options['anisotropy'] = args.anisotropy
    gmic_plugin_options['sharpness'] = args.sharpness

    # ffmpeg process to get frames
    input_file = args.input_file
    output_file = args.output_file

    probe = ffmpeg.probe(input_file)
    video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
    width = int(video_info['width'])
    height = int(video_info['height'])

    process1 = (
        ffmpeg
        .input(input_file)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .run_async(pipe_stdout=True)
    )

    process2 = (
        ffmpeg
        .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='%dx%d' % (width, height))
        .output(output_file, pix_fmt='yuv420p')
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )

    while True:
        in_bytes = process1.stdout.read(width * height * 3)
        if not in_bytes:
            break

        in_frame = np.frombuffer(in_bytes, np.uint8).reshape([height, width, 3])

        # G'MIC processing with the updated plugin options
        gmic_command = "fx_dreamsmooth %d,%d,%d,%0.2f,%d" % (
            gmic_plugin_options['width_scale'], gmic_plugin_options['height_scale'],
            gmic_plugin_options['smoothness'], gmic_plugin_options['anisotropy'],
            gmic_plugin_options['sharpness']
        )
        gmic_instance = gmic.Gmic(gmic_command)
        out_frame = gmic_instance.run(in_frame)

        process2.stdin.write(out_frame.astype(np.uint8).tobytes())

    process2.stdin.close()
    process1.wait()
    process2.wait()


if __name__ == '__main__':
    sys.exit(main())
