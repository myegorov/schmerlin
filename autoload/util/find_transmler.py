from distutils.version import LooseVersion

MIN_TRANSMLER_VER = '0.3.3'

def test_transmler():
    try:
        import transmler
        if LooseVersion(transmler.__version__) < LooseVersion(MIN_TRANSMLER_VER):
            # raise ImportError('Require transmler >= %s' %MIN_TRANSMLER_VER)
            return 0
        return 1
    except ModuleNotFoundError as err:
        # raise err
        return 0
    except AttributeError:
        # raise ImportError('Require transmler >= %s' %MIN_TRANSMLER_VER)
        return 0

if __name__ == "__main__":
    test_transmler()
