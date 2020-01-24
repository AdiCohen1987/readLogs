import re
from datetime import datetime

import easygui
import math
import xlsxwriter

WORKBOOK_HEADERS = ['traceId', 'level', 'logger', 'message', 'part 2', 'part 3', 'part 4', 'part 5']
CELL_SIZE_LIMIT = 32000


def read_lines():
    path = easygui.fileopenbox()

    workbook = xlsxwriter.Workbook(path + ' logs ' + datetime.now().strftime("%d-%m-%Y %H-%M-%S") + '.xlsx')
    worksheet = workbook.add_worksheet()

    file = open(path, 'r+')

    data = file.readlines()
    row = 0
    cell_format = workbook.add_format()
    cell_format.set_bg_color('yellow')
    # write headers to the excel sheet
    for col in range(len(WORKBOOK_HEADERS)):
        worksheet.write(row, col, WORKBOOK_HEADERS[col],cell_format)

    row = 1
    for i in range(len(data)):
        Line = re.split('","', data[i])
        column = 0
        if len(Line) > 1 and Line[0][8] != '}' and Line[0][2] == 'm':
            # split the trace ID
            parameter = re.split('\":"', Line[0])
            worksheet.write(row, column, parameter[1])
            column = column + 1
            # split the rest of the headers
            for j in range(1, len(Line)):
                parameter = re.split('\":"', Line[j])
                if parameter[0] in WORKBOOK_HEADERS:
                    if parameter[0] != WORKBOOK_HEADERS[3]:
                        worksheet.write(row, column, parameter[1])
                        column = column + 1
                    else:
                        # messages -  removing Backslashes and splitting if size is more then 32K
                        newStringWOBackslashes = parameter[1].replace("\\", "")
                        parameter[1] = newStringWOBackslashes
                        if len(parameter[1]) < CELL_SIZE_LIMIT:
                            worksheet.write(row, column, parameter[1])
                            column = column + 1
                        else:
                            amountOfCellsNeeded = math.ceil(len(parameter[1]) / CELL_SIZE_LIMIT)
                            messageSplitPartSize = round(len(parameter[1]) / amountOfCellsNeeded)
                            for y in range(0, amountOfCellsNeeded):
                                partSize = parameter[1][(messageSplitPartSize * y):(messageSplitPartSize * (y+1))]
                                worksheet.write(row, column, partSize)
                                column = column + 1
            row = row + 1

    worksheet.set_column(0, 6, 20)
    worksheet.autofilter('A1:H' + str(column))
    workbook.close()
    file.close()
    easygui.msgbox("Done")


if __name__ == '__main__':
    read_lines()
