#!/usr/bin/env python3

import os
from argparse import ArgumentParser
from sys import exit  # exit randomly fails on winblows without this.

OFFSET = 17
SEPARATOR = chr(15)  # ASCII SI (shift in) (separator after shifting by offset)
WINBLOWS_EOL = b'\x0D\x0A'  # ASCII CR LF

# Box drawing characters from https://www.compart.com/en/unicode/block/U+2500
SEP_HOR = '━'
SEP_VERT = '┃'
SEP_CROSS = '╋'

HEADER_WORD = 'Word'
HEADER_MATCH_TYPE = 'Match type'
HEADER_REPLACE = 'Mask word'

MATCH_TYPE_P = 'Partial'
MATCH_TYPE_F = 'Full'

ENCODED_FILENAME = 'filter.FTR'
DECODED_FILENAME = 'filter.FTR_decoded.txt'
VALID_FILE_EXTENSIONS = {'encoded': ENCODED_FILENAME[-4:].upper(), 'decoded': DECODED_FILENAME[-4:].upper()}

# Unchanged as of 1.05E to 3.8
VANILLA_FILTER_FILE_BYTES = (
    b'r\x84\x84y\x80}v \x81 y~~\r\nr\x84\x84yvru \x81 y~~\r\nr\x83\x84v w y~~\r\nr\x83\x84vy\x80}v \x81 y~~\r\nr\x83'
    b'\x84vyvru \x81 y~~\r\nr\x7fr} w y~~\r\ns\x86\x85\x85 w y~~\r\ns\x86\x85\x85yvru w y~~\r\ns\x86\x85\x85\x80t| \x81'
    b' y~~\r\nsz\x85ty \x81 y~~\r\nsr\x84\x85r\x83u \x81 y~~\r\nsr}\x80\x7f\x8a\x81\x80\x7f\x8a \x81 y~~\r\nsr}}\x84 w '
    b'y~~\r\ns\x80\x7fv\x83 \x81 y~~\r\ns}\x80\x88{\x80s \x81 y~~\r\ns\x80}}\x80t|\x84 \x81 y~~\r\ns\x80}}\x80\x89 \x81'
    b' y~~\r\nsv}}v\x7fu \x81 y~~\r\nsr\x7fuz\x85 \x81 y~~\r\nt\x86\x7f\x85 \x81 y~~\r\nt\x86\x7f\x7f\x8a \x81 y~~\r\nt'
    b'\x83\x80t| \x81 y~~\r\nt\x80t| \x81 y~~\r\nt\x83r\x81 \x81 y~~\r\nt}vr\x87rxv \x81 y~~\r\nt}z\x85 \x81 y~~\r\nt'
    b'\x80\x80\x8bv \x81 y~~\r\nt}vw\x85 \x81 y~~\r\nt}z~r\x89 \x81 y~~\r\nuzt| \x81 y~~\r\nuz\x83\x85s\x80\x89 \x81 y~'
    b'~\r\nuz}u\x80 \x81 y~~\r\nu\x8a|v \x81 y~~\r\nw\x83zx \x81 y~~\r\nw\x86t| \x81 y~~\r\nw\x86t| w }\x80\x87v\r\nwr'
    b'\x7f\x7f\x8a \x81 y~~\r\nwr\x83\x85 \x81 y~~\r\nw}r\x81 \x81 y~~\r\nwv}ty \x81 y~~\r\nx\x86\x84\x84v\x85 \x81 y~~'
    b'\r\nx\x80ss}v \x81 y~~\r\nxr\x84y \x81 y~~\r\ny\x80\x83\x7f\x8a \x81 y~~\r\ny\x80\x7f|\x8a \x81 y~~\r\ny\x80\x80'
    b'\x85v\x83\x84 \x81 y~~\r\ny\x80\x7fv\x8a\x81\x80\x85 \x81 y~~\r\nyr~\x84yr\x7f| \x81 y~~\r\nyrz\x83\x81zv \x81 y~'
    b'~\r\n{v\x83|\x80ww \x81 y~~\r\n{z\x8b\x8b \x81 y~~\r\n{rt|\x80ww \x81 y~~\r\n{\x86\x7f|zv \x81 y~~\r\n{rz}srz\x85'
    b' \x81 y~~\r\n|\x7f\x80s \x81 y~~\r\n}\x80\x87v~z}| \x81 y~~\r\n}\x80\x87v\x85\x83\x86\x7ftyv\x80\x7f \x81 y~~\r\n'
    b'}\x80\x87v\x85\x86\x7f\x7fv} \x81 y~~\r\n~z\x7fxv \x81 y~~\r\n~\x80\x85\x85 \x81 y~~\r\n~\x86ww \x81 y~~\r\n\x7f'
    b'\x80styvv\x84v \x81 y~~\r\n\x7f\x80s\x8avr\x84\x85 \x81 y~~\r\n\x7f\x80\x7ftv \x81 y~~\r\n\x7fzxxv\x83 \x81 y~~\r'
    b'\n\x7fz\x81\x81}v \x81 y~~\r\n\x7f\x80\x83|\x84 \x81 y~~\r\n\x80\x83zwztv \x81 y~~\r\n\x80\x83r} \x81 y~~\r\n\x81'
    b'\x83zt| \x81 y~~\r\n\x81\x80\x7ftv \x81 y~~\r\n\x81\x86\x84\x84\x8a \x81 y~~\r\n\x81\x80\x80\x7f\x85r\x7fx \x81 y'
    b'~~\r\n\x81v\x7fz\x84 \x81 y~~\r\n\x81vv\x81vv \x81 y~~\r\n\x81z\x84\x84 \x81 y~~\r\n\x81z~\x81 \x81 y~~\r\n\x81'
    b'\x80\x83|\x84\x88\x80\x83u \x81 y~~\r\n\x83vt\x85\x86~ \x81 y~~\r\n\x83z\x7fx\x81zvtv \x81 y~~\r\n\x83vt\x85r} '
    b'\x81 y~~\r\n\x84\x7fr\x85ty \x81 y~~\r\n\x84yz\x85 \x81 y~~\r\n\x84}z\x85 \x81 y~~\r\n\x84~\x86\x85 \x81 y~~\r\n'
    b'\x84t\x86~ \x81 y~~\r\n\x84\x81\x86\x7f| \x81 y~~\r\n\x84\x81r\x7f| \x81 y~~\r\n\x84\x81\x86\x83\x85 \x81 y~~\r\n'
    b'\x84}r\x84y \x81 y~~\r\n\x85\x86\x83u \x81 y~~\r\n\x85\x80\x84\x84 \x81 y~~\r\n\x85\x88r\x85 \x81 y~~\r\n\x86\x83'
    b'v\x85y\x83r \x81 y~~\r\n\x86\x83z\x7fv \x81 y~~\r\n\x87rxz\x7fr \x81 y~~\r\n\x87ruxv \x81 y~~\r\n\x88r\x7f| \x81 '
    b'y~~\r\n\x88v}}y\x86\x7fx \x81 y~~\r\n\x88vv\x88vv \x81 y~~\r\n\x88r\x83v\x8b \x81 y~~\r\nD}DD\x85 \x81 y~~\r\n'
)


