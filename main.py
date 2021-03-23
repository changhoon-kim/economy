# -*- coding: utf-8 -*-

from log import setup_logging
from crawler import Crawler
from reporter import Reporter

if __name__ == '__main__':
    setup_logging()

    crawler = Crawler()
    crawler.get_daily_data()

    reporter = Reporter()
    reporter.monthly_report(force=True)
