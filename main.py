import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox as tkmes
from scipy.spatial import ConvexHull, convex_hull_plot_2d
from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt
from ConvexHullCalculate.ConvexHullCalculate import ConvexHullCalculate

m = 2

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica',
                                      size=18)
        self.geometry("400x400")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):
    @staticmethod
    def increase(lbl_value):
        global m
        m=m+1
        lbl_value["text"] = f"{m} "
    @staticmethod
    def discrease(lbl_value):
        global m
        if m>1:
            m=m-1
            lbl_value["text"] = f"{m}"
        else:
            tkmes.showinfo("不得為0","我們的範圍要大於0")
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="請決定你要的維度",font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        dim_control = tk.Frame(self)
        dim_control.rowconfigure(0,minsize=50,weight=1)
        dim_control.columnconfigure([0,1,2],minsize=50,weight=1)
        dim_control.pack(side="top",expand=True)


        lbl_value = tk.Label(master=dim_control,text=f"{m}")
        lbl_value.grid(row=0,column=1)

        btn_increase = tk.Button(master=dim_control,text="+",width=2,height=1,
                                 command=lambda:self.increase(lbl_value))
        btn_increase.grid(row=0,column=2,sticky="nesw")

        btn_decress = tk.Button(master=dim_control,text="-",width=2,height=1,
                                command=lambda:self.discrease(lbl_value))
        btn_decress.grid(row=0,column=0,sticky="nesw")

        button1 = tk.Button(self, text="進入下一步", height=1 ,
                            command=lambda: controller.show_frame("PageOne"))
        button1.pack(padx=100,expand=True)

        labelOR = tk.Label(self, text="或", height=1)
        labelOR.pack(padx=100,expand=True)
        button2 = tk.Button(self, text="計算二維+圖形介面", height=1 ,
                            command=lambda: controller.show_frame("PageTwo"))
        button2.pack(padx=100,expand=True)


