# Training Disclosure for moreffmpeg
This Training Disclosure, which may be more specifically titled above here (and in this document possibly referred to as "this disclosure"), is based on **Training Disclosure version 1.1.4** at https://github.com/Hierosoft/training-disclosure by Jake Gustafson. Jake Gustafson is probably *not* an author of the project unless listed as a project author, nor necessarily the disclosure editor(s) of this copy of the disclosure unless this copy is the original which among other places I, Jake Gustafson, state IANAL. The original disclosure is released under the [CC0](https://creativecommons.org/public-domain/cc0/) license, but regarding any text that differs from the original:

This disclosure also functions as a claim of copyright to the scope described in the paragraph below since potentially in some jurisdictions output not of direct human origin, by certain means of generation at least, may not be copyrightable (again, IANAL):

Various author(s) may make claims of authorship to content in the project not mentioned in this disclosure, which this disclosure by way of omission unless stated elsewhere implies is of direct human origin unless stated elsewhere. Such statements elsewhere are present and complete if applicable to the best of the disclosure editor(s) ability. Additionally, the project author(s) hereby claim copyright and claim direct human origin to any and all content in the subsections of this disclosure itself, where scope is defined to the best of the ability of the disclosure editor(s), including the subsection names themselves, unless where stated, and unless implied such as by context, being copyrighted or trademarked elsewhere, or other means of statement or implication according to law in applicable jurisdiction(s).

Disclosure editor(s): Hierosoft LLC

Project author: Hierosoft LLC

This disclosure is a voluntary of how and where content in or used by this project was produced by LLM(s) or any tools that are "trained" in any way.

The main section of this disclosure lists such tools. For each, the version, install location, and a scope of their training sources in a way that is specific as possible.

Subsections of this disclosure contain prompts used to generate content, in a way that is complete to the best ability of the disclosure editor(s).

tool(s) used:
- GPT-4-Turbo (Version 4o, chatgpt.com)

Scope of use: code described in subsections--typically modified by hand to improve logic, variable naming, integration, etc, but in this commit, unmodified.

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

ok now improve the readme and setup.py to indicate the project is called moreffmpeg and the headline should be "Use G'MIC plugins with ffmpeg (finally!) thanks to the wonderful ffmpeg-python and gmic for Python. A useful high level feature ensures correct integer size after float scaling.'

Only online URL is https://github.com/Hierosoft/moreffmpeg, and e-mail is 7557867+poikilos@users.noreply.github.com

explain how to install everything in the readme, using git clone, cd to the project directory I specified, then sudo apt install python3-venv, then python3 -m venv .venv then activate it and install requirements.txt

you keep formatting your output instead of giving me markdown. Try restructured text instead.

Go back to markdown, but put all commands in a row in a code block

rename the upscale_diffusion_dvd_16_9_to_720p function to main with no args, and move all argparse processing to main, so the __main__ case is only sys.exit(main()). Move width_scale=178, height_scale=150,
                                       smoothness=0, anisotropy=0.4, sharpness=21 to a dictionary called gmic_plugin_options.

