import re
from datetime import datetime
import math
import tkinter as tk
from tkinter import filedialog
import xlsxwriter

VALID_PARAMETERS = ['traceId', 'level', 'logger', 'message']

def read():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename()

    now = datetime.now()

    workbook = xlsxwriter.Workbook(path + ' logs ' + now.strftime("%d-%m-%Y %H-%M-%S") + '.xlsx')
    ws = workbook.add_worksheet()
    f1 = open(path, 'r+')
    data = f1.readlines()  # read all lines at once
    row = 0
    for col in range(len(VALID_PARAMETERS)):
        ws.write(row, col, VALID_PARAMETERS[col])
    ws.write(row, len(VALID_PARAMETERS), VALID_PARAMETERS[3] + ' part 2')
    ws.write(row, len(VALID_PARAMETERS)+1, VALID_PARAMETERS[3] + ' part 3')
    ws.write(row, len(VALID_PARAMETERS)+2, VALID_PARAMETERS[3] + ' part 4')
    ws.write(row, len(VALID_PARAMETERS)+3, VALID_PARAMETERS[3] + ' part 5')

    row = 1
    for i in range(len(data)):
        Line = re.split('","', data[i])
        column = 0
        if len(Line) > 1 and Line[0][8] != '}' and Line[0][2] == 'm':
            parameter = re.split('\":"', Line[0])
            ws.write(row, column, parameter[1])  # Write to cell i, j
            column = column + 1
            for j in range(1, len(Line)):
                parameter = re.split('\":"', Line[j])
                if parameter[0] in VALID_PARAMETERS:
                    if parameter[0] != VALID_PARAMETERS[3]:
                        ws.write(row, column, parameter[1])
                        column = column + 1
                    else:
                        newStringWOBackslash = parameter[1].replace("\\", "")
                        parameter[1] = newStringWOBackslash
                        if len(parameter[1]) < 32000:
                            ws.write(row, column, parameter[1])
                            column = column + 1
                        else:
                            amountOfCellsNeeded = math.ceil(len(parameter[1]) / 32000)
                            partSize = round(len(parameter[1]) / amountOfCellsNeeded)
                            firstPart = parameter[1][:partSize]
                            ws.write(row, column, firstPart)
                            column = column + 1
                            for y in range(2, amountOfCellsNeeded):
                                middlePart = parameter[1][(partSize * (y - 1)):(partSize * (y))]
                                ws.write(row, column, middlePart)
                                column = column + 1
                            lastPart = parameter[1][((partSize) * (amountOfCellsNeeded - 1)):]
                            ws.write(row, column, lastPart)
                            column = column + 1
            row = row + 1

    workbook.close()
    f1.close()


if __name__ == '__main__':
    read()
