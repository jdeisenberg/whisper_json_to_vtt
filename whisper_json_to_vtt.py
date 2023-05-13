#
#	Given the output from whisper with word_timestamps set to True,
#	create a VTT file with a given number of characters per line.
#
#	Thanks to rBrenick for this gist: https://gist.github.com/rBrenick/fcb8d07ecaa55856ecd9745ecfd29341
#	which gave me most of the argument parsing code.

import sys
import json
import re
import argparse

def add_timing(vtt_list, start_time, end_time, text):
    vtt_list.append({
        "start": start_time,
        "end": end_time,
        "text": text})

def create_vtt_list(json_dict, max_line_length):
    vtt_list = []
    segment_list = json_dict.get("segments", {})
    for segment in segment_list:
        text = segment.get("text", "").strip()
        if len(text) <= max_line_length:
            add_timing(vtt_list, segment.get("start"), segment.get("end"), text)
        else:
            current_length = 0
            current_text = ""
            current_start_time = segment.get("start")
            words_list = segment.get("words", [])

            for word_dict in words_list:
                one_word = word_dict.get("word", "")
                if len(one_word) + current_length > max_line_length:
                    # if we have something to emit, emit it...
                    if current_length > 0:
                        add_timing(vtt_list, current_start_time, current_end_time,
                                   current_text)
                    current_text = one_word
                    current_length = len(one_word)
                    current_start_time = word_dict.get("start")
                    current_end_time = word_dict.get("end")
                else:
                    current_text += one_word
                    current_length += len(one_word)
                    current_end_time = word_dict.get("end")

            # Take care of anything left over...
            if current_length > 0:
                add_timing(vtt_list, current_start_time, current_end_time, current_text)

    return vtt_list

def munge_time(seconds_str):
    """Given a string with a number of seconds, convert
    to a string in form hh:mm:ss.sss
    """
    total_seconds = float(seconds_str)
    hours = int(total_seconds // 3600)
    min_left = total_seconds % 3600
    minutes = int(min_left // 60)
    seconds = min_left % 60
    return f'{hours:02d}:{minutes:02d}:{seconds:06.3f}'

def emit_vtt_file(vtt_list, output_file_name):
    output_file = open(output_file_name, 'w')
    output_file.write('''WEBVTT
Kind: captions
Language: en
##\n\n''')
    for item in vtt_list:
        # 00:00:00.240 --> 00:00:03.200
        # Let’s discuss the print() function in Python.
        start = munge_time(item.get('start'))
        end = munge_time(item.get('end'))
        output_file.write(f'{start} --> {end}\n')
        output_file.write(f"{item.get('text').strip()}\n\n")

    output_file.close()



def optional_int(string):
    return None if string == "None" else int(string)

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("json_file", type=str, help=".json file to convert to VTT")
    parser.add_argument("--output_file", "-o", type=str, default="", help="output file, if empty will change extension to .vtt")
    parser.add_argument("--max_line_length", type=optional_int, default=42, help="max number of characters for a line in the subtitle files")

    args = parser.parse_args().__dict__
    
    input_file_name = args.get("json_file")
    max_line_length = args.get("max_line_length")

    if args.get("output_file"):
        output_file_name = args.get("output_file")
    else:
        output_file_name = re.sub(r"\.(\w+)$", ".vtt", input_file_name)

    try:
        input_file = open(input_file_name, 'r')
        json_dict = json.loads(input_file.read())

        vtt_list = create_vtt_list(json_dict, max_line_length);
        emit_vtt_file(vtt_list, output_file_name)
        
    except FileNotFoundError:
        print(f'Unable to open {input_file_name}; file not found.')
    
main()
