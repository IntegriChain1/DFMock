import random
import sys
import pandas as pd
from string import ascii_lowercase as low_letters
from datetime import datetime
## TODO: this needs a logging module

class DFMock:
    " sample dataframe maker."

    def __init__(self, count:int = 100, columns:dict = dict())->None:
        self._count = count
        self._columns = columns

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, columns:dict)->None:
        """ sets the column names and types for the dataframe.
            ARGS:
                - columns (dict) a dictionary in the format {name:datatype}
        """
        VALID_DATATYPES = ("string","int","float","bool","timedelta","datetime","category")
        for k,v in columns.items():
            if v.lower() not in VALID_DATATYPES:
                raise ValueError(f"{v} is not a valid data type. Valid data types are: {','.join(VALID_DATATYPES)}")
        self._columns = columns      

    @property
    def size(self)->float:
        return str(round(sys.getsizeof(self._dataframe)/1e+6,2)) + " MB"

    @property
    def count(self)->int:
        return self._count

    @count.setter
    def count(self,count:int)->None:
        self._count = int(count)

    @property
    def dataframe(self):
        if hasattr(self,'_dataframe'):
            return self._dataframe 
        else:
            raise ValueError("dataframe has not yet been created. Run generate_dataframe first.")

    def grow_dataframe_to_size(self,size:int)->None:
        """ appends rows to the frame until it reaches or exceeds the size (in MB)"""
        size = size * 1e+6 
        def grower(frame:pd.DataFrame)->pd.DataFrame:
            cur_size = sys.getsizeof(frame)
            if cur_size >= size:
                return frame
            else: 
                return grower(frame.append(self._generate_dataframe()))
        sized_frame = grower(self._dataframe)
        self._dataframe = sized_frame

    def _generate_dataframe(self)->pd.DataFrame:
        dataframe = pd.DataFrame()
        for key, value in self._columns.items():
            v = value.lower()
            k = key.lower()
            if v == "string":
                dataframe[k] = self._mock_string(count=self._count)
            elif v == "int":
                dataframe[k] = self._mock_integer(count=self._count)
            elif v == "float":
                dataframe[k] = self._mock_float(count=self._count)
            elif v == "bool":
                dataframe[k] = self._mock_bool(count=self._count)
            elif v == "timedelta":
                dataframe[k] = self._mock_timedelta(count=self._count)
            elif v == "datetime":
                dataframe[k] = self._mock_datetime(count=self._count)
        return dataframe

    def generate_dataframe(self)->None:
        self._dataframe = self._generate_dataframe()

    def _mock_integer(self, count:int)->list:
        return [random.randrange(1000000) for x in range(0,count)]

    def _mock_float(self, count:int)->list:
        return [float(random.random()) for x in range(0,count)]

    def _mock_boolean(self, count:int)->list:
        return [random.choice((True,False)) for x in range(0,count)]

    def _mock_category(self, count:int)->pd.Categorical:
        #TODO: this should accept variable for the number of category elements
        category_elements = ["a","b","c"]
        category_content = [random.sample(category_elements,k=1)[0] for x in range(0,count)]
        return pd.Categorical(category_content, categories=category_elements)

    def _mock_timedelta(self, count:int)->list:
        def make_rand_td():
            days = random.randrange(100)
            hours = random.randrange(12)
            seconds = random.randrange(60)
            return pd.Timedelta(days=days,hours=hours,seconds=seconds)
        return[make_rand_td() for x in range(0,count)]

    def _mock_string(self, count:int, min_len:int = 10, max_len:int = 40)-> list:
        def make_rand_string():
            length = random.randrange(min_len, max_len)
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
