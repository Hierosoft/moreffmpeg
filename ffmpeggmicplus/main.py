from __future__ import print_function

import argparse
import ffmpeg
import glob
import gmic
import os
import numpy as np
import sys

from collections import OrderedDict
from datetime import datetime

gmic_help = None

DEFAULT_COMMANDS_TXT = """#@gui Upscale [Diffusion]:fx_upscale_smart,fx_upscale_smart_preview(0)
#@gui :Width=text("200%")
#@gui :Height=text("200%")
#@gui :Smoothness=float(2,0,20)
#@gui :Anisotropy=float(0.4,0,1)
#@gui :Sharpness=float(50,0,100)
#@gui :_=separator()
#@gui :_=note("<small>Author: <i><a href='http://bit.ly/2CmhX65'>David Tschumperl&#233;</a></i>.&#160;&#160;&#160;&#160;&#160;&#160;Latest Update: <i>2010/29/12</i>.</small>")
"""

# Default G'MIC plugin options
gmic_plugin_options = {
    'width_scale': 178,
    'height_scale': 150,
    'smoothness': 0,
    'anisotropy': 0.4,
    'sharpness': 21,
}


class OptionInfo:
    def __init__(self, name, type_name, value_default=None, value_min=None, value_max=None, choices=None):
        self.name = name
        self.type_name = type_name
        self.value_default = value_default
        self.value_min = value_min
        self.value_max = value_max
        self.choices = choices


class CommandInfo:
    def __init__(self, key):
        self.key = key
        self.functions = []  # Store functions as a list
        self.options = OrderedDict()


class GMICHelp:
    def __init__(self):
        self.commands = OrderedDict()

    def preprocess_gui_lines(self, commands_txt):
        """Preprocess the commands_txt to extract and merge #@gui lines."""
        gui_lines = []
        current_line = ""
        collecting = False

        inside_quotes = False
        start_char = None
        end_char = None

        for line in commands_txt.splitlines():
            line = line.strip()

            if not line.startswith("#@gui "):
                continue  # Only process lines starting with '#@gui '

            # Extract the value after the equals sign, and determine if we should start collecting
            if not collecting:
                # Extract the value after the equals sign
                if '=' in line:
                    value = line.split('=', 1)[1].strip()

                    # Use regex to check for the start of a multiline construct
                    if re.search(r'(\(|\{)', value):
                        start_char = re.search(r'(\(|\{)', value).group(1)
                        end_char = {'(': ')', '{': '}'}[start_char]
                        collecting = True  # Start collecting lines
                    current_line = line  # Start accumulating the line
                else:
                    current_line = line  # Regular line without collecting
            else:
                current_line += line  # Append this line to the current entry

            # Track quoted status while iterating through the characters
            inside_quotes = self.track_quoted_status(current_line, inside_quotes)

            # If we're collecting and find the closing character, stop collecting
            if collecting and end_char in current_line and not inside_quotes:
                collecting = False
                gui_lines.append(current_line)  # Add the complete entry to gui_lines
                current_line = ""  # Reset for the next line

        return gui_lines

    def track_quoted_status(self, line, inside_quotes):
        """Track whether we are inside quotes based on encountering quotes in the line."""
        in_quotes = inside_quotes
        for char in line:
            if char == '"':
                in_quotes = not in_quotes
        return in_quotes

    def load_commands_txt(self, commands_txt):
        command = None

        # Split the input by newlines
        for line in self.preprocess_gui_lines():
            line = line.strip()
            if "@gui" not in line:
                continue

            gui_txt = line.split("@gui", 1)[-1].strip()

            if not gui_txt.startswith(":"):
                # Extract command name and functions
                name, options_txt = gui_txt.split(":", 1)
                name = name.strip()
                functions_list = options_txt.split(",")

                command = CommandInfo(key=name.lower())
                command.functions = functions_list  # Set functions instead of options
                self.commands[command.key] = command
            else:
                # Process options
                option_line = gui_txt[1:].strip()  # Skip the colon
                option_parts = option_line.split("=")
                option_name = option_parts[0].strip()
                option_def = option_parts[1].strip() if len(option_parts) > 1 else None

                if option_def:
                    option = OptionInfo(name=option_name.lower(), type_name=self.get_type(option_def))
                    if option.type_name == "float":
                        values = self.extract_float_values(option_def)
                        option.value_default = values[0]
                        option.value_min = values[1]
                        option.value_max = values[2]
                    elif option.type_name == "int":
                        values = self.extract_int_values(option_def)
                        option.value_default = values[0]
                        option.value_min = values[1]
                        option.value_max = values[2]
                    elif option.type_name == "choice":
                        option.choices, option.value_default = self.extract_choices(option_def)
		    else:
			option.value =
                    command.options[option.key] = option

    def get_type(self, option_def):
        """Extract the type name from the option definition using regex.

	Return:
	    str: Return the part before the first parenthesis or curly
	        brace, stripped of spaces
	"""
        # Use regex to find either '(' or '{' to split the string:
        match = re.split(r'(\(|\{)', option_def.strip(), 1)
        if match:
            return match[0].strip()
        return None

    def extract_raw_args_str(self, option_def):
        """Extract the raw arguments string, handling both () and {}."""
        # Use regex to capture values inside the first set of parentheses or curly braces
        match = re.search(r'\(([^)]*)\)|\{([^}]*)\}', option_def)
        if match:
            # Extract the matched group (either parentheses or curly braces)
            return match.group(1) if match.group(1) else match.group(2)
        return None

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
        return choices, default_index


