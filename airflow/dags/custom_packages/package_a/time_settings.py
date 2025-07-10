from datetime import datetime as dt


class TimeSettings:
    @staticmethod
    def current_time():
        return dt.now()
