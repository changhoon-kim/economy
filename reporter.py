# -*- coding: utf-8 -*-
import os

from util import get_last_n_lines
from util import is_first_day_of_month
from util import get_today_month
from util import get_previous_month
from push.telegram import Telegram
from push.line import Line
from log import Logger
from model.path import Path

class Reporter:
    def __init__(self):
        self.path = Path()

        self.event_earning_rate_dict = {
            'kodex_200': 0, # KODEX 200
            'kodex_us_S_and_P500': 0, # KODEX 미국S&P500선물(H)
            'tiger_euro_50': 0, # TIGER 유로스탁스50(합성 H)
            'kodex_japan_topix_100': 0, # KODEX 일본TOPIX100
        }

        # NOTE: 예금 금리는 1.5 % 로 고정, 추후 필요하면 Crawler 에서 금리 긁어오도록 수정
        self.deposit_interest_rate = 1.5

    def _get_last_6_month_earning_rate(self, event):
        #TODO: datime time 으로 6개월 전 의 달을 계산 후 해당 달의 첫 번째 거래일로 계산
        #tail 을 한 130~140 개 가져와서 앞에 몇개 살펴 보면 될 듯
        #TODO: trade_history dir 에 거래 날짜별 보유항목, 수량, 현금, 평가금 기록해서 실제로 수행할 시 어떻게 될지 확인
        fpath = '%s/%s' %(self.path.data, event)

        last_data = get_last_n_lines(fpath, 1)[0]
        last_price = int(last_data.split()[1].replace(',', ''))

        ago_6_month_data = get_last_n_lines(fpath, 120)[0]
        ago_6_month_price = int(ago_6_month_data.split()[1].replace(',', ''))

        Logger.info('last data:%s 6 month ago data:%s' %(last_data, ago_6_month_data))
        earning_rate = (float(last_price - ago_6_month_price) / ago_6_month_price) * 100

        return earning_rate

    def _write_monthly_report_item(self, max_item):
        report_date = get_today_month()
        fpath = '%s/%s' %(self.path.report, report_date)
        f = open(fpath, 'w')
        line = '%s\n' % max_item
        f.write(line)
        f.close()

    def _get_previos_monthly_report(self):
        prev_month = get_previous_month()
        fpath = '%s/%s' %(self.path.report, prev_month)

        if not os.path.isfile(fpath):
            return None

        f = open(fpath, 'r')
        prev_item = f.readlines()[0]
        f.close()

        return prev_item.strip()

    def _push_to_user(self, send_text):
        telegram = Telegram()
        telegram.push(send_text)

        line = Line()
        line.push(send_text)

    def monthly_report(self, force=False):
        if not force and not is_first_day_of_month():
            return

        max_item = 'deposit'
        max_rate = self.deposit_interest_rate

        send_text = ''

        for event in self.event_earning_rate_dict:
            earning_rate = self._get_last_6_month_earning_rate(event)
            Logger.info('%s %f'%(event, earning_rate))

            line = '\n[%s]\n최근 6개월 수익률: %.2f\n' %(event, earning_rate)
            send_text = ''.join([send_text, line])
            self.event_earning_rate_dict[event] = earning_rate

            if earning_rate > max_rate:
                max_item = event
                max_rate = earning_rate

        if max_rate == self.deposit_interest_rate:
            Logger.info('All item sell and convert to cash')
            send_text = ''.join([send_text, '\n\n- 모든 항목이 예금 금리보다 아래, 현금 보유\n'])
        else:
            Logger.info('%.2f > %.2f: buy item -> %s' %(max_rate, self.deposit_interest_rate, max_item))
            send_text = ''.join([send_text, '\n\n- 최대 수익률 항목:%s\n'%max_item])

        self._write_monthly_report_item(max_item)
        previos_item = self._get_previos_monthly_report()

        if previos_item == max_item:
            send_text = ''.join([send_text, '- 이전 보유 항목:%s  계속 유지\n'%(previos_item)])
        else:
            send_text = ''.join([send_text, '- 이전 보유 항목:%s\n- %s 항목으로 변경 필요\n'%(previos_item, max_item)])

        self._push_to_user(send_text)
