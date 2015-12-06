#coding: utf8
from tennis.models import infoTournoi
from django.shortcuts import render

def view(request):
    info = infoTournoi.objects.all()
    info = info.order_by("edition")[len(info) - 1]
    edition = info.edition
    last = edition - 1
    date = info.date
    year = date.year
    month = date.month
    print(month)
    month_text = ""
    if month == 1:
        month_text = "janvier"
    elif month == 2:
        month_text = "février"
    elif month == 3:
        month_text = "mars"
    elif month == 4:
        month_text = "avril"
    elif month == 5:
        month_text = "mai"
    elif month == 6:
        month_text = "juin"
    elif month == 7:
        month_text = "juillet"
    elif month == 8:
        month_text = "août"
    elif month == 9:
        month_text = "septembre"
    elif month == 10:
        month_text = "octobre"
    elif month == 11:
        month_text = "novembre"
    elif month == 12:
        month_text = "decembre"
    day = date.day
    return render(request, 'home.html', {'edition':edition, 'last':last, 'year':year, 'month_text':month_text, 'day':day, 'month':month})
