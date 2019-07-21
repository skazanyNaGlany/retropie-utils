#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Just change font size for all RetroPie emulators.


if __name__ != '__main__':
    print('Please run this script standalone.')
    exit(1)


import argparse
import os
import fnmatch
import glob


CONFIGS_PATHNAME = '/retropie/opt/retropie/configs/'


parser = argparse.ArgumentParser(description='Set video font size (for messages using hotkey) for all RetroArch emulators.')
parser.add_argument(
    '-s',
    '--size',
    help='video font size 1 - 40',
    metavar='size',
    nargs=1,
    type=int
)
args = parser.parse_args()


def set_by_file(size, cfg_pathname):
    lines = []
    found_video_font_size = False
    new_video_font_size_entry = 'video_font_size = "{}.000000"'.format(size)

    for iline in open(cfg_pathname).read().split('\n'):
        iline = iline.strip()

        if iline.find('video_font_size = "') == 0:
            found_video_font_size = True
            lines.append(new_video_font_size_entry)

            continue

        lines.append(iline)

    if not found_video_font_size:
        return False

    with open(cfg_pathname, 'w') as f:
        for iline2 in lines:
            f.write(iline2 + '\n')

    return True


def set_by_size(size):
    some_changed = False

    for dirpath, dirnames, files in os.walk(CONFIGS_PATHNAME):
        for name in files:
            if name == 'retroarch.cfg':
                cfg_pathname = os.path.join(dirpath, name)

                if set_by_file(size, cfg_pathname):
                    print('Changed in ' + cfg_pathname)
                    some_changed = True

    return some_changed


if args.size:
    size = int(args.size[0])

    if size < 1 or size > 40:
        print('Font size must be 1 - 40')
        exit(1)

    if set_by_size(size):
        print('Reboot RetroPie to apply changes.')
    else:
        print('No changes (retroarch.cfg files not found in ' + CONFIGS_PATHNAME + ' ?)')
else:
    parser.print_help()

exit(0)