class PageTwo(tk.Frame):
    def CVimage(list_point):
        AllPoints = np.mat(list_point)
        xPoints = AllPoints[:AllPoints.shape[0]-1,:]
        print(xPoints)

    @staticmethod
    def addValue(xEntry,yEntry,xValueLB):
        x_str = xEntry.get()
        y_str = yEntry.get()
        last_str = ""
        for Value in (x_str,y_str):
            isNum = False
            isStart = True
            for i in Value:
                last_str=i
                if isNum: #若下一個不是為數字, 代表輸入有錯
                    if i not in "1234567890":
                        tkmes.showinfo("請輸入正確","分數、小數有誤")
                        return None
                    continue
                if isStart: #若第一格或','後面的空格不為數字或'-', 代表輸入有錯
                    if i not in "1234567890-":
                        tkmes.showinfo("請輸入正確","第一個字不是數字")
                        return None
                    isStart = False
                    if i == '-': #如果為'-', 要確定下一個是否為數字
                        isNum=True
                    continue
                elif i in "1234567890./":
                    #若為'.'或'/',檢查下一個是否為數字 
                    if i in "./":
                        isNum = True
                else: #若不為我們要求的字元, 有錯
                    tkmes.showinfo("請輸入正確","請輸入我們規定的字元")
                    return None
            if Value =="":
                tkmes.showinfo("請輸入正確","裡面為空")
                return None
            if last_str not in "0123456789":
                tkmes.showinfo("請輸入正確","最後一個字不是數字")
                return None
        #加入到Listbox
        Value = f"{x_str},{y_str}"
        xValueLB.insert(tk.END, Value)
        xEntry.delete(0,tk.END)
        yEntry.delete(0,tk.END)

    @staticmethod
    def backToDim2(xEntry,yEntry,p1Entry,p2Entry,xValueLB,controller):
        xEntry.delete(0,tk.END)
        yEntry.delete(0,tk.END)
        p1Entry.delete(0,tk.END)
        p2Entry.delete(0,tk.END)
        xValueLB.delete(0,tk.END)
        controller.show_frame("StartPage")
    @staticmethod
    def calculate(p1_str,p2_str,xLB):
        last_str = ""
        for Value in (p1_str,p2_str):
            isNum = False
            isStart = True
            for i in Value:
                last_str=i
                if isNum: #若下一個不是為數字, 代表輸入有錯
                    if i not in "1234567890":
                        tkmes.showinfo("請輸入正確","分數、小數有誤")
                        return None
                    continue
                if isStart: #若第一格或','後面的空格不為數字或'-', 代表輸入有錯
                    if i not in "1234567890-":
                        tkmes.showinfo("請輸入正確","第一個字不是數字")
                        return None
                    isStart = False
                    if i == '-': #如果為'-', 要確定下一個是否為數字
                        isNum=True
                    continue
                elif i in "1234567890./":
                    #若為'.'或'/',檢查下一個是否為數字 
                    if i in "./":
                        isNum = True
                else: #若不為我們要求的字元, 有錯
                    tkmes.showinfo("請輸入正確","請輸入我們規定的字元")
                    return None
            if Value =="":
                tkmes.showinfo("請輸入正確","裡面為空")
                return None
            if last_str not in "0123456789":
                tkmes.showinfo("請輸入正確","最後一個字不是數字")
                return None
        #加入到Listbox
        p_str = f"{p1_str},{p2_str}"
        print(p_str,xLB)
        if xLB == ():
            tkmes.showinfo("請輸入正確","起碼要有1個x")
            return None

        #########Listbox的東西轉成list#########
        A = list()
        #把每一列listbox變數字
        for i in xLB:
            if i == None:
                continue
            x = []
            for str_num in i.split(","):
                x.append(float(Fraction(str_num).limit_denominator()))
            A.append(x)
        #把p的Entry變數字
        p = []
        for str_num in p_str.split(","):
            p.append(float(Fraction(str_num).limit_denominator()))
        A.append(p)
        print(A)
        #開始計算
        is_in_CH = ConvexHullCalculate(A)
        if is_in_CH:
            tkmes.showinfo("結果","P在凸集內")
        else:
            tkmes.showinfo("結果","P不在凸集內")
        plt.clf()
        AllPoints = np.mat(A)
        fix_xPoints = np.copy(AllPoints[:AllPoints.shape[0]-1,:])
        if(fix_xPoints.shape[0]<3):
            plt.plot(fix_xPoints[:,0], fix_xPoints[:,1], 'o')
            plt.plot(fix_xPoints[:,0], fix_xPoints[:,1], 'k-')
        else:
            xPoints = np.copy(fix_xPoints)
            print(xPoints)
            for i in range(1,xPoints.shape[0]):
                xPoints[i,:] = xPoints[i,:]-xPoints[0,:]
            xPoints[0,:] = xPoints[0,:]-xPoints[0,:]
            print(xPoints)
            max = 0
            max_index = 1
            min = 0
            min_index = 0
            dim2 = False 
            print(xPoints.shape)
            for i in range(2,xPoints.shape[0]):
                d1 =Fraction(xPoints[i,0])/Fraction(xPoints[1,0])
                d2 = Fraction(xPoints[i,1])/Fraction(xPoints[1,1])
                print(d1,d2)
                if d1 != d2: 
                    dim2 = True
                    break
                if max < d1:
                    max = d1
                    max_index=i
                elif min > d1:
                    min = d1
                    min_index=i

            if(dim2):
                hull = ConvexHull(fix_xPoints)
                plt.plot(fix_xPoints[:,0], fix_xPoints[:,1], 'o')
                for simplex in hull.simplices:
                    plt.plot(fix_xPoints[simplex, 0], fix_xPoints[simplex, 1], 'k-')

            else:
                plt.plot(fix_xPoints[:,0], fix_xPoints[:,1], 'o',color='blue')
                plt.plot([fix_xPoints[min_index,0],fix_xPoints[max_index,0]],[fix_xPoints[min_index,1],fix_xPoints[max_index,1]],'k-')
            
        plt.plot(AllPoints[fix_xPoints.shape[0],0], AllPoints[fix_xPoints.shape[0],1], 'o',color='red', markersize=12)
        plt.show()
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="輸入x和p的值", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        #輸入x的Frame
        InputFrame = tk.Frame(self,height=11)
        InputFrame.rowconfigure([0,1,2,3],minsize=11,weight=1)
        InputFrame.columnconfigure([0,1,2,3,4],minsize=50,weight=1)
        InputFrame.pack(side="top",fill="x",pady=10)
        #把x放入Listbox(Listbox的Frame)
        getVelueFrame = tk.Frame(InputFrame)
        getVelueFrame.grid(row=0,column=2,rowspan=4,columnspan=3,sticky="nesw")
        #把x放入Listbox(Listbox的捲軸)
        scrollbar = tk.Scrollbar(getVelueFrame)         # 在頁框中加入捲軸元件
        scrollbar.pack(side='right', fill='y')  # 設定捲軸的位置以及填滿方式
        #把x放入Listbox
        xValueLB = tk.Listbox(getVelueFrame,selectmode=tk.SINGLE,yscrollcommand = scrollbar.set)
        xValueLB.pack(side='left', fill='y',expand=True)
        scrollbar.config(command = xValueLB.yview)
        #
        xFrame = tk.Frame(InputFrame)
        xFrame.grid(row=0,column=0,columnspan=1,sticky="ew")
        xFrame.columnconfigure([0,1,2,3,4,5],minsize=50,weight=1)
        xLabel = tk.Label(xFrame,text="x = ")
        xLabel.grid(row=0,column=0)
        xEntry = tk.Entry(xFrame)
        xEntry.grid(row=0,column=1,columnspan=1)
        #
        yLabel = tk.Label(xFrame,text="y = ")
        yLabel.grid(row=0,column=2)
        yEntry = tk.Entry(xFrame)
        yEntry.grid(row=0,column=3,columnspan=1)

        #加入和刪除的按鈕(Frame)
        BTframe = tk.Frame(InputFrame)
        BTframe.grid(row=1,column=0,sticky="ew")
        BTframe.rowconfigure(0,minsize=50,weight=50)
        BTframe.columnconfigure([0,1],minsize=50,weight=1)

        #加入和刪除的按鈕(加入)
        inputBT = tk.Button(BTframe,text="輸入",width=8,height=1,
                            command=lambda:self.addValue(xEntry,yEntry,xValueLB))

        #加入和刪除的按鈕(刪除)
        inputBT.grid(row=0,column=0)
        delBT = tk.Button(BTframe,text="刪除",width=8,height=1
                          ,command= lambda:xValueLB.delete(xValueLB.curselection()[0]) if xValueLB.size()>0 else tkmes.showinfo("已經空了","裡面是空的"))
        delBT.grid(row=0,column=1)


        pFrame = tk.Frame(InputFrame)
        pFrame.grid(row=3,column=0,columnspan=1,sticky="nesw")
        pFrame.columnconfigure([0,1,2,3,4,5],minsize=50,weight=1)
        p1Label = tk.Label(pFrame,text="p1 = ")
        p1Label.grid(row=0,column=0)
        p1Entry = tk.Entry(pFrame)
        p1Entry.grid(row=0,column=1,columnspan=1)
        #
        p2Label = tk.Label(pFrame,text="p2 = ")
        p2Label.grid(row=0,column=2)
        p2Entry = tk.Entry(pFrame)
        p2Entry.grid(row=0,column=3,columnspan=1)

        #選單按鍵(Frame)
        StarFrame = tk.Frame(self)
        StarFrame.rowconfigure(0,minsize=50,weight=1)
        StarFrame.columnconfigure([0,1],minsize=50,weight=1)
        StarFrame.pack(side="top",fill="x",pady=10)
        
        #選單按鍵(主選單Button)
        button = tk.Button(StarFrame, text="回到主選單",
                           command=lambda: self.backToDim2(xEntry,yEntry,p1Entry,p2Entry,xValueLB,controller))

        button.grid(row=0,column=1,padx=5, pady=5)

        #選單按鍵(計算凸集Button)
        Calbt= tk.Button(StarFrame, text="開始計算",
                           command=lambda: self.calculate(p1Entry.get(),p2Entry.get(),xValueLB.get(0,tk.END)))
        Calbt.grid(row=0,column=0,padx=5, pady=5)

