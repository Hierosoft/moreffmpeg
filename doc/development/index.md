# ffmpeg-gmic-plus Development

## gmic commands
The only exhaustive list of commands I could find is in [gmic/src/gmic_stdlib.gmic](https://raw.githubusercontent.com/GreycLab/gmic/refs/heads/master/src/gmic_stdlib.gmic).

Ideally this program (or G'MIC...) should parse the gmic file and allow something like `gmic help commands` or `gmic help fx_upscale_smart` or `gmic help upscale_smart`. Example of gmic file content:
```
#@gui Upscale [Diffusion] : fx_upscale_smart, fx_upscale_smart_preview(0)
#@gui : Width = text("200%")
#@gui : Height = text("200%")
#@gui : Smoothness = float(2,0,20)
#@gui : Anisotropy = float(0.4,0,1)
#@gui : Sharpness = float(50,0,100)
#@gui : sep = separator()
#@gui : note = note("<small>Author: <i>David Tschumperlé</i>.      Latest Update: <i>2010/29/12</i>.</small>")
fx_upscale_smart :
  to_rgb upscale_smart $1,$2,1,$3,$4,$5 c 0,255
```
(The GIMP plugin is defined in a SCM file in <https://github.com/GreycLab/gmic/tree/master/src>)

Example `ffmpeg` commands that could be improved with `ffmpeg-gmic`:
```
ffmpeg -threads 0 -analyzeduration 150M -probesize 150M -i input.vob -map 0:v -preset veryslow -vf crop=720:464:0:4,scale=1024:-2:flags=print_info+lanczos+accurate_rnd+full_chroma_int:param0=5,unsharp=7:7:1.0:7:7:0.0,vaguedenoiser=method=1:threshold=4 -profile:v high -level:v 4.0 -vcodec libx264 -crf 22 -tune film -allow_skip_frames 1 -g 120 -bf 0 -pix_fmt yuv420p -x264-params look_ahead_depth=60 -map 0:a:0 -acodec copy output.mkv
ffmpeg -threads 0 -analyzeduration 150M -probesize 150M -i input.vob -map 0:v -preset veryslow -vf crop=720:464:0:4,scale=1024:-2:flags=lanczos:param0=5,unsharp=7:7:1.0:7:7:0.0,vaguedenoiser=method=1:threshold=4 -profile:v high -level:v 4.0 -vcodec libx264 -crf 22 -tune film -allow_skip_frames 1 -g 120 -bf 0 -pix_fmt yuv420p -x264-params look_ahead_depth=60 -map 0:a:0 -acodec copy output.mkv
```

## Example commands
This section provides some examples of commands that should be allowed and passed to `ffmpeg-gmic` after `-vf`.

Based on ffmpeg frei0r syntax `frei0r=filter_name=pixeliz0r:filter_params=0.02|0.02`
and gmic CLI syntax `gmic vlcsnap-2024-10-07-08h23m00s709.png fx_upscale_smart 178%,150%,0,0.4,35 output output_image.png`:
- `-vf "gmic=filter_name=fx_upscale_smart:filter_params=178%|150%|0|0.4|35"`
  - Maybe allow multiple filters like `-vf "gmic=sharpen 1, frei0r=glow:0.5"`

[upscale_smart](https://gmic.eu/reference/upscale_smart.html#top) G'MIC documentation:
- `smart_upscale width[%],_height[%],_depth,_smoothness>=0,_anisotropy=[0,1],sharpening>=0`
  - but you actually have to do `fx_upscale_smart`
- `rescale2d ,100 +upscale_smart 500%,500% append x`
  - but rescale2d is invalid...so see [gmic commands](#gmic-commands) instead.

`gmic help` says:
- `gmic image.jpg denoise 30,10 output denoised.jpg`


## PIL interop
[PIL](https://gmic-py.readthedocs.io/en/latest/PIL.html) gmic-py documentation:
```Python
gmic.GmicImage.from_PIL
gmic.GmicImage.to_PIL
```
