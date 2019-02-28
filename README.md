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

| **PANDAS TYPE** | **DICT VALUE** |
| :-------------- | -------------: |
| object          | string         |
| int64           | int            |
| float64         | float          |
| bool            | bool           |
| datetime64      | datetime       |
| timedelta       | timedelta      |
| category        | category       |

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

## Grouping 
**NOTE**: `timedelta` and `category` datatypes are not currently supported. 
Sometimes you need a column you can aggregate on with a given data type. For example, you may want 1M rows with one of 4 datetime values (maybe representing 4 observation reporting timestamps?). You can do this using **grouping**.
a grouped column is declared by passing a dict as the data type value with the params for the grouped column as keys. Like this: 

    columns = {"amazing_grouped_column_with_3_values": { "option_count":3, "option_type":"string"}}

This will give you a column with only 3 distinct values and (nearly) equal distribution. 
If you need to control the distribution you can pass the histogram argument. This is useful if, for instance, you want a dataset with 4 datetime values and want one value for 50% of records, another for 30%, and the remaining values 20%. You would delcare this distribution like so: 

    columns = {"super_cool_grouped_column_with_histogram": {"option_count":4, "option_type":"datetime","histogram":(5,3,2,2,)}}

The integers you pass histogram need to add up to 10 with the same number of values as option count (ie. if `option_count` = 5, you need 5 values). This caps option count at 10 currently for histogram. 
Your desired row count must also be divisible by 10 - this keeps the math simple. 


## Contribution
We welcome pull requests!    
