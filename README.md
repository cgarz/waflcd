# WAFLCD (Worms Armageddon Filter List CoDec)
## A tool to encode and decode the filter.FTR file of Worms Armageddon to allow it to be read and customized.

By default when online on WormNET with Worms Armageddon certain words are filtered. The filter file in Worms Armageddon is stored at `<install dir>/DATA/filter.FTR`. This file is obfuscated using a simple ascii caesar cipher with shift offset 17. This tool converts between that format and a simple text file formatted into a table with unicode block characters to make it pretty. This text file can then be easily viewed and edited with any text editor.

The format of the file after shifting the bytes by the offfset is:  
`WORD (SI) MATCH TYPE (SI) MASK WORD`  
SI is the ASCII shift in character. Decimal 15 or hexadecimal 0F.

Match type will be `p` or `f`. Which means partial or full.  
If full, then the word will be replaced with the mask word.  
If partial, then each character will be replaced with an asterix, regardless of whether or not it is a word on its own or within another word.


### basic usage:
Simply drag filter.FTR or a decoded filter file onto waflcd.py or waflcd.exe to convert it between the two.  
(The compiled waflcd.exe is in releases. It is created with PyInstaller.)

### command line usage:
waflcd.py [-h] [--force] [-o [output file path]] [--restore] [filter file path]

required positional argument:

Path to an encoded or decoded filter list file. Type determined by file extension. Will be removed if output file is written successfully to allow easy toggling of type.

optional arguments:
* -h, --help  
  show this help message and exit
* --force  
  Allows overwriting files. Default is to quit.
* -o [output file path], --out-file [output file path]  
  Output file path. Default depends on input file's file extension. For .FTR it will be "filter.FTR_decoded.txt" and for .TXT it will be "filter.FTR"
* --restore  
  Output a vanilla filter.FTR file. Useful if you mess up or want to restore defaults. Specify target with --out-file. Will fail if not set. --force required to overwrite.

The tool is written for python 3 and requires at least python 3.6 to run due to the use of an f-string.