def get_gmic_commands_txt():
    gmic_dir = os.path.expanduser("~/.config/gmic")
    gmic_files = glob.glob(os.path.join(gmic_dir, "*.gmic"))

    if not gmic_files:
        return None

    # Get the last modified file
    latest_file = max(gmic_files, key=os.path.getmtime)
    return latest_file


def main():
    global gmic_help

    commands_txt = get_gmic_commands_txt()

    if commands_txt is None or not os.path.exists(commands_txt):
        print("Warning: Install the gmic package for your distro (or compile & install gmic) then run it at least once to download and generate a gmic commands file such as ~/.config/gmic/update292.gmic.")
        commands_txt = DEFAULT_COMMANDS_TXT
    else:
	gmic_help = GMICHelp()
	gmic_help.load_commands_txt(commands_txt)

    # Continue with the rest of your FFmpeg addon logic here...
    print("Using commands file:", commands_txt)

    parser = argparse.ArgumentParser(
        description="Upscale a 16:9 DVD video to 1280x720 using G'MIC."
    )
    parser.add_argument("-i", help="Input video file")
    parser.add_argument("-o", help="Output video file")
    parser.add_argument(
        "--width_scale", type=int, default=gmic_plugin_options['width_scale'],
        help="Percentage to upscale width, such as 720*1.78=1282, cropped to 1280 (default: %s)" % gmic_plugin_options['width_scale']
    )
    parser.add_argument(
        "--height_scale", type=int, default=gmic_plugin_options['height_scale'],
        help="Percentage to upscale height, such as 150 for 480*1.5=720 (default: %s)" % gmic_plugin_options['height_scale']
    )
    parser.add_argument(
        "--smoothness", type=int, default=gmic_plugin_options['smoothness'],
        help="Smoothness level for G'MIC processing (default: %s)" % gmic_plugin_options['smoothness']
    )
    parser.add_argument(
        "--anisotropy", type=float, default=gmic_plugin_options['anisotropy'],
        help="Anisotropy level for G'MIC processing (default: %s)" %  % gmic_plugin_options['anisotropy']
    )
    parser.add_argument(
        "--sharpness", type=int, default=gmic_plugin_options['sharpness'],
        help="Sharpness level for G'MIC processing (default: %s)" % gmic_plugin_options['sharpness']
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
        gmic_command = "fx_upscale_smart %d,%d,%d,%0.2f,%d" % (
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