def parse_ftr(encoded_filepath):
    """Read lines from an FTR filterlist file and split the 3 parts using the SEPARATOR const. Deobfuscate characters by
       decrementing each chars byte value based on the OFFSET const. Apply pretty table formatting using the SEP consts.
       Convert match type letters to more obvious long form in the MATCH_TYPE consts."""
    with open(encoded_filepath, 'rb') as f:
        encoded_lines = f.read().splitlines()

    decoded_lines = []
    for line in encoded_lines:
        word, match_type, replace = ''.join([chr(c - OFFSET) for c in line]).split(SEPARATOR)
        if match_type == 'p':
            match_type = MATCH_TYPE_P
        elif match_type == 'f':
            match_type = MATCH_TYPE_F
        decoded_lines.append({'word': word, 'match_type': match_type, 'replace': replace})

    word_col_len = max(len(HEADER_WORD), max(len(line['word']) for line in decoded_lines))
    match_type_col_len = max(len(HEADER_MATCH_TYPE), len(MATCH_TYPE_F), len(MATCH_TYPE_P))
    replace_col_len = len(HEADER_REPLACE)

    output_lines = [
        '{} {sep} {} {sep} {}'.format(
            HEADER_WORD.ljust(word_col_len),
            HEADER_MATCH_TYPE.ljust(match_type_col_len),
            HEADER_REPLACE,
            sep=SEP_VERT),
        '{}{sep}{}{sep}{}'.format(
            SEP_HOR * word_col_len,
            SEP_HOR * match_type_col_len,
            SEP_HOR * replace_col_len,
            sep=SEP_HOR + SEP_CROSS + SEP_HOR)
    ]
    for line in decoded_lines:
        output_lines.append('{} {sep} {} {sep} {}'.format(
            line['word'].ljust(word_col_len),
            line['match_type'].ljust(match_type_col_len),
            line['replace'],
            sep=SEP_VERT)
        )
    return output_lines