At the beginning of main, call a get_gmic_commands_txt function that will list all .gmic files in ~/.config/gmic, and return the last modified one. If there are no results, return None. In main, set commands_txt to the value. If the file doesn't exist, show "Warning: Install the gmic package for your distro (or compile & install gmic) then run it at least once to download and generate a gmic commands file such as ~/.config/gmic/update292.gmic." and set commands_txt to a DEFAULT_COMMANDS_TXT global which should be """#@gui Upscale [Diffusion]:fx_upscale_smart,fx_upscale_smart_preview(0)
#@gui :Width=text("200%")
#@gui :Height=text("200%")
#@gui :Smoothness=float(2,0,20)
#@gui :Anisotropy=float(0.4,0,1)
#@gui :Sharpness=float(50,0,100)
#@gui :_=separator()
#@gui :_=note("<small>Author: <i><a href="http://bit.ly/2CmhX65">David Tschumperl&#233;</a></i>.&#160;&#160;&#160;&#160;&#160;&#160;Latest Update: <i>2010/29/12</i>.</small>")
""".

Write a GMICHelp class with a load_commands_txt function. At the beginning of main, set help = GMICHelp(), then call help.load_commands_txt(commands_txt). The method should set a local variable command = None, self.commands = OrderedDict() if self.commands is None, then split the input by newlines, then for each line, see if the line contains "@gui", otherwise continue (short circuit loop). Get all text after that as gui_txt and strip it. If gui_txt does not start with ":", collect the command like self.commands[command.key] if command is not None and set command as a new CommandInfo instance, setting the attributes as follows: assume gui_txt is formatted like "Upscale [Diffusion] : fx_upscale_smart, fx_upscale_smart_preview(0)" in this case, split(":", 1) to only split into 2 parts, and set name to the part before ":" (stripped) then split the second part (after ":") by comma, then set name to the first element (stripped), and the rest of the list can do in a functions attribute. else create option = OptionInfo(), and set its name, type_name (and value_default, value_min, value_max in that order if typeName is neither "text" nor "_bool" nor "separator" nor "note" nor choice), assuming the format of the line can be any of: #@gui : Width = text("200%")
Height = text("200%")
Smoothness = float(2,0,20)
Anisotropy = float(0.4,0,1)
Sharpness = float(50,0,100) url = link("https://thispersondoesnotexist.com/") Update Portrait = button()
sep = separator() choice(2,"Dots","Wireframe","Flat","Flat-Shaded","Gouraud","Phong")
note = note("<small>Author: <i>David Tschumperlé</i>.      Latest Update: <i>2010/29/12</i>.</small>"). If the type is choice, use the first item (2 in that case) as the default_index but do not set default_value, and the rest of the comma-separated values in parenthesis should go in a list called choices and the quotes should be stripped. Also set option.key to name.lower(). Write the OptionInfo class with those attributes, and add this to an ordered dict in the current command: command.options using option.key as the key. if type is float, cast each value in the parenthesis to float, or if int, cast each to int.


In the case of  if not gui_txt.startswith(":"):, the options should not be touched. Instead of options_list = options_txt.split(","), set functions_list = options_txt.split(",") then set key=functions_list[0] and set command.functions = functions_list


Instead of processing for line in commands_txt.splitlines(), directly, iterate a gui_lines list and iterate that instead. To generate it, separate '#@gui ' (be sure to check for a space after gui) lines from other lines otherwise continue (short circuit the loop). Merge the multi-line statements:
  - curly braces:
```
#@gui : Preset = choice{1,"Default (Circle)","Alien Rasta","All Round","Carnivorous Plant","Cat Pad","Flower",
#@gui : "Flower Cushion","Fly Karateka","Hearts","Moving Leaf","Radioactive Flower","Rosace","Spaceship",
#@gui : "Transformer","Tubular Waves","Twisted Heart","Twisted Heart 2","Twisted Tunnel","Waterslide"}
```
    - or:
```
#@gui : note = note{"You must then decompress all files contained in this archive at the following location:\n
#@gui : - for <b>Unix</b>-like systems : <span color="blue"><samp>$HOME/.cache/gmic/</samp></span>\n
#@gui : - for <b>Windows</b> systems : <span color="blue"><samp>%APPDATA%/gmic/</samp></span>
#@gui : "}
```
  - explicit line continuation:
```
#@gui : note = note("<small><b><span color="#FF0055">Note:</span></b> Set <i>Random Seed</i> to <b>0</b> to make it \
# random as well.</small>")
```
  - implicit line continuation:
```
#@gui : note = note("<small><b>Note:</b> This filter proposes a showcase of some interactive demos, all written
#@gui : as G'MIC scripts.</small>")
```

- [ ] For nested quotes, track the quoted or unquoted status by iterating each character, and if unquoted and character is ")", end the string regardless of the number of lines: ```note = note("<center><a href="https://tschumperle.users.greyc.fr/"><img src="data:image/png;base64,iVB
# AnoH9FcRhS6kAAAAAElFTkSuQmCC" />   Sébastien Fourey</a></center>")
``` Combine multiline curly braces the same way as parenthesis. Find either the parenthesis or curly brace, and find end_char like {'(': ")", '{': "}"}[start_char]


To ensure start entry lines are not confused with {  or ( continuations, make a collecting boolean and use that to supercede start entry parsing. If not collecting, check for the start_chart, but instead of looking to see if "(" in line or "{" in line, do it more reliably. Set value = line.split("=", 1)[1]. Use regex to split value further, ending on either "(" or "{" and everything after that is processed in the way I've described to find the closing on that line or a later line.

Now improve get_type using the same search pattern from preprocess_gui_lines  and just return the text, stripped, before ( or {.


Combine the arg extract functions this way: ```    def extract_raw_args_str(self, option_def):
        values = option_def[option_def.index('(')+1:option_def.index(')')].split(',')
        return values

    def extract_raw_args(self, option_def):
        values = self.extract_raw_args_str(options_def).split(',')
        return values

    def extract_float_values(self, option_def):
        return [float(val) for val in self.extract_raw_args(option_def)]

    def extract_int_values(self, option_def):
        return [int(val) for val in self.extract_raw_args(option_def)]

    def extract_choices(self, option_def):
        parts = self.extract_raw_args(options_def)
        default_index = int(parts[0])
        choices = [choice.strip().strip('"') for choice in parts[1:]]
        return choices, default_index``` but improve the extract_raw_args_str function by allowing ( or { like the other regex code we used.


## gmic-external-test
make a python script that ensures the gmic-output directory exists using os.makedirs then iterates i starting at 1, while file exists, and the name is "blues%s.png" % i, & uses the gmic command on each using subprocess Popen. Set sharp_radius=.75,sharp_amount=2,sharp_threshold=1,constrant_radius=5,overshoot=0. The gmic command is to do iain_constrained_sharpen with the args "%s,%s,%s,%s,%s,0,1" and format the string with the values (sharp_radius,sharp_amount,sharp_threshold,constrant_radius,overshoot) and fx_upscale_smart with the args: 170%,150%,1,0,0.4,21 on each image, and save a file of the same name to the gmic-output folder.

For compatibility use a python shebang, from future import print, do not use type hinting, and use percent formatting instead of string interpolation.

Make a varible to control the behavior of the sharpen step called sharpen_order. accept a positional CLI argument using argparse for it as -n or --sharpen-order. If the value is -1 (default), place the sharpen step first in the command, if 1, after the scale step, and if 0, do not add the sharpen filter to the command.

iain_constrained_sharpen. Also, change "170%%,150%%,1,0,0.4,21" to "1280,720,1,0,0.4,21". The gmic command only takes one effect at a time, so you will have to make intermediate files. Make the following functions: fx_upscale_smart(src_file, dst_file) and iain_constrained_sharpen(src_file, dst_file). If the order is -1, call iain_constrained_sharpen and save to a subfolder under output_file in "iain_constrained_sharpen" then use the resulting path to call fx_upscale_smart with the previous destination as the source, and the destination in a folder called "iain_constrained_sharpen+fx_upscale_smart". If the order is 1, call them in the opposite order and use a folder called "fx_upscale_smart" as the destination for upscale, then use that destination as the source for sharpen and use the folder "fx_upscale_smart+iain_constrained_sharpen" as the destination for sharpen.

If sharpen_order is 0, you can use the subfolder "fx_upscale_smart" for that too.

if sharpen_order == -1:, the final file should be placed in "iain_constrained_sharpen+fx_upscale_smart" subfolder.
