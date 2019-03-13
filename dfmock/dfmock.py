import math
import random
import sys
import pandas as pd
from string import ascii_lowercase as low_letters
from datetime import datetime
import logging


class DFMock:
    " sample dataframe maker."
    logger = logging.getLogger(__name__)

    def __init__(self, count: int = 100, columns: dict = dict())->None:
        self._count = count
        self._columns = columns

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, columns: dict)->None:
        """ sets the column names and types for the dataframe.
            ARGS:
                - columns (dict) a dictionary in the format {name:datatype}
        """
        VALID_DATATYPES = ("string", "int", "integer", "float",
                           "bool", "boolean", "timedelta", "datetime", "category")
        for k, v in columns.items():
            if (not isinstance(v, dict) and v.lower() not in VALID_DATATYPES):
                invalid_message = f"{v} is not a valid data type. Valid data types are: {','.join(VALID_DATATYPES)} OR a dict for grouping columns"
                self.logger.critical(invalid_message)
                raise ValueError(invalid_message)
        self._columns = columns

    @property
    def size(self)->float:
        return str(round(sys.getsizeof(self._dataframe)/1e+6, 2)) + " MB"

    @property
    def count(self)->int:
        return self._count

    @count.setter
    def count(self, count: int)->None:
        self._count = int(count)

    @property
    def dataframe(self):
        if hasattr(self, '_dataframe'):
            return self._dataframe
        else:
            raise ValueError(
                "dataframe has not yet been created. Run generate_dataframe first.")

    def grow_dataframe_to_size(self, size: int)->None:
        """ appends rows to the frame until it reaches or exceeds the size (in MB)"""
        
        self.logger.debug(f"Growing dataframe to {size}MB.")
        size = size * 1<<20
        current_size = float(sys.getsizeof(self._dataframe))
        
        num_iterations = math.ceil(size/current_size)

        frame = self._dataframe
        self.logger.info(f"Growing dataframe {num_iterations} times...")
        for x in range(num_iterations):
            self._dataframe = pd.concat([self._dataframe, frame])
        self.logger.info("Done.")

    def _generate_dataframe(self)->pd.DataFrame:
        dataframe = pd.DataFrame()
        for key, value in self._columns.items():
            if isinstance(value, dict):
                dataframe[key] = self._mock_grouping(count=self._count,
                                                     option_count=value['option_count'],
                                                     option_type=value['option_type'], histogram=value.get('histogram', None))
            else:
                v = value.lower()
                k = key.lower()
                if v == "string":
                    dataframe[k] = self._mock_string(count=self._count)
                elif v in ("int", "integer"):
                    dataframe[k] = self._mock_integer(count=self._count)
                elif v == "float":
                    dataframe[k] = self._mock_float(count=self._count)
                elif v in ("bool", "boolean"):
                    dataframe[k] = self._mock_boolean(count=self._count)
                elif v == "timedelta":
                    dataframe[k] = self._mock_timedelta(count=self._count)
                elif v == "category":
                    dataframe[k] = self._mock_category(count=self._count)
                elif v == "datetime":
                    dataframe[k] = self._mock_datetime(count=self._count)
        return dataframe

    def generate_dataframe(self)->None:
        self._dataframe = self._generate_dataframe()

    def _mock_grouping(self, count: int, option_count: int, option_type: str, histogram: iter = None)->list:

        def option_switch(option_type, option_count):
            if option_type == "string":
                opt_set = self._mock_string(count=option_count)
            elif option_type in ("int", "integer"):
                opt_set = self._mock_integer(count=option_count)
            elif option_type == "float":
                opt_set = self._mock_float(count=option_count)
            elif option_type in ("bool", "boolean"):
                opt_set = self._mock_boolean(count=option_count)
            elif option_type == "timedelta":
                raise NotImplementedError("Timedelta datatype is not supported for groupings at this time.")
            elif option_type == "category":
                raise NotImplementedError("Category datatype is not supported for groupings at this time.")
            elif option_type == "datetime":
                opt_set = self._mock_datetime(count=option_count)
            else:
                raise ValueError(
                    f"Invalid datatype set for grouping column: {option_type}")
            return opt_set

        if histogram is not None:
            hist_error = """ To use histogram, make sure that:
- your count is a multiple of 10
- you pass an iterable
- the number of values in the iterable matches option_count
- the values are integers 0 < 10
- the values sum to exactly 10
"""
            if (len(histogram) != option_count) or (count % 10 != 0):
                raise ValueError(
                    hist_error + f" : {len(histogram)} hist values, {option_count} options")
            hist_list = []
            for hist_count in histogram:
                hist_row = option_switch(option_type, 1)
                hist_list = hist_list + (hist_row * hist_count)
            multiple = int(count/len(hist_list))
            return hist_list * multiple

        # if no histogram, return the opt set
        opt_set = option_switch(option_type, option_count)
        multiple = int(math.ceil(count/option_count))
        
        oversized_list = opt_set * multiple
        return oversized_list[:count]

    def _mock_integer(self, count: int)->list:
        return [random.randrange(1000000) for x in range(0, count)]

    def _mock_float(self, count: int)->list:
        return [float(random.random()) for x in range(0, count)]

    def _mock_boolean(self, count: int)->list:
        return [random.choice((True, False)) for x in range(0, count)]

    def _mock_category(self, count: int)->pd.Categorical:
        # TODO: this should accept variable for the number of category elements
        category_elements = ["a", "b", "c"]
        category_content = [random.sample(category_elements, k=1)[
            0] for x in range(0, count)]
        return pd.Categorical(category_content, categories=category_elements)

    def _mock_timedelta(self, count: int)->list:
        def make_rand_td():
            days = random.randrange(100)
            hours = random.randrange(12)
            seconds = random.randrange(60)
            return pd.Timedelta(days=days, hours=hours, seconds=seconds)
        return[make_rand_td() for x in range(0, count)]

    def _mock_string(self, count: int, min_len: int = 10, max_len: int = 40)-> list:
        def make_rand_string():
            length = random.randrange(min_len, max_len)
            string = ''
            for char in range(0, length):
                string += random.sample(low_letters, k=1)[0]
            return string
        return [make_rand_string() for x in range(0, count)]

    def _mock_datetime(self, count: int, year_start: int = 2000, allow_future: bool = True)-> list:
        """ makes random datetimes
            ARGS:
                - count(int) the number of records to make
                - year_start(int) the earliest year allowed in the set
                - allow_future(bool) if false, all records are < current date
        """
        dates = []
        for x in range(0,count):
            year,mon,day,hour,minute,second,tz = self._make_ts_vals(year_start,allow_future)
            dates.append(datetime(int(year),int(mon),int(day),int(hour),int(minute)))
        return dates
            

    def _mock_timestamp(self, count: int, year_start: int = 2000, allow_future: bool = True)-> list:
        """ makes random pandas timestamps.
            ARGS:
                - count(int) the number of records to make
                - year_start(int) the earliest year allowed in the set
                - allow_future(bool) if false, all records are < current date
        """
        return [pd.Timestamp(ts_input="{}/{}/{} {}:{}:{} {}".format(self._make_ts_vals(year_start,allow_future))) for x in range(0, count)]

    def _make_ts_vals(self, year_start: int, allow_future: bool)-> tuple:
        """ Generates the random data for date / ts vals"""

        current = datetime.now()
        tz = random.sample(["+4", "+5", "-8"], k=1)[0]
        year_end = current.year if not allow_future else 2100
        year = random.randrange(year_start, year_end)
        # TODO: this is a hack way to enforce allow_future. make less hacky please!
        max_month = current.month - 1 if not allow_future else 12
        mon = str(random.randrange(1, 12)).rjust(2, '0')
        day = str(random.randrange(1, 28)).rjust(2, '0')
        hour = str(random.randrange(0, 23)).rjust(2, '0')
        sixty = str(random.randrange(60)).rjust(2, '0')
        
        return tuple([year, mon, day, hour, sixty, sixty, tz])


