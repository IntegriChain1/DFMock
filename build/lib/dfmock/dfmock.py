import random
import pandas as pd
from string import ascii_lowercase as low_letters
## TODO: logging module
import logging
from datetime import datetime

class DFMock:
    " sample dataframe maker."
    """
    def __init__(self, count:int = 100)->None:
        self._data = pd.DataFrame({ "time_of_event":self._random_timestamp(count),
                                    "event_name":self._random_string(count)}
                          )
    """   
    @property
    def count(self)->int:
        return self._count

    @count.setter
    def count(self,count:int)->None:
        self._count = int(count)


    @property
    def data(self):
        return self._data  



    def _generate_dataframe(self)->None:
        ""

    def _random_string(self, count:int)-> list:
        def make_rand_string():
            length = random.randrange(10,40)
            string = ''
            for char in range(0,length):
                string += random.sample(low_letters,k=1)[0]
            return string
        return [make_rand_string() for x in range(0,count)]

    def _mock_datetime(self, count:int, year_start:int = 2000, allow_future:bool = True)-> list:
        """ makes random pandas timestamps.
            ARGS:
                - count(int) the number of records to make
                - year_start(int) the earliest year allowed in the set
                - allow_future(bool) if false, all records are < current date
        """
        def make_ts():
            current = datetime.now()
            tz = random.sample(["+4", "+5", "-8"], k=1)[0]
            year_end = current.year if not allow_future else 2100
            year = random.randrange(year_start, year_end)
            ## TODO: this is a hack way to enforce allow_future. make less hacky please!
            max_month = current.month -1 if not allow_future else 12
            mon = str(random.randrange(1,12)).rjust(2,'0')
            day = str(random.randrange(1,28)).rjust(2,'0')
            hour = str(random.randrange(0,23)).rjust(2,'0')
            sixty = str(random.randrange(60)).rjust(2,'0')
            ts_string = f"{year}/{mon}/{day} {hour}:{sixty}:{sixty} {tz}"
            return pd.Timestamp(ts_input=ts_string)
            
        return [make_ts() for x in range(0,count)]
