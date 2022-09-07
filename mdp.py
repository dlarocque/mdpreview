import sys
from io import TextIOWrapper
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def compile_to_pdf(filepath: str, out: TextIOWrapper) -> None:
    print('compiling to pdf')
    subprocess.run(['pandoc', '-f', 'markdown', '-t',
                   'pdf', filepath], stdout=out)


class Handler(FileSystemEventHandler):

    def __init__(self, filepath: str, out: TextIOWrapper):
        self.filepath = filepath
        self.out = out


    def on_any_event(self, event) -> None:
        if event.event_type in ['modified', 'deleted']:
            compile_to_pdf(self.filepath, self.out)



def main(filepath: str) -> None:
    # Validate that filepath is a markdown file
    # TODO: Check if file exists
    if len(filepath) <= 3 or filepath[-3:] != '.md':
        print("invalid filepath")
        return

    out_filepath = filepath[:-3] + '.pdf'
    out_file = open(out_filepath, 'w')

    compile_to_pdf(filepath, out_file)

    zathura_process = subprocess.Popen(['zathura', out_filepath])

    event_handler = Handler(filepath, out_file)
    observer = Observer()
    observer.schedule(event_handler, filepath, recursive=False)
    observer.start()

    try:
        while zathura_process.poll() is None:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('missing file name')
    else:
        main(sys.argv[1].strip())

