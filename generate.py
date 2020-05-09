#!/usr/bin/env python3

import re
import subprocess
from pathlib import Path
from jinja2 import Template


# -------------------------------------------------------------------
def screen_count():
    return int(subprocess.check_output('xrandr | grep " connected " | wc -l', shell=True).decode('utf-8'))


# -------------------------------------------------------------------
def load_base16():
    xdefaults_file = Path.home() / '.Xdefaults'

    base16 = {}
    with open(xdefaults_file, 'r') as infile:
        for line in infile.readlines():
            match = re.match(r'#define (base.*) (#.*)$', line.strip())
            if match:
                base16[match.group(1)] = match.group(2)
    return base16


# -------------------------------------------------------------------
BASE16 = load_base16()


# -------------------------------------------------------------------
def load_template(filename):
    with open(filename, "r") as infile:
        return Template(infile.read())


# -------------------------------------------------------------------
def main():
    jinja_rc_files = Path.home().glob('.conky/rc/*.jinja')
    existing_rc_files = Path.home().glob('.conky/rc/*.rc')
    for rc_file in existing_rc_files:
        rc_file.unlink()

    for jinja_rc_file in jinja_rc_files:
        for screen in range(0, screen_count()):
            template = load_template(jinja_rc_file)
            rc_file = jinja_rc_file.with_suffix('.screen-%d.rc' % screen)
            print('Writing %s' % rc_file)
            with open(rc_file, 'w') as outfile:
                print(template.render(screen=screen, **BASE16), file=outfile)


# -------------------------------------------------------------------
if __name__ == "__main__":
    main()
