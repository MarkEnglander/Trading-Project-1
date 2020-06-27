import pandas as pd
import numpy as np
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib import colors
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPDF

from TradingClasses import *

config_default = TradeCsvConfig()
# Change all_data to be the database
all_data = pd.read_csv("order_details_US (1).csv")


def input_to_time(time):
    return datetime.strptime(time, '20%y-%m-%d %H:%M:%S+00:00')


# The function that should be used most of the time, with 5 dynamic inputs
def get_pdf(start_time='', end_time='', orderref='', accountno='', symbol='', data=all_data):
    # sort out the title:
    start = " Start - " + start_time.replace(':', '-') if start_time != '' else ''
    end = " End - " + end_time.replace(':', '-') if end_time != '' else ''
    order = " Orderref - " + orderref if orderref != '' else ''
    account = " Accountno - " + accountno if accountno != '' else ''
    sym = " Symbol - " + symbol if symbol != '' else ''
    title = sym + account + order + start + end

    # Get all the time formats in a useful form (datetime)
    data['time'] = [input_to_time(x) for x in data['time']]
    data.sort_values(by='time', ascending=True)
    data2 = data
    if start_time != '':
        data = data[(data['time'] > start_time)]
    if end_time != '':
        data = data[(data['time'] < end_time)]
    if symbol != '':
        data = data[(data['symbol'] == symbol)]
    if orderref != '':
        data = data[(data['OrderRef'] == orderref)]
    if accountno != '':
        data = data[(data['accountNo'] == accountno)]
    get_pdf_of_stats(data, title)


# Takes a config as defined in TradingClasses (can just use default) and data in the form of pandas reading a csv.
# Would not use this library for pdfs again, so I'm not commenting what's below.
def get_pdf_of_stats(data, title, config=config_default):
    canvas = Canvas("Results - " + title + ".pdf")
    trades = csv_to_trades(data, config)
    statss = all_trade_stats(trades, title)
    li = list(statss.split("\n"))
    start = 790
    canvas.setFont('Times-Bold', 13)
    for i in li:
        canvas.drawString(70, start, i)
        start -= 15
    print(canvas.getAvailableFonts())
    # create the pie chart
    d = Drawing()
    pie = Pie()
    pie.x = 100
    pie.y = 50
    win_no = len(trade_filter(trades, True))
    loss_no = len(trade_filter(trades, False))
    total = float(win_no + loss_no)
    pie_data = [np.round(100 * win_no / float(total)), np.round(100 * loss_no / float(total))] if total > 0 else [0, 0]
    pie.labels = ['Profiting', 'Losing']
    pie.slices.strokeWidth = 0.5
    pie.data = pie_data
    d.add(pie)
    renderPDF.draw(d, canvas, 300, 400, showBoundary=False)

    # create the bar chart
    d2 = Drawing()
    bar = VerticalBarChart()
    dataa = get_list(trades, 'profit')
    d2.add(bar, '')
    dataaa = [[x] for x in dataa]
    if len(dataaa) > 0:
        bar.data = dataaa
        for i in range(len(dataaa)):
            bar.bars[(i, 0)].fillColor = colors.green if dataaa[i][0] > 0 else colors.red
        renderPDF.draw(d2, canvas, 300, 650, showBoundary=False)
    canvas.save()


from TradingClasses import *
from FunctionsForStats import *
from TradeGraphs import *