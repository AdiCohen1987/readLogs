
import easygui
import xlwt


def read():
  path = easygui.fileopenbox()

  excelbook = xlwt.Workbook()
  ws = excelbook.add_sheet('First Sheet')  # Add a sheet

  #f = open('/DOT/textfile.txt', 'r+')
  f1 = open(path, 'r+')
  row
  data = f1.readlines()  # read all lines at once
  for i in range(len(data)):
    row = data[
      i].split()  # This will return a line of string data, you may need to convert to other formats depending on your use case

    for j in range(len(row)):
      ws.write(i, j, row[j])  # Write to cell i, j

  excelbook.save('logs' + '.xls')
  f1.close()


if __name__ == '__main__':
    read()