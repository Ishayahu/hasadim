# -*- coding:utf-8 -*-
# coding=<utf8>

import datetime, re

def htmlize(text=''):
    r"""
    Функция для преобразования разметки в html код

    >>> a="*bold* **italic** http://site.com https://site.com https://site.com/page.php"
    >>> htmlize(a)
    '<b>bold</b> <i>italic</i> <a href="http://site.com">http://site.com</a> <a href="https://site.com">https://site.com</a>  <a href="https://site.com/page.php">https://site.com/page.php</a>'

    TODO: добавить тестирование таблицы
    """
    # print 'in htmlize',text.encode('koi8-r')
    links = re.findall(r'https?://\S*',text)
    # links += re.findall(r'https://\S*',text)       
    html = ''
    # заменяем \r\n на \n для более простой обработки построения страницы. На выводе это никак не сказывается
    text = text.replace('\r\n','\n')
    inBold = False
    inItalic = False
    # для таблицы
    inTable = False
    inRow = False
    inCell = False
    tegs = {True:'</', False:'<'}
    count = 0
    while count < len(text):
        if text[count] == '\n' and not inTable:
            html += '<br />'
        elif text[count] == '*' and count+1<len(text) and text[count+1] != '*':
            html = html + tegs[inBold] + 'b>'
            inBold = not inBold
        elif text[count] == '*' and count+1<len(text) and text[count+1] == '*':
            html = html + tegs[inItalic] + 'i>'
            count +=1
            inItalic = not inItalic
        elif text[count] == '*' and inBold:
            html = html + '</b>'
        elif text[count] == '\\' and count+1==len(text):
            html += '\\'
        elif text[count] == '\\':
            html += text[count+1]
            count += 1
        elif text[count] == '<':
            html += '&lt'
            # count +=1
        elif text[count] == '>':
            html += '&gt'
            count +=1
        elif text[count] == '&':
            html += '&amp'
            # count +=1
        # обработка создания таблиц
        elif count+3<len(text) and text[count]=='|' and text[count+1]=='|':
            # обрабатываем создание начала таблицы
            if (text[count-1]=='\n' or count-1<0) and not inTable:
                html += '<table border="1"><tr><td>'
                inTable = True
                inRow = True
                inCell = True
            elif inTable and not inRow:
                html += '<tr><td>'
                inRow = True
                inCell = True
            elif inCell:
                if text[count+2]!='\n':
                    html+='</td><td>'
                    inCell = True
                if text[count+2] == '\n':
                    html+='</td></tr>'
                    inCell = False
                    inRow=False
                    count+1
                    if text[count+3]!='|':
                        html+='</table>'
                        inTable=False
            count+=1
        elif (count+2>=len(text) and inTable) or (count+3<len(text) and text[count+2]=='\n' and inTable and text[count+3]!='|'):
            if inCell:
                html += '</td>'
                inCell = False
            if inRow:
                html += '</tr>'
                inRow = False
            html+='</table>'
            inTable = False
            count+=1
            
        else:
            html += text[count]
        count +=1
    # Преобразуем в множество, чтобы каждый url заменять только один раз
    # Затем упорядочиваем по длине, чтобы не было двойного замещения. например
    # ['http://www.youtube.com/embed/RRpDn5qPp3s?', 'https://www.youtube.com', 'http://www.youtube.com']
    # В таком случае, после того, как уже заменят первый элемент, в нём снова будут замены при обработке последнего
    # элемента
    print links
    links = sorted(list(set(links)),key = lambda x: len(x))
    print links
    for link in links:
        html = html.replace(link.replace('&','&amp'),'<a href="'+link+'">'+link+'</a>')
    return html
def what_to_people_friendly(a):
    """
    Функция для преобразования списка покупок в человеческий вид

    >>> a='a;a;b;a;b;a'
    >>> what_to_people_friendly(a)
    u'a - 4 \u0448\u0442; b - 2 \u0448\u0442; '
    """
    b=list(set(a.split(';')))
    c = ''
    for word in b:
        count=a.split(';').count(word)
        c = c + word + ' - ' + str(count) + u' шт; '
    return c