# whisper_json_to_vtt
Convert Whisper AI word by word JSON to VTT file with a user-specified max line length.

If you create a JSON file with word-by-word data, with a command like this:

```
whisper --language=en --word_timestamps=True --output_format=json videofile.mp4
```

You can then generate a VTT file with a specific maximum line length for the
captions:


```
usage: whisper_json_to_vtt.py [-h] [--output_file OUTPUT_FILE] [--max_line_length MAX_LINE_LENGTH] json_file

positional arguments:
  json_file             .json file to convert to VTT

options:
  -h, --help            show this help message and exit
  --output_file OUTPUT_FILE, -o OUTPUT_FILE
                        output file, if empty will change extension to .vtt (default: )
  --max_line_length MAX_LINE_LENGTH
                        max number of characters for a line in the subtitle files (default: 42)
```
