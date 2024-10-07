# Training Disclosure for ffmpeg-gmic-plus
This Training Disclosure, which may be more specifically titled above here (and in this disclosure possibly referred to as "this disclosure"), is based on Training Disclosure version 1.0.0 at https://github.com/Hierosoft/training-disclosure by Jake Gustafson. Jake Gustafson is probably *not* an author of the project unless listed as a project author, nor necessarily the disclosure editor(s) of this copy of the disclosure unless this copy is the original which among other places I, Jake Gustafson, state IANAL. The original disclosure is released under the [CC0](https://creativecommons.org/public-domain/cc0/) license, but regarding any text that differs from the original:

This disclosure also functions as a claim of copyright to the scope described in the paragraph below since potentially in some jurisdictions output not of direct human origin, by certain means of generation at least, may not be copyrightable (again, IANAL):

Various author(s) may make claims of authorship to content in the project not mentioned in this disclosure, which this disclosure by way of omission implies unless stated elsewhere is of direct human origin to the best of the disclosure editor(s) ability. Additionally, the project author(s) hereby claim copyright and claim direct human origin to any and all content in the subsections of this disclosure itself, where scope is defined to the best of the ability of the disclosure editor(s), including the subsection names themselves, unless where stated, and unless implied such as by context, being copyrighted or trademarked elsewere, or other means of statement or implication according to law in applicable jurisdiction(s).

Disclosure editor(s): Hierosoft LLC

Project author: Hierosoft LLC

This document is a voluntary of how and where content in or used by this project was produced by LLM(s) or any tools that are "trained" in any way.

The main section of this document lists such tools. For each, the version, install location, and a scope of their training sources in a way that is specific as possible.

Subsections of this document contain prompts used to generate content, in a way that is complete to the best ability of the disclosure editor(s).

tool(s) used:
- GPT-4-Turbo (Version 4o, chatgpt.com)

Scope of use: code described in subsections--typically modified by hand to improve logic, variable naming, integration, etc, but unmodified in this commit.

## upscale_diffusion_dvd_16_9_to_720p
Use ffmpeg-python from pip, then use the "gmic" python module as well, and make an example ffmpeg-python script called upscale_diffusion_dvd_16_9_to_720p that performs gmic diffusion upscale with 178% width, 150% height, smoothness 0, anisotropy .4, sharpness 21. These are defaults. Program the ffmpeg-python filter to accept arguments for these settings. The diffusion upscale will change the size of the image, so to make it exactly 1280x720, crop the video using remove_left=int((width-1280)/2) remove_right=(width-1280)-remove_left. If remove amounts are negative, add that much (absolute value) of padding on each side, otherwise crop by those amounts. Before and after this process you will have to get image data from ffmpeg-python, feed it to gmic module, use gmic to edit it, then transfer it back to ffmpeg python. Maybe make functions to ffmpeg_to_gmic and gmic_to_ffmpeg before and after the operation respectively, to transfer image data between ffmpeg-python and gmic. Make a readme with an explanation of the project and an examples section with an example command using the feature. Make a setup.py with the requirements and relevant classifiers, as well as a requirements.txt file.

The data formats appear to be very easy to transfer so do not use ffmpeg_to_gmic or gmic_to_ffmpeg


You don't seem to be quite getting it. You are using ffmpeg's scale but should use gmic's scale as I described. Here is an example of decoding, modifying a frame with tensorflow (but you need to use gmic for that step instead):
```process1 = (
    ffmpeg
    .input(in_filename)
    .output('pipe:', format='rawvideo', pix_fmt='rgb24', vframes=8)
    .run_async(pipe_stdout=True)
)

process2 = (
    ffmpeg
    .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
    .output(out_filename, pix_fmt='yuv420p')
    .overwrite_output()
    .run_async(pipe_stdin=True)
)

while True:
    in_bytes = process1.stdout.read(width * height * 3)
    if not in_bytes:
        break
    in_frame = (
        np
        .frombuffer(in_bytes, np.uint8)
        .reshape([height, width, 3])
    )

    # See examples/tensorflow_stream.py:
    out_frame = deep_dream.process_frame(in_frame)

    process2.stdin.write(
        out_frame
        .astype(np.uint8)
        .tobytes()
    )

process2.stdin.close()
process1.wait()
process2.wait()
```


For compatibility, use from __future__ import print_function and use percent sign formatting instead of str interpolation

ok now improve the readme and setup.py to indicate the project is called ffmpeg-gmic-plus and the headline should be "Use G'MIC plugins with ffmpeg (finally!) thanks to the wonderful ffmpeg-python and gmic for Python. A useful high level feature ensures correct integer size after float scaling.'

Only online URL is https://github.com/Hierosoft/ffmpeg-gmic-plus, and e-mail is 7557867+poikilos@users.noreply.github.com

explain how to install everything in the readme, using git clone, cd to the project directory I specified, then sudo apt install python3-venv, then python3 -m venv .venv then activate it and install requirements.txt

you keep formatting your output instead of giving me markdown. Try restructured text instead.

Go back to markdown, but put all commands in a row in a code block






