from shutil import which

MLTON = 'mlton'
MIN_MLTON_VER = 20171201 # TODO: update when -show-basis-flat branch merged

TRANSMLER = 'transmile'
MIN_TRANSMLER_VER = '0.3.3'

def is_exe(command):
    """ Check if command found on PATH and is executable.
    """
    return which(command) is not None

