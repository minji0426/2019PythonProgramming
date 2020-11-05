import csv  # CSV 모듈 불러오기
import matplotlib.pyplot as plt

f = open('mybirthday_weather.csv')  # seoul.csv 파일 읽기 모드로 불러오기
data = csv.reader(f)
header = next(data)  # 맨 윗줄을 header 변수에 저장하기
year=[]
a=0
for row in data:
    if(row[0].split('-')[1] =='04'):
        if(row[0].split('-')[2]=='26'):
            year.append((float(row[3]), float(row[4])))
plt.boxplot(year)
plt.show()
f.close()