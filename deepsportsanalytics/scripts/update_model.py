''' Update current predictable model with fresh data '''

if __name__ == '__main__':
    l = logging.getLogger()
    l.setLevel(logging.INFO)
    l.addHandler(logging.StreamHandler())

    utc_date_now = datetime.datetime.date(datetime.datetime.utcnow())
    update(utc_date_now - datetime.timedelta(days=6))
