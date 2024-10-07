# ffmpeg-gmic-plus Development

## gmic commands
The only exhaustive list of commands I could find is in [gmic/src/gmic_stdlib.gmic](https://raw.githubusercontent.com/GreycLab/gmic/refs/heads/master/src/gmic_stdlib.gmic).

Ideally this program (or G'MIC...) should parse the gmic file and allow something like `gmic help commands`. Example of gmic file content:

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

## Example commands
This section provides some examples of commands that should be allowed and passed to `ffmpeg-gmic` after `-vf`.

[upscale_smart](https://gmic.eu/reference/upscale_smart.html#top) G'MIC documentation:
- `smart_upscale width[%],_height[%],_depth,_smoothness>=0,_anisotropy=[0,1],sharpening>=0`
- `rescale2d ,100 +upscale_smart 500%,500% append x`

`gmic help`:
- `gmic image.jpg denoise 30,10 output denoised.jpg`
- rescale2d ,100 +upscale_smart 500%,500%
  - but rescale2d is invalid...
    See [gmic commands](#gmic-commands) instead.

## PIL interop
[PIL](https://gmic-py.readthedocs.io/en/latest/PIL.html) gmic-py documentation:
```Python
gmic.GmicImage.from_PIL
gmic.GmicImage.to_PIL
```
