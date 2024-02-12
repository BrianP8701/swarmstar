import sys
import pdb
import traceback

try:
    pass
except:
    extype, value, tb = sys.exc_info()
    traceback.print_exc()
    pdb.post_mortem(tb)