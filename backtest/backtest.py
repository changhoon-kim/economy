# -*- coding:utf-8 -*-

# 초기 자본 입력
# 실제 거래 수행하는 것 처럼 테스트
# 매달 수익률도 확인
# 최종 수익률, 최종 금액 확인

import os

item_list = ['kodex_200', 'kodex_us_S_and_P500', 'tiger_euro_50', 'kodex_japan_topix_100']
data_path = os.path.abspath(os.path.join(__file__, '..', '..', 'datas'))

def get_date_info(date):
    sp = date.split('.')
    year = int(sp[0])
    month = int(sp[1])
    day = int(sp[2])

    return year, month, day

def get_first_month():
    max_year = 0
    max_month = 0
    max_day = 0

    for item in item_list:
        fpath = '%s/%s' %(data_path, item)

        f = open(fpath, 'r')
        line = f.readline()
        f.close()

        date = line.split()[0]
        year, month, day = get_date_info(date)

        if year > max_year:
            max_year = year
            max_month = month
            max_day = day
        elif year == max_year:
            if month > max_month:
                max_year = year
                max_month = month
                max_day = day
            elif month == max_month:
                if day > max_day:
                    max_year = year
                    max_month = month
                    max_day = day

    return max_year, max_month + 1

def get_earing_rate(prev_price, curr_price):
    return (float(curr_price - prev_price) / prev_price) * 100

def adjust_month(month):
    if month > 12:
        return month - 12

    return month

def get_monthly_price_dict(first_year, first_month):
    monthly_price_list = {}
    for item in item_list:
        data_list = []
        prev_month = 0
        fpath = '%s/%s' %(data_path, item)
        f = open(fpath, 'r')
        for line in f.readlines():
            date = line.split()[0]
            year, month, _ = get_date_info(date)

            if year < first_year:
                continue
            if year == first_year and month < adjust_month(first_month + 1):
                prev_month = month
                continue

            if month == adjust_month(prev_month + 1):
                price = int(line.split()[1].replace(',', ''))
                data_list.append(price)

                prev_month = month
        f.close()

        monthly_price_list[item] = data_list

    return monthly_price_list

def get_daily_price_dict(first_year, first_month):
    daily_price_list = {}
    for item in item_list:
        data_list = []
        fpath = '%s/%s' %(data_path, item)
        f = open(fpath, 'r')
        for line in f.readlines():
            date = line.split()[0]
            year, month, _ = get_date_info(date)

            if year < first_year:
                continue
            if year == first_year and month < adjust_month(first_month + 1):
                continue

            price = int(line.split()[1].replace(',', ''))
            data_list.append(price)
        f.close()

        daily_price_list[item] = data_list

    return daily_price_list

def get_current_earing_rate(origin_cash, trade_price, current_item, current_count, current_cash):
    if current_item:
        current_cash += trade_price[current_item] * current_count

    return (float(current_cash - origin_cash) / origin_cash) * 100

def simulation(price_dict, index):
    origin_cash = 5000000
    current_item = None
    current_cash = origin_cash
    current_count = 0
    while True:
        trade_price = {}
        max_earing_rate = 1.5
        max_item = 'deposit'
        for item in price_dict:
            price_list = price_dict[item]
            trade_price[item] = price_list[index]
            earning_rate = get_earing_rate(price_list[index-6], price_list[index])

            if earning_rate > max_earing_rate:
                max_earing_rate = earning_rate
                max_item = item

        if max_item == 'deposit':
            if current_item:
                current_cash += trade_price[current_item] * current_count
                current_count = 0
                current_item = None
                print '모든 항목이 예금금리 밑으로 다 팔고 현금 보유, 현금: %d' %(current_cash)
            else:
                print '현재 현금 보유 중 현금 보유 유지. 현금: %d' %(current_cash)
        else:
            if max_item != current_item:
                before_item = current_item
                if current_item:
                    current_cash += trade_price[current_item] * current_count
                current_count = current_cash / trade_price[max_item]
                current_cash -= trade_price[max_item] * current_count
                current_item = max_item
                print '다른 항목이 수익률이 높아 항목 변경. 변경 전: %s 변경 후: %s 보유량:%d 매입가: %d 주식금액: %d 현금:%d 평가금액: %d' %(before_item, current_item, current_count, trade_price[current_item], current_count * trade_price[current_item], current_cash, current_cash + current_count * trade_price[current_item])
            else:
                print '현재 보유 중인 항목을 유지. 항목: %s 보유량: %d 주식금액: %d, 현금: %d 평가금액: %d' %(current_item, current_count, current_count * trade_price[current_item], current_cash, current_cash + current_count * trade_price[current_item])

        print '현재까지 수익률: %s' %(get_current_earing_rate(origin_cash, trade_price, current_item, current_count, current_cash))

        index += 1
        if index == len(price_dict[item_list[0]]):
            break

if __name__ == '__main__':
    first_year, first_month = get_first_month()
    monthly_price_dict = get_monthly_price_dict(first_year, first_month)
    daily_price_dict = get_daily_price_dict(first_year, first_month)

    #simulation(monthly_price_dict, 6)
    simulation(daily_price_dict, 120)
