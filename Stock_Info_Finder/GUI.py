import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import tkinter.scrolledtext as tkscroll
import get_comp_inf as gci
import get_news as gn
import get_cashflow as gc
import get_analytics as ga
import get_future as gf


height = 900
width = 900


def get_info_text(query):
    try:
        text_result = gci.get_comp_inf(query)
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.INSERT, text_result)
    except:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.INSERT, 'Oops! Something went wrong. Try a different ticker. Thank you!')


def get_news_text(query):
    try:
        text_result = gn.get_news(query)
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.INSERT, text_result)
    except:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.INSERT, 'Oops! Something went wrong. Try a different ticker. Thank you!')


def get_cashflow_text(query):
    try:
        text_result = gc.get_cashflow(query)
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.INSERT, text_result)
    except:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.INSERT, 'Oops! Something went wrong. Try a different ticker. Thank you!')


def get_analytics_text(query):
    try:
        text_result = ga.get_stock_trend(query)
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.INSERT, text_result)
    except:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.INSERT, 'Oops! Something went wrong. Try a different ticker. Thank you!')


def plot_hp_chart(query):
    data = ga.get_data_for_analysis(query)
    name = str(query).upper() + ' historical prices'
    plt.figure()
    plt.grid(False)
    plt.plot(data['value'], label=name, color='#000033')
    plt.plot(data['roll_mean'], label='Bollinger Middle Band', color='#e6b800', linestyle="--" )
    plt.plot(data['upper_band'], label='Bollinger Upper Band', color='#00802b', linestyle=":")
    plt.plot(data['lower_band'], label='Bollinger Lower Band', color='#cc0066', linestyle=":")
    plt.title(f'{name}', size=10)
    plt.xlabel('Date', size=10)
    plt.ylabel('Price in $', size=10)
    plt.xticks(size=7)
    plt.yticks(size=7)
    plt.legend(loc=0, fontsize='x-small')
    plt.xticks(np.arange(0, 82, 5), rotation=30)
    plt.show()


def get_prediction(query):
    try:
        text_result, data = gf.get_predictions(query)
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.INSERT, text_result)
    except:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.INSERT, 'Oops! Something went wrong. Try a different ticker. Thank you!')


def plot_future(query):
    text, data = gf.get_predictions(query)
    name = str(query).upper() + ' 15 day price prediction'
    plt.figure()
    plt.grid(False)
    plt.plot(data['value'], label='Historical prices', color='#000033')
    plt.plot(data['svm'], label='Prices predicted - Support Vector Model', color='#ff1a66', linestyle="--")
    plt.plot(data['lr'], label='Prices predicted - Linear Regression', color='#00b300', linestyle="--")
    plt.title(name, size=10)
    plt.xlabel('Trading days', size=10)
    plt.ylabel('Price in $', size=10)
    plt.xticks(size=7)
    plt.yticks(size=7)
    plt.legend(loc=0, fontsize='x-small')
    plt.xticks(np.arange(0, 40, 1))
    plt.show()



root = tk.Tk()
root.title('Stock Info Finder')

canvas = tk.Canvas(root, height=height, width=width)
canvas.pack()

upper_frame = tk.Frame(root, bg='#3e3e5b', bd=3)
upper_frame.place(relx=0.5, relwidth=0.90, relheight=0.09, anchor='n', rely=0.03)

upper_label = tk.Label(upper_frame, justify='left', wraplength=760, anchor='nw', bd=15, bg='#f0f0f5')
upper_label.place(relwidth=1, relheight=1)
upper_label['font'] = ("Century Schoolbook", '9')
upper_label['text'] = 'Welcome to Stock Info Finder! Enter an exchange ticker in the yellow field below and hit relevant buttons to obtain desired information and charts. ' \
                      'Note: app is connected to sandbox environment so it is recommended to try serurities from Dow Jones 30 index. \n' \
                      'Here you can find the list: https://money.cnn.com/data/dow30/ \n' \

frame = tk.Frame(root, bg='#004d4d', bd=3)
frame.place(relx=0.5, relwidth=0.90, relheight=0.04, anchor='n', rely=0.14)

lower_frame = tk.Frame(root, bg='#004d4d', bd=3)
lower_frame.place(relx=0.5, relwidth=0.90, relheight=0.75, anchor='n', rely=0.21)

text_area = tkscroll.ScrolledText(master=lower_frame, wrap=tk.WORD, padx=20, pady=20)
text_area['font'] = ("Century Schoolbook", '10')
text_area.pack(fill=tk.BOTH, expand=True)

entry = tk.Entry(frame, bg='#ffffcc', font=16)
entry.place(relwidth=0.11, relheight=1, relx=0.01)
entry['font'] = ("Century Schoolbook", '12')

button = tk.Button(frame, text='Comp Info', bg='#f0f5f5', command=lambda: get_info_text(entry.get()))
button.place(relx=0.16, relwidth=0.11, relheight=1)
button['font'] = ("Century Schoolbook", '9', 'bold')

button2 = tk.Button(frame, text='News', bg='#d1e0e0', command=lambda: get_news_text(entry.get()))
button2.place(relx=0.28, relwidth=0.11, relheight=1)
button2['font'] = ("Century Schoolbook", '9', 'bold')

button3 = tk.Button(frame, text='Cashflow', bg='#b3cbcb', command=lambda: get_cashflow_text(entry.get()))
button3.place(relx=0.40, relwidth=0.11, relheight=1)
button3['font'] = ("Century Schoolbook", '10', 'bold')

button4 = tk.Button(frame, text='Analytics', bg='#95b7b7', command=lambda: get_analytics_text(entry.get()))
button4.place(relx=0.52,relwidth=0.11, relheight=1)
button4['font'] = ("Century Schoolbook", '9', 'bold')

button5 = tk.Button(frame, text='Prediction', bg='#76a2a2', command=lambda: get_prediction(entry.get()))
button5.place(relx=0.64,relwidth=0.11, relheight=1)
button5['font'] = ("Century Schoolbook", '9', 'bold')

button6 = tk.Button(frame, text='HP Chart', bg='#d1d1e0', command=lambda: plot_hp_chart(entry.get()))
button6.place(relx=0.76,relwidth=0.11, relheight=1)
button6['font'] = ("Century Schoolbook", '9', 'bold')

button7 = tk.Button(frame, text='Fut Chart', bg='#b3b3cb', command=lambda: plot_future(entry.get()))
button7.place(relx=0.88,relwidth=0.11, relheight=1)
button7['font'] = ("Century Schoolbook", '9', 'bold')

root.mainloop()