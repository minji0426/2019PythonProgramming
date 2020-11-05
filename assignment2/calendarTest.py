import calendar
import tkinter as tk
import time
from tkinter import ttk
from tkinter import *
import csv
import operator
from collections import deque
from korean_lunar_calendar import KoreanLunarCalendar

class MyDatePicker(tk.Toplevel):
    def __init__(self, widget=None, format_str=None):
        super().__init__()
        self.widget = widget
        self.str_format = format_str
        self.init_frames()

        self.dat1_list = []       #cvs파일 불러와서 저장
        with open('birthday.CSV', 'r') as raw:
            reader = csv.reader(raw)
            for lines in reader:
                self.dat1_list.append(lines)

        self.dat2_list = []
        self.dic = {}           #dictionary 사용
        for line in self.dat1_list:
            bir_mon = line[3][2] + line[3][3]
            bir_day = line[3][4] + line[3][5]
            a = [line[1], bir_mon, bir_day]
            self.dat2_list.append(a)
            self.dic[line[1]] = bir_mon + bir_day

        self.init_needed_vars()
        self.init_month_year_labels()
        self.init_buttons()
        self.space_between_widgets()
        self.c_mon=self.month_names.index(self.month_str_var.get())
        self.fill_days()
        self.make_calendar()

    def list_birthday(self):
        window = Toplevel(root)

        sdic = sorted(self.dic.items(), key=operator.itemgetter(1))
        print("<전체 생일 리스트>")
        self.label_1 = tk.Label(window, text="<전체 생일 리스트>")
        self.label_1.pack()

        fifo = deque()      #deque 사용
        fifo.append(sdic)
        for i in fifo:
            for a in i:
                m = int(a[1][0] + a[1][1])
                d = int(a[1][2] + a[1][3])
                s = a[0] + " : " + str(m) + "월 " + str(d) + "일"
                self.label_1 = tk.Label(window, text=s)
                self.label_1.pack()
                print("{} : {}월 {}일".format(a[0], str(m), str(d)))

    def month_list_birthday(self, month):
        window = Toplevel(root)

        print("<이번 달 생일 리스트>")
        self.label_1 = tk.Label(window, text="<이번 달 생일 리스트>")
        self.label_1.pack()
        for a in self.dat2_list:
            if int(a[1]) == month:
                m = int(a[1])
                d = int(a[2])
                s = a[0] + " : " + str(m) + "월 " + str(d) + "일"
                self.label_1=tk.Label(window,text=s)
                self.label_1.pack()
                print("{} : {}월 {}일".format(a[0], str(m), str(d)))

    def init_frames(self):
        self.frame2 = tk.Frame(self)    #사진 프레임
        self.frame2.pack()

        self.imgObj = PhotoImage(file="pengsoo.gif")
        self.imgLabel = Label(self.frame2)
        self.imgLabel.config(image=self.imgObj)
        self.imgLabel.pack()

        self.frame1 = tk.Frame(self)    #월, 년도, 이전,다음버튼 프레임
        self.frame1.pack()

        self.frame_days = tk.Frame(self)    #날짜 프레임
        self.frame_days.pack()

        self.frame_button = tk.Frame(self)  #생일 리스트 보여주는 버튼 프레임
        self.frame_button.pack()
        self.bir1_button = Button(self.frame_button, text="전체 생일 리스트", command=self.list_birthday)
        self.bir1_button.pack()

        self.bir2_button = Button(self.frame_button, text="이번 달 생일 리스트", command=lambda: self.month_list_birthday(self.c_mon))
        self.bir2_button.pack()

    def init_needed_vars(self):
        self.month_names = tuple(calendar.month_name)    #tuple 사용
        self.day_names = tuple(calendar.day_abbr)
        self.year = time.strftime("%Y")     #현재의 년도
        self.month = time.strftime("%B")    #현재의 달

    def init_month_year_labels(self):
        self.year_str_var = tk.StringVar()
        self.month_str_var = tk.StringVar()

        self.year_str_var.set(self.year)    #년도 값 넣어줌
        self.year_lbl = tk.Label(self.frame1, textvariable=self.year_str_var, width=3) #년도의 라벨 생성
        self.year_lbl.grid(row=0, column=5) #그리드뷰에 넣어줌

        self.month_str_var.set(self.month)      #현재 달을 넣어줌
        self.month_lbl = tk.Label(self.frame1, textvariable=self.month_str_var,width=8)
        self.month_lbl.grid(row=0, column=1)

    def init_buttons(self):     #이전, 다음으로 넘기는 버튼 생성
        self.left_yr = ttk.Button(self.frame1, text="←", width=5, command=self.prev_year)
        self.left_yr.grid(row=0, column=4)

        self.right_yr = ttk.Button(self.frame1, text="→", width=5, command=self.next_year)
        self.right_yr.grid(row=0, column=6)

        self.left_mon = ttk.Button(self.frame1, text="←", width=5, command=self.prev_month)
        self.left_mon.grid(row=0, column=0)

        self.right_mon = ttk.Button(self.frame1, text="→", width=5, command=self.next_month)
        self.right_mon.grid(row=0, column=2)

    def space_between_widgets(self):    #간격
        self.frame1.grid_columnconfigure(3, minsize=40)

    def prev_year(self):    #이전 년도로 바꾸는 함수
        self.prev_yr = int(self.year_str_var.get()) - 1
        self.year_str_var.set(self.prev_yr)

        self.make_calendar()

    def next_year(self):    #다음 년도로 바꾸는 함수
        self.next_yr = int(self.year_str_var.get()) + 1
        self.year_str_var.set(self.next_yr)

        self.make_calendar()

    def prev_month(self):   #이전 달로 바꾸는 함수
        index_current_month = self.month_names.index(self.month_str_var.get())
        index_prev_month = index_current_month - 1
        if index_prev_month == 0:
            self.month_str_var.set(self.month_names[12])
            self.prev_year()
        else:
            self.month_str_var.set(self.month_names[index_current_month - 1])
        self.c_mon=self.c_mon - 1
        if self.c_mon==0:
            self.c_mon=12
        self.make_calendar()

    def next_month(self):   #다음 달로 바꾸는 함수
        index_current_month = self.month_names.index(self.month_str_var.get())
        try:
            self.month_str_var.set(self.month_names[index_current_month + 1])
        except IndexError:
            self.month_str_var.set(self.month_names[1])
            self.next_year()
        self.c_mon = self.c_mon + 1
        if self.c_mon == 13:
            self.c_mon = 1
        self.make_calendar()

    def fill_days(self):    #요일 넣어주는 함수
        col = 0
        for day in self.day_names:
            self.lbl_day = tk.Label(self.frame_days, text=day)
            self.lbl_day.grid(row=0, column=col)
            col += 1

    def make_calendar(self):    #달력 만드는 함수
        try:
            for dates in self.m_cal:
                for date in dates:
                    if date == 0:
                        continue
                    self.delete_buttons(date)
            self.delete_buttons
        except AttributeError:
            pass

        year = int(self.year_str_var.get())     #년도 저장
        month = self.month_names.index(self.month_str_var.get())    #월 저장
        self.m_cal = calendar.monthcalendar(year, month)

        for dates in self.m_cal:
            row = self.m_cal.index(dates) + 1
            for date in dates:
                col = dates.index(date)
                if date == 0:
                    continue
                k_calendar = KoreanLunarCalendar()      #음력으로 바꿔주는 코드
                k_calendar.setSolarDate(year, month, date)
                k_day = k_calendar.LunarIsoFormat()

                num = 0
                for a in self.dat2_list:
                    m = int(a[1])
                    d = int(a[2])
                    if m == month and d == int(date):
                        num = num + 1
                self.make_button(str(date), str(row), str(col), str(k_day.split('-')[1]), str(k_day.split('-')[2]),num) #날짜, 행, 열을 인자로 함수를 넣어줌.

    def make_button(self, date, row, column, k_m, k_d, num):    #버튼 생성
        if num==0:
            exec(
                "self.btn_" + date + " = ttk.Button(self.frame_days, text='(" +k_m+"/"+k_d+")"+'\\n'+ date+'\\n'
                +"'"+ ", width=8)\n"
                  "self.btn_" + date + ".grid(row=" + row + " , column=" + column
                + ")\n"
                  "self.btn_" + date + ".bind(\"<Button-1>\", self.get_date)"
            )
        else:
            num=str(num)
            exec(
                "self.btn_" + date + " = ttk.Button(self.frame_days, text='(" + k_m + "/" + k_d + ")" + '\\n' + date + '\\n' +"생일:"+num
                + "'" + ", width=8)\n"
                        "self.btn_" + date + ".grid(row=" + row + " , column=" + column
                + ")\n"
                  "self.btn_" + date + ".bind(\"<Button-1>\", self.get_date)"
            )

    def delete_buttons(self, date):     #버튼 삭제
        exec(
            "self.btn_" + str(date) + ".destroy()"
        )

    def get_date(self, clicked=None):
        window = Toplevel(root)

        clicked_button = clicked.widget
        year = self.year_str_var.get()
        month = self.month_names.index(self.month_str_var.get())
        date = clicked_button['text']
        date = str(date).split('\n')[1]

        s = "<" +str(month) + "월 " + str(date) + "일" + " 생일자>"
        self.label = tk.Label(window, text=s)
        self.label.pack()
        print(s)
        num=0
        ss=set()        #set 사용
        for a in self.dat2_list:
            m = int(a[1])
            d = int(a[2])
            if m == month and d == int(date):
                ss.add(a[0])
                print(a[0])
                num=num+1
        for a in ss:
            self.label_1 = tk.Label(window, text=a)
            self.label_1.pack()
        if num==0:
            self.label = tk.Label(window, text="없음")
            self.label.pack()
            print("생일자 없음")
        try:
            self.widget.delete(0, tk.END)
            self.widget.insert(0, self.full_date)
        except AttributeError:
            pass

if __name__ == '__main__':
    def application():
        MyDatePicker()

    root = tk.Tk()
    root.withdraw()
    application()
    root.mainloop()