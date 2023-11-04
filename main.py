import os
import sys

from Source import Himnario

if __name__ == "__main__":
    datapath_file = "DATAPATH"
    if os.path.exists(datapath_file):
        with open(datapath_file) as f:
            datapath = f.readline().strip()
            f.close()
    else:
        datapath = "Data"
    if len(sys.argv) > 1:
        datapath = sys.argv[1]
    app = Himnario.App(datapath)
    app.mainloop()
