import math
import csv
from datetime import datetime

# IMPORTED from __main__ BSE.py
def schedule_offsetfn_read_file(filename, col_t, col_p, scale_factor=75):
    """
    Read in a CSV data-file for the supply/demand schedule time-varying price-offset value
    :param filename: the CSV file to read
    :param col_t: column in the CSV that has the time data
    :param col_p: column in the CSV that has the price data
    :param scale_factor: multiplier on prices
    :return: on offset value event-list: one item for each change in offset value
            -- each item is percentage time elapsed, followed by the new offset value at that time
    """
    
    vrbs = True
    
    # does two passes through the file
    # assumes data file is all for one date, sorted in time order, in correct format, etc. etc.
    rwd_csv = csv.reader(open(filename, 'r'))
    
    # first pass: get time & price events, find out how long session is, get min & max price
    minprice = None
    maxprice = None
    firsttimeobj = None
    timesincestart = 0
    priceevents = []
    
    first_row_is_header = True
    this_is_first_row = True
    this_is_first_data_row = True
    first_date = None
    
    for line in rwd_csv:
        
        if vrbs:
            print(line)
        
        if this_is_first_row and first_row_is_header:
            this_is_first_row = False
            this_is_first_data_row = True
            continue
            
        row_date = line[col_t][:10]
        
        if this_is_first_data_row:
            first_date = row_date
            this_is_first_data_row = False
            
        if row_date != first_date:
            continue
            
        time = line[col_t][11:19]
        if firsttimeobj is None:
            firsttimeobj = datetime.strptime(time, '%H:%M:%S')
            
        timeobj = datetime.strptime(time, '%H:%M:%S')
        
        price_str = line[col_p]
        # delete any commas so 1,000,000 becomes 1000000
        price_str_no_commas = price_str.replace(',', '')
        price = float(price_str_no_commas)
        
        if minprice is None or price < minprice:
            minprice = price
        if maxprice is None or price > maxprice:
            maxprice = price
        timesincestart = (timeobj - firsttimeobj).total_seconds()
        priceevents.append([timesincestart, price])
        
        if vrbs:
            print(row_date, time, timesincestart, price)
        
    # second pass: normalise times to fractions of entire time-series duration
    #              & normalise price range
    pricerange = maxprice - minprice
    endtime = float(timesincestart)
    offsetfn_eventlist = []
    for event in priceevents:
        # normalise price
        normld_price = (event[1] - minprice) / pricerange
        # clip
        normld_price = min(normld_price, 1.0)
        normld_price = max(0.0, normld_price)
        # scale & convert to integer cents
        price = int(round(normld_price * scale_factor))
        normld_event = [event[0] / endtime, price]
        if vrbs:
            print(normld_event)
        offsetfn_eventlist.append(normld_event)
    
    return offsetfn_eventlist


def schedule_offsetfn_from_eventlist(time, params):
    """
    Returns a price offset-value for the current time, by reading from an offset event-list.
    :param time: the current time
    :param params: a list of parameter values...
        params[1] is the final time (the end-time) of the current session.
        params[2] is the offset event-list: one item for each change in offset value
                    -- each item is percentage time elapsed, followed by the new offset value at that time
    :return: integer price offset value
    """

    final_time = float(params[0])
    offset_events = params[1]
    # this is quite inefficient: on every call it walks the event-list
    percent_elapsed = time/final_time
    offset = None
    for event in offset_events:
        offset = event[1]
        if percent_elapsed < event[0]:
            break
    return offset


def schedule_offsetfn_increasing_sinusoid(t, params):
    """
    Returns sinusoidal time-dependent price-offset, steadily increasing in frequency & amplitude
    :param t: time
    :param params: set of parameters for the offsetfn: this is empty-set for this offsetfn but nonempty in others
    :return: the time-dependent price offset at time t
    """
    if params is None:  # this test of params is here only to prevent PyCharm from warning about unused parameters
        pass
    scale = -7500
    multiplier = 7500000    # determines rate of increase of frequency and amplitude
    offset = ((scale * t) / multiplier) * (1 + math.sin((t*t)/(multiplier * math.pi)))
    return int(round(offset, 0))


# FLASH CRASH OFFSET FUNCTION 
def schedule_offsetfn_with_flash_crash(time, params):
    """
    Wraps schedule_offsetfn_from_eventlist, adding a flash crash offset
    during a specified time window.
    
    :param time: float, current time in seconds
    :param params: list or tuple with the following structure:
        [
          base_end_time,   # same as used by schedule_offsetfn_from_eventlist
          offset_events,   # same as used by schedule_offsetfn_from_eventlist
          flash_start,     # time at which the crash starts
          flash_end,       # time at which the crash ends
          flash_offset     # how big to offset the price. Usually negative for a crash
        ]
    :return: integer offset
    """

    base_end_time   = params[0]
    offset_events   = params[1]
    flash_start     = params[2]
    flash_end       = params[3]
    flash_offset    = params[4] 

    # get normal offset
    normal_offset = schedule_offsetfn_from_eventlist(time, [base_end_time, offset_events])

    # check if time is in the flash crash window
    if flash_start <= time <= flash_end:
        return normal_offset + flash_offset # flash crash: add extra offset
    else:
        return normal_offset


