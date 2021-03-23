# -*- coding: utf8 -*-

import requests, sys, os

from bs4 import BeautifulSoup
from util import get_last_n_lines
from util import get_now_hour
from log import Logger

class Crawler:
    def __init__(self):
        self.data_path = os.path.abspath(os.path.join(__file__, '..', 'datas'))

        self.event_code_dict = {
            'kodex_200': '069500', # KODEX 200
            'kodex_us_S_and_P500': '219480', # KODEX 미국S&P500선물(H)
            'tiger_euro_50': '195930', # TIGER 유로스탁스50(합성 H)
            'kodex_japan_topix_100': '101280', # KODEX 일본TOPIX100
        }

        if not os.path.isfile('%s/done_init_data'%self.data_path):
            os.makedirs(self.data_path)
            self._get_historical_data()

    def _get_page_datas(self, url):
        datas = []

        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        trs = soup.find_all('tr')
        for tr in trs :
            tds = tr.find_all('td')

            data = {}
            count = 0
            for td in tds:
                span = td.span
                if span is None:
                    continue

                val = span.string

                if count == 0:
                    data['date'] = val
                elif count == 1:
                    data['closing_price'] = val

                count += 1

            if 'date' in data and 'closing_price' in data:
                datas.append(data)

        last_page = 0
        pgrr = soup.find('td', class_='pgRR')
        if pgrr is not None:
            link = pgrr.find('a').get('href')
            last_page = int(link.split('=')[2])

        return datas, last_page

    def _make_done_file(self):
        fpath = '%s/done_init_data' % self.data_path
        f = open(fpath, 'w')
        f.close()

    def _write_event_data(self, event, datas):
        datas.reverse()

        fname = '%s/%s' %(self.data_path, event)
        f = open(fname, 'w')

        for data in datas:
            date = data['date']
            closing_price = data['closing_price']
            line = '%s %s\n' %(date, closing_price)
            f.write(line)

        f.close()

    def _get_historical_data(self):
        base_url = 'https://finance.naver.com/item/sise_day.nhn?code=%s&page=%d'
        for event, code in self.event_code_dict.iteritems():
            ratio = 0
            page = 1
            datas = []
            while True:
                url = base_url %(code, page)
                page_datas, last_page = self._get_page_datas(url)
                datas.extend(page_datas)
                page += 1

                if page > last_page:
                    break

                new_ratio = int((float(page) / last_page) * 100)
                if new_ratio - ratio > 1:
                    ratio = new_ratio
                    Logger.info('proc: %s %d%%' %(event, ratio))

            self._write_event_data(event, datas)

        self._make_done_file()

    def _get_last_date_in_local(self, event):
        fpath = '%s/%s' %(self.data_path, event)
        last_data = get_last_n_lines(fpath, 1)[0]
        last_date = last_data.split()[0]

        return last_date

    def _add_recent_data(self, event, date, price):
        fname = '%s/%s' %(self.data_path, event)
        f = open(fname, 'a')
        line = '%s %s\n' %(date, price)
        f.write(line)
        f.close()

    def _is_market_closed(self):
        starting_hour = 9
        closing_hour = 17
        now_hour = get_now_hour()
        if starting_hour < now_hour and now_hour < closing_hour:
            return False

        return True

    def get_daily_data(self):
        if not self._is_market_closed():
            Logger.info('market not closed')
            return

        base_url = 'https://finance.naver.com/item/sise_day.nhn?code=%s&page=1'
        for event, code in self.event_code_dict.iteritems():
            url = base_url % code

            page_datas, _ = self._get_page_datas(url)
            recent_data = page_datas[0]
            recent_date = recent_data['date']
            recent_price = recent_data['closing_price']

            Logger.info('recent data: %s %s' %(recent_date, recent_price))
            if recent_date == self._get_last_date_in_local(event):
                Logger.info('last local date and recent date has same value. %s', recent_date)
                return

            self._add_recent_data(event, recent_date, recent_price)