#輸入x,p頁面
class PageOne(tk.Frame):
    #把Entry加入Listbox
    @staticmethod
    def addValue(inputValueEY,xValue,xValueLB):
        spaceCount = 0 #計數有幾個空格
        isStart = True #是否在第一格或','後面的空格
        isNum = False #下一個是否為數字
        for i in xValue:
            if isNum: #若下一個不是為數字, 代表輸入有錯
                if i not in "1234567890":
                    tkmes.showinfo("請輸入正確","分數、小數有誤")
                    return None
                isNum = False
                continue
            if isStart: #若第一格或','後面的空格不為數字或'-', 代表輸入有錯
                if i not in "1234567890-":
                    tkmes.showinfo("請輸入正確","第一個字不是數字")
                    return None
                isStart = False
                if i == '-': #如果為'-', 要確定下一個是否為數字
                    isNum=True
                continue
            elif i in "1234567890,./":
                #若為'.'或'/',檢查下一個是否為數字 
                if i in "./":
                    isNum = True
                #若為'-',檢查下一個是否為數字或'-' 
                elif i == ',':
                    isStart = True
                    spaceCount+=1
            else: #若不為我們要求的字元, 有錯
                tkmes.showinfo("請輸入正確","請輸入我們規定的字元")
                return None
        global m    
        if isNum:
            tkmes.showinfo("請輸入正確","最後一個字不是數字")
            return None
        if spaceCount != m-1:#空格數 != m-1(數字的數量是否符合維度)
            tkmes.showinfo("請輸入正確",f"我們要{m}個數")
            return None
        #加入到Listbox
        xValueLB.insert(tk.END, xValue)
        inputValueEY.delete(0,tk.END)

    #回到主頁
    @staticmethod
    def backToDim(inputPEY,inputValueEY,xValueLB,controller):
        inputPEY.delete(0,tk.END)
        inputValueEY.delete(0,tk.END)
        xValueLB.delete(0,tk.END)
        controller.show_frame("StartPage")

    @staticmethod
    def calculate(x_Value,p_Value):
        ################檢查p是否符合格式#################
        spaceCount = 0
        isStart = True
        isNum = False
        for i in p_Value:
            if isNum:
                if i not in "1234567890":
                    tkmes.showinfo("請輸入正確","分數、小數有誤")
                    return None
                isNum = False
                continue
            if isStart:
                if i not in "1234567890-":
                    tkmes.showinfo("請輸入正確","第一個字不是數字")
                    return None
                isStart = False
                if i == '-':
                    isNum=True
                continue
            elif i in "1234567890,./":
                if i in "./":
                    isNum = True
                elif i == ',':
                    isStart = True
                    spaceCount+=1
            else:
                tkmes.showinfo("請輸入正確","請輸入我們規定的字元")
                return None
        global m    
        if isNum:
            tkmes.showinfo("請輸入正確","p內的最後一個字不是數字")
            return None
        if spaceCount != m-1:
            tkmes.showinfo("請輸入正確",f"我們要{m}個數在p內的")
            return None
        #####################檢查完畢#########################
        if x_Value == ():
            tkmes.showinfo("請輸入正確","起碼要有1個x")
            return None

        #########Listbox的東西轉成list#########
        A = list()
        #把每一列listbox變數字
        for i in x_Value:
            if i == None:
                continue
            x = []
            for str_num in i.split(","):
                x.append(float(Fraction(str_num).limit_denominator()))
            A.append(x)
        #把p的Entry變數字
        p = []
        for str_num in p_Value.split(","):
            p.append(float(Fraction(str_num).limit_denominator()))
        A.append(p)
        print(A)
        #開始計算
        is_in_CH = ConvexHullCalculate(A)
        if is_in_CH:
            tkmes.showinfo("結果","P在凸集內")
        else:
            tkmes.showinfo("結果","P不在凸集內")
        
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #字體
        self.controller = controller
        contain_font = tkfont.Font(family='Helvetica',
                                      size=12)
        #標題
        label = tk.Label(self, text="輸入x 和 p", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
     
        #輸入x的Frame
        InputFrame = tk.Frame(self)
        InputFrame.rowconfigure([0,1,2,3],minsize=50,weight=1)
        InputFrame.columnconfigure([0,1],minsize=50,weight=1)
        InputFrame.pack(side="top",fill="x",pady=10)

        #輸入x的Entry
        inputValueEY = tk.Entry(InputFrame,font=contain_font) 
        inputValueEY.grid(row=1,column=0,padx=5, pady=5)

        #把x放入Listbox(Listbox的Frame)
        getVelueFrame = tk.Frame(InputFrame)
        getVelueFrame.grid(row=0,column=1,rowspan=3,sticky="nesw")
        #把x放入Listbox(Listbox的捲軸)
        scrollbar = tk.Scrollbar(getVelueFrame)         # 在頁框中加入捲軸元件
        scrollbar.pack(side='right', fill='y')  # 設定捲軸的位置以及填滿方式

        #把x放入Listbox
        xValueLB = tk.Listbox(getVelueFrame,selectmode=tk.SINGLE,yscrollcommand = scrollbar.set)
        xValueLB.pack(side='left', fill='y',expand=True)
        scrollbar.config(command = xValueLB.yview)

        #加入和刪除的按鈕(Frame)
        BTframe = tk.Frame(InputFrame)
        BTframe.grid(row=2,column=0,sticky="nesw")
        BTframe.rowconfigure(0,minsize=50,weight=50)
        BTframe.columnconfigure([0,1],minsize=50,weight=1)

        #加入和刪除的按鈕(加入)
        inputBT = tk.Button(BTframe,text="輸入",width=8,height=1,
                            command=lambda:self.addValue(inputValueEY,inputValueEY.get(),xValueLB))

        #加入和刪除的按鈕(刪除)
        inputBT.grid(row=0,column=0)
        delBT = tk.Button(BTframe,text="刪除",width=8,height=1
                          ,command= lambda:xValueLB.delete(xValueLB.curselection()[0]) if xValueLB.size()>0 else tkmes.showinfo("已經空了","裡面是空的"))
        delBT.grid(row=0,column=1)

        #輸入點p(提示label)
        labelP = tk.Label(InputFrame,text="輸入p：")
        labelP.grid(row=3,column=0,padx=5, pady=5)
        #輸入點p(輸入Entry)
        inputPEY = tk.Entry(InputFrame,font=contain_font) 
        inputPEY.grid(row=3,column=1,padx=5, pady=5)

        #選單按鍵(Frame)
        StarFrame = tk.Frame(self)
        StarFrame.rowconfigure(0,minsize=50,weight=1)
        StarFrame.columnconfigure([0,1],minsize=50,weight=1)
        StarFrame.pack(side="top",fill="x",pady=10)
        
        #選單按鍵(主選單Button)
        button = tk.Button(StarFrame, text="回到主選單",
                           command=lambda: self.backToDim(inputPEY,inputValueEY,xValueLB,controller))
        button.grid(row=0,column=1,padx=5, pady=5)

        #選單按鍵(計算凸集Button)
        Calbt= tk.Button(StarFrame, text="開始計算",
                           command=lambda: self.calculate(xValueLB.get(0,tk.END),inputPEY.get()))
        Calbt.grid(row=0,column=0,padx=5, pady=5)


if __name__ == '__main__':
    app = App()
    app.mainloop()
'''
    window = tk.Tk()
    label = tk.Label(text="Hello, Tkinter",
                     foreground="white",
                     background="#708090",
                     width = 10,
                     height = 10)
    button = tk.Button(
        text = "Click me",
        width=25,
        height=5,
        background="blue",
        foreground="yellow"
    )
    entry = tk.Entry(fg="yellow",
                     bg='blue',
                     width=50)
    label.pack()
    button.pack()
    entry.pack()
    window.mainloop()
'''