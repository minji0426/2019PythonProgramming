import csv

f = open('seoul_weather.csv')
data = csv.reader(f)
header = next(data)
max_temp = -999
max_date = ''

for row in data:
    if row[-1] == '':
        row[-1] = -999
    row[-1] = float(row[-1])
    if max_temp < row[-1]:
        max_date = row[0]
        max_temp = row[-1]
f.close()
print('지난 100년 간 서울의 가장 더웠던 날은', max_date + '로,', max_temp, '도 였습니다.')