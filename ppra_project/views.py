import json
import requests
from bs4 import BeautifulSoup
from django.db import connection, connections
from django.http import HttpResponse


def get_html_data(request):
    url = "http://irrigation.punjab.gov.pk/Search.aspx"
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    print('github testing')
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Content-Type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    soup = get_page_response_soup(soup, headers, 'rdbsearchtype$0', '', url)
    # arr_divisions = list(TblDivision.objects.all().values())
    # for d in arr_divisions:
    #     soup_division = get_page_response_soup(soup, headers, d['division_event_target'], '', url)
    #     # insert_names_and_targets(soup, d)
    #     arr_channels = list(TblChannel.objects.all().values())
    #     for c in arr_channels:
    #         soup_channel = get_page_response_soup(soup_division, headers, c['channel_event_target'], '', url)
    #         for t in range(6784, 6800):
    #             soup = get_page_response_soup(soup_channel, headers, 'datecal','6789','http://irrigation.punjab.gov.pk/livedata.aspx')
    #
    #
    #             insert_names_and_targets(soup_channel, c, t)


# soup = get_page_response_soup(soup, headers, 'dgdivision$_ctl2$_ctl0', '', url)
# soup = get_page_response_soup(soup, headers, 'dgchannel$_ctl2$_ctl0', '', url)
# soup = get_page_response_soup(soup, headers, 'datecal', '6787', url)
    print(soup.prettify())
    return HttpResponse('Go ahead')


# def convert_excel_date_format(t):
#     # excel_date = 6550
#     dt = datetime.fromordinal(datetime(2000, 1, 1).toordinal() + t)
#     tt = dt.date()
#     return tt
#
#
# def insert_names_and_targets(soup, row, t):
#     soup.find_all('table', width="100%")
#     channel_id = TblChannel.objects.filter(id=row['id']).get()
#     # date_discharge = t
#     date_discharge = convert_excel_date_format(t)
#
#     frm_json = {}
#     for input in soup.find_all('input')[7:28]:
#         frm_json[input.get('name')] = input.get('value')
#     frm_json['channel_id'] = channel_id
#     frm_json['discharge_date'] = date_discharge
#     channel_obj = TblChannelDetail(**frm_json)
#     channel_obj.save(force_insert=True)


# dg = soup.find_all(id=re.compile("dg"))[1]
# for form in dg.find_all('a'):
#     obj = []
#     for i in form:
#         eventtarget_insert = (form.get('href').split("'")[1])
#         name_insert = form.text
#         channel_id = row['id']
#         div_obj = TblDivision.objects.filter(id=channel_id).get()
#         div_obj = TblDivision(division_name=name_insert, division_event_target=eventtarget_insert)
#         div_obj.save(force_insert=True)
#         channel_obj = TblChannel(channel_name=name_insert, channel_event_target=eventtarget_insert, div_id=div_obj)
#         channel_obj.save(force_insert=True)


def get_form_data(soup):
    form = soup.find_all('form')[0]
    frm_json = {}
    for input in form.find_all('input'):
        frm_json[input.get('name')] = input.get('value')
    return frm_json


def get_page_response_soup(soup, headers, EVENTTARGET, EVENTARGUMENT, url):
    formfields = get_form_data(soup)
    formfields['__EVENTTARGET'] = EVENTTARGET
    formfields['__EVENTARGUMENT'] = EVENTARGUMENT

    # if EVENTARGUMENT == '':
    #     formfields['rdbsearchtype'] = '1'
    # else:
    #     formfields['LiveReportViewer:_ctl0'] = ''
    #     formfields['LiveReportViewer:_ctl4'] = ''
    #     formfields['LiveReportViewer:_ctl5'] = ''
    #     formfields['LiveReportViewer:_ctl6'] = 1

    res = requests.post(url, data=formfields, headers=headers).text
    soup = BeautifulSoup(res, "html.parser")
    return soup


def execute_query(str_query):
    # connection = connections['']
    cursor = connection.cursor()
    try:
        cursor.execute(str_query)
        return True
    except SyntaxError:
        return False


def getJSONFromDB(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    data = dictfetchall(cursor)
    data_json = json.dumps(data, default=date_handler)
    return data_json


def dictfetchall(cursor):
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
            ]


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)

# def get_hierarchy_page(request, template=loader.get_template('hierarchy.html')):
#     return HttpResponse(template.render({}, request))
