import pandas as pd
import numpy as np
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from io import BytesIO
from reportlab.graphics import renderPDF


pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))


# Takes a config as defined in TradingClasses (can just use default) and data in the form of pandas reading a csv.
# Would not use this library for pdfs again, so I'm not commenting what's below.
def get_pdf_of_stats(data, title, config):
    canvas = Canvas("Trade Analytics " + title + ".pdf")
    trades = csv_to_trades(data, config)
    statss = all_trade_stats(trades, title)
    li = list(statss.split("\n"))
    start = 790
    for i in li:
        canvas.drawString(70, start, i)
        start -= 15
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
    renderPDF.draw(d, canvas, 300, 500, showBoundary=False)
    canvas.save()


from TradingClasses import *
from FunctionsForStats import *
from TradeGraphs import *