import re
from datetime import datetime

import easygui
import xlwt

VALID_PARAMETERS = ['traceId', 'level', 'logger', 'message']


def read():
    path = easygui.fileopenbox()
    excelBook = xlwt.Workbook()
    ws = excelBook.add_sheet('First Sheet')  # Add a sheet
    f1 = open(path, 'r+')
    data = f1.readlines()  # read all lines at once
    row = 0
    for col in range(len(VALID_PARAMETERS)):
        ws.write(row, col, VALID_PARAMETERS[col])
    ws.write(row, len(VALID_PARAMETERS), VALID_PARAMETERS[3] + ' part 2')
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
                            firstPart, secondPart = \
                                parameter[1][:round(len(parameter[1]) / 2)], parameter[1][round(len(parameter[1]) / 2):]
                            ws.write(row, column, firstPart)
                            ws.write(row, column + 1, secondPart)
                            column = column + 2
            row = row + 1

    now = datetime.now()
    excelBook.save(path + ' logs ' + now.strftime("%d-%m-%Y %H-%M-%S") + '.xls')
    f1.close()


if __name__ == '__main__':
    read()
