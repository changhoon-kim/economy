import datetime

def test_weekday():
    weekday = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    dt = datetime.date(2021, 3, 3)
    dttm = datetime.datetime(year=dt.year, month=dt.month, day=dt.day)

    assert 2 == dttm.weekday()
    assert 'wednesday' == weekday[dttm.weekday()]
