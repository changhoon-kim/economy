import os, datetime

def get_last_n_lines(file_name, N):
    list_of_lines = []
    is_first = True

    with open(file_name, 'rb') as read_obj:
        read_obj.seek(0, os.SEEK_END)

        buffer = bytearray()
        pointer_location = read_obj.tell()
        while pointer_location >= 0:
            read_obj.seek(pointer_location)
            pointer_location = pointer_location -1
            new_byte = read_obj.read(1)

            if new_byte == b'\n':
                if is_first:
                    is_first = False
                    buffer = bytearray()
                else:
                    list_of_lines.append(buffer.decode()[::-1])
                    if len(list_of_lines) == N:
                        return list(reversed(list_of_lines))
                    buffer = bytearray()
            else:
                buffer.extend(new_byte)

        if len(buffer) > 0:
            list_of_lines.append(buffer.decode()[::-1])

    return list(reversed(list_of_lines))

def get_now_hour():
    now = datetime.datetime.now()
    now_hour = now.strftime('%H')

    return int(now_hour)

def get_today_month():
    now = datetime.datetime.now()

    return now.strftime('%Y%m')

def is_first_day_of_month():
    now = datetime.datetime.now()
    now_date = int(now.strftime('%d'))

    if now_date == 1:
        return True

    return False

def get_previous_month():
    today = datetime.date.today()
    first = today.replace(day=1)
    prev_month = first - datetime.timedelta(days=1)

    return prev_month.strftime('%Y%m')

if __name__ == '__main__':
    print get_today_month()
