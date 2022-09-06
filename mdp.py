import sys
import subprocess
import os
import time


def main(filename: str):
    # Validate that filename is a markdown file
    # TODO: Check if file exists
    if len(filename) <= 3 or filename[-3:] != '.md':
        print("invalid filename")
        return

    out_filename = filename[:-3] + '.pdf'
    out_file = open(out_filename, 'w')

    subprocess.run(['pandoc', '-f', 'markdown', '-t',
                   'pdf', filename], stdout=out_file)

    zathura_process = subprocess.Popen(['zathura', out_filename])

    last_modified = os.stat(filename).st_mtime
    while zathura_process.poll() is None:
        time.sleep(0.1)  # should be event based

        if last_modified != os.stat(filename).st_mtime:
            last_modified = os.stat(filename).st_mtime

            out_file = open(out_filename, 'w')
            subprocess.run(['pandoc', '-f', 'markdown', '-t',
                           'pdf', filename], stdout=out_file)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('missing file name')
    else:
        main(sys.argv[1].strip())
