# ffmpeg-gmic-plus
Use G\'MIC plugins with ffmpeg (finally!) thanks to the wonderful
ffmpeg-python and gmic for Python.

## Overview

**ffmpeg-gmic-plus** is a Python library that allows you to
utilize G\'MIC plugins with FFmpeg in a straightforward and efficient
manner. It leverages ffmpeg-python and gmic
to perform high-quality image and video processing, specifically
designed to upscale video using G\'MIC\'s powerful diffusion algorithm.

This project provides a convenient way to upscale videos to a 720p
resolution while maintaining the correct aspect ratio, ensuring the
final output meets your requirements.

## Features

- Utilize G\'MIC\'s diffusion upscale directly within FFmpeg.
- Automatically crop or pad the video to achieve a final resolution of
  1280x720.
- Adjustable parameters for upscaling, including width scale, height
  scale, smoothness, anisotropy, and sharpness.

## Installation
```bash
git clone https://github.com/Hierosoft/ffmpeg-gmic-plus.git
cd ffmpeg-gmic-plus
sudo apt install python3-venv
python3 -m venv .venv
source .venv/bin/activate  # For Linux and macOS
# .venv\Scripts\activate    # For Windows
pip install -r requirements.txt
```


## Usage

To upscale a video, run the following command:

```bash
python upscale_diffusion_dvd_16_9_to_720p.py <input_file> <output_file>
```

### Example

```bash
python upscale_diffusion_dvd_16_9_to_720p.py input_video.mp4 output_video.mp4
```

This command will read [input_video.mp4]{.title-ref}, apply the G\'MIC
diffusion upscale, and write the result to
[output_video.mp4]{.title-ref}.

# Parameters

The [upscale_diffusion_dvd_16_9\_to_720p]{.title-ref} function accepts
the following optional parameters:

- `width_scale`: Percentage to upscale width (default: 178)
- `height_scale`: Percentage to upscale height (default: 150)
- `smoothness`: Smoothness level for G\'MIC processing (default: 0)
- `anisotropy`: Anisotropy level for G\'MIC processing (default: 0.4)
- `sharpness`: Sharpness level for G\'MIC processing (default: 21)

## Contributing

Contributions are welcome! Feel free to open issues or submit pull
requests for improvements or new features.

See also [doc/development/index.md](doc/development/index.md)

## License

See [license.txt](license.txt)