def parse_txt(plaintext_filepath):
    """Read lines from a plaintext filter list file but skip header. Split into the 3 parts based on the SEP_VERT const
       and strip and leading or trailing whitespace. Convert match type strings into match type letters. Join parts on
       the SEPARATOR const. Obfuscate characters by incrementing each chars byte value based on the OFFSET const. """
    with open(plaintext_filepath, 'rt') as f:
        lines = f.read().splitlines()

    output_lines = []
    for line in lines[2:]:  # skip header / first 2 lines
        word, match_type, replace = (x.strip() for x in line.split(SEP_VERT))
        match_type = 'p' if match_type == MATCH_TYPE_P else 'f'
        output_line = bytearray(SEPARATOR.join((word, match_type, replace)), 'UTF8')
        output_lines.append(bytes([b+OFFSET for b in output_line]))
    return output_lines


def main():
    """Use argparse to get the launch arguments and carry out the requested action. Validate manual input and require
       clobbering to be explicit. Write parsed lines to appropriate output file and remove input file. If --restore
       is set write a vanilla restore file to specified path and exit."""
    parser = ArgumentParser(description='WAFLCD (Worms Armageddon Filter List CoDec). A tool to encode and decode the'
                                        ' filter.FTR file of Worms Armageddon to allow it to be read and customized.')
    parser.add_argument('--force', action='store_true', help='Allows overwriting files. Default is to quit.')
    parser.add_argument('-o', '--out-file', nargs='?', type=str, default=None, metavar='output file path',
                        help='Output file path. Default depends on input file\'s file extension.'
                             ' For {VFEE} it will be "{DF}" and for {VFED} it will be "{EF}"'.format(
                                 VFEE=VALID_FILE_EXTENSIONS['encoded'],
                                 DF=DECODED_FILENAME,
                                 VFED=VALID_FILE_EXTENSIONS['decoded'],
                                 EF=ENCODED_FILENAME))
    parser.add_argument('--restore', action='store_true',
                        help='Output a vanilla filter.FTR file. Useful if you mess up or want to restore defaults.'
                             ' Specify target with --out-file. Will fail if not set. --force required to overwrite.')
    parser.add_argument('filter_path', default=None, nargs='?', type=str, metavar='filter file path',
                        help='Path to an encoded or decoded filter list file. Type determined by file extension.'
                             ' Will be removed if output file is written successfully to allow easy toggling of type.')
    args = parser.parse_args()

    if args.restore:
        if not args.out_file:
            parser.error('Output file not set.')
        if os.path.isfile(args.out_file) and not args.force:
            parser.error('Output file exists but force overwrite is not set.')
        with open(args.out_file, 'wb') as f:
            f.write(VANILLA_FILTER_FILE_BYTES)
        print('Vanilla filter file written.')
        exit(0)

    if args.filter_path:
        input_ext = args.filter_path[-4:].upper()
    else:
        parser.error('No filter file specified.')
    if not os.path.isfile(args.filter_path):
        parser.error('Specified filter file not found.')
    if input_ext not in VALID_FILE_EXTENSIONS.values():
        parser.error('Specified filter file has invalid extension. Must be: {}'.format(
            ' or '.join(VALID_FILE_EXTENSIONS.values())))
    if not args.out_file:
        os.chdir(os.path.dirname(args.filter_path))
        args.out_file = DECODED_FILENAME if input_ext == VALID_FILE_EXTENSIONS['encoded'] else ENCODED_FILENAME
    if os.path.isfile(args.out_file) and not args.force:
        parser.error(f'Output file "{args.out_file}" exists but force overwrite is not set.')

    if input_ext == VALID_FILE_EXTENSIONS['encoded']:
        output_lines = parse_ftr(args.filter_path)
        output_file = open(args.out_file, 'wt')
        eol = '\n'
    else:
        output_lines = parse_txt(args.filter_path)
        output_file = open(args.out_file, 'wb')
        eol = WINBLOWS_EOL

    output_file.write(eol.join(output_lines))
    output_file.write(eol)
    output_file.close()

    print('Output file written successfully. Removing input file.')
    os.remove(args.filter_path)
    print('Removed successfully. Conversion completed.')


if __name__ == '__main__':
    main()
