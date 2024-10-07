from __future__ import print_function
import ffmpeg
import gmic
import numpy as np

def upscale_diffusion_dvd_16_9_to_720p(input_file, output_file, width_scale=178, height_scale=150,
                                       smoothness=0, anisotropy=0.4, sharpness=21):
    """Upscale video using G'MIC diffusion, then crop/pad to make exactly 1280x720."""

    # Start by decoding the input video
    probe = ffmpeg.probe(input_file)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

    width = int(video_stream['width'])
    height = int(video_stream['height'])

    # Calculate new dimensions
    width_new = int(width * width_scale / 100)
    height_new = int(height * height_scale / 100)

    remove_left = int((width_new - 1280) / 2)
    remove_right = (width_new - 1280) - remove_left
    remove_top = int((height_new - 720) / 2)
    remove_bottom = (height_new - 720) - remove_top

    # Initialize FFmpeg processes
    process1 = (
        ffmpeg
        .input(input_file)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24', vframes=8)
        .run_async(pipe_stdout=True)
    )

    process2 = (
        ffmpeg
        .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='1280x720')
        .output(output_file, pix_fmt='yuv420p')
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )

    while True:
        # Read a frame from the input video
        in_bytes = process1.stdout.read(width * height * 3)
        if not in_bytes:
            break
        in_frame = (
            np
            .frombuffer(in_bytes, np.uint8)
            .reshape([height, width, 3])
        )

        # Process the frame with G'MIC diffusion upscale
        gmic_instance = gmic.Gmic()
        out_frame = gmic_instance.run("input %dx%dx3 %s -scale %dx%d -fx_dream_smoothing %d,%f,%d,0" %
                                      (width, height, in_frame, width_new, height_new,
                                       smoothness, anisotropy, sharpness))

        # Handle cropping/padding based on calculated values
        if remove_left >= 0:
            out_frame = out_frame[remove_top:height_new-remove_bottom,
                                  remove_left:width_new-remove_right]
        else:
            pad_left = abs(remove_left)
            pad_right = abs(remove_right)
            pad_top = abs(remove_top)
            pad_bottom = abs(remove_bottom)

            out_frame = np.pad(out_frame, ((pad_top, pad_bottom), (pad_left, pad_right), (0, 0)),
                               mode='constant')

        # Write the processed frame to the output
        process2.stdin.write(
            out_frame
            .astype(np.uint8)
            .tobytes()
        )

    process2.stdin.close()
    process1.wait()
    process2.wait()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python upscale_diffusion_dvd_16_9_to_720p.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    upscale_diffusion_dvd_16_9_to_720p(input_file, output_file)
