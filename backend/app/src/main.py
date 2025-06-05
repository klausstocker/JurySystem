import os
import sys
import time

try:
    from shared.foo import module
except ImportError:
    # need to append paths
    sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
    sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
    from shared.foo import module

if __name__ == '__main__':
    print('Main started')
    while True:
        print(f"{time.time():} Alive :-)")
        module.printout()
        time.sleep(1)
