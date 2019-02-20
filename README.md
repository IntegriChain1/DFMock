# DFMock
pandas dataframe mocker for python3. 

## Why? 
Sometimes you just need mock data that is already in pandas datatypes. There are lots of data gen tools out there, but most produce CSVs or some such that needs to be consumed by pandas; this adds a volitile point to your tests. **What if your logic is correct, but the datatypes didn't import correctly from the CSV?** So DFMock aims to generate mock dataframes where the datatypes are controlled. 

## Installation
Use pip
    
    pip install dfmock

You can also get the source [here](git@github.com:IntegriChain1/DFMock.git)

## The API
using is simple. 
import into your module, select your column names and data types, set the number of columns, and generate your frame. 
    from dfmock import DFMock

    columns = { "hamburger":"string",
                "hot_dog":"integer",
                "shoelace":"timedelta"
              }
    dfmock = DFMock(count=100, cols=columns)
    dfmock.generate_dataframe()

    my_mocked_dataframe = dfmock.dataframe

Pandas data types supported:
|pandas type|dict value|
|-----------|----------|
|object     |string    |
|int64      |int       |
|float64    |float     |
|bool       |bool      |
|datetime64 |datetime  |
|timedelta  |timedelta |
|category   |category  |

so to make a dataframe with column "banana" that is an `int64` and "rockstar" that is a `category` type:

    dfmock.cols = {"banana":"int","rockstar":"category"}

pretty simple.

## Grow to Size
sometimes you need your dataset to be a certain memory size instead of row size. The `grow_dataframe_to_size()` allows you to grow a frame until it reaches or passes the given size (in MB). 
Need a 10MB dataframe? 

    dfmock.generate_dataframe()
    dfmock.size
    ## returns 0.2 MB

    dfmock.grow_dataframe_to_size(10)
    dfmock.size
    ## returns ~10 MB

## Contribution
We welcome pull requests!    
