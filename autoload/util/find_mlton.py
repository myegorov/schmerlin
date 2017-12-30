from shutil import which
from subprocess import run, PIPE, STDOUT

MLTON_EXE = 'mlton'
MLTON_CMD = '%s -expert true -show' %MLTON_EXE
MLTON_SEARCH_STRINGS = ['-show-basis-flat','-show-basis-def','-show-basis-compact']
MIN_MLTON_VER = 'MLton 20171229.*' 

def is_exe(command):
    """ Check if command found on PATH and is executable.
    """
    return which(command) is not None

def test_mlton():
    if is_exe(MLTON_EXE):
        usage = run(MLTON_CMD.split(), stdout=PIPE, stderr=STDOUT)
        if not all(substr in usage.stdout.decode('utf-8') for substr in MLTON_SEARCH_STRINGS):
            return 0
            # raise ImportError('Require MLton >= %s' %MIN_MLTON_VER)
        return 1
    else:
        # raise ImportError('MLton not found')
        return 0

if __name__ == "__main__":
    test_mlton()
