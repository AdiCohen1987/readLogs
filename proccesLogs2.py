from tkinter.filedialog import askopenfilename

from Tkinter import Tk


def read():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    print(filename)

    f = open(filename)



if __name__ == '__main__':
    read()