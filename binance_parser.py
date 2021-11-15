def get_binance_data(symbol, timeframe, length, include_current_candle = True, file_format = ['txt', 'csv'], api_cooldown_seconds = 0):

    data_limit = 500 

    binance_symbols = [market['symbol'] for market in ccxt.binance({}).fetch_markets()]
    binance_timeframes = {'1m': 60*1000, '3m': 3*60*1000, '5m': 5*60*1000, '15m': 15*60*1000, '30m': 30*60*1000, '1h': 60*60*1000, '2h': 2*60*60*1000, '4h': 4*60*60*1000, '6h': 6*60*60*1000, '12h': 12*60*60*1000, '1d': 24*60*60*1000, '3d': 3*24*60*60*1000, '1w': 7*24*60*60*1000}
    missing_timeframes = {'3h': ['1h', 3, 60*60*1000], '2w': ['1w', 2, 7*24*60*60*1000]}

    timestamp = []
    openx = []
    high = []
    low = []
    close = []
    volume = []

    timestamp_temp = []
    openx_temp = []
    high_temp = []
    low_temp = []
    close_temp = []
    volume_temp = []
    
    proceed = True

    if symbol not in binance_symbols:
        print("ERROR:\tPlease use one of the following Symbols:\n\t" + "\n\t".join(sorted(binance_symbols)))
        proceed = False

    if not(timeframe in binance_timeframes.keys() or timeframe in missing_timeframes.keys()):
        print("ERROR:\tPlease use one of the following Timeframes:\n\tMinute:\t'1m', '3m', '5m', '15m', '30m',\n\tHour:\t'1h', '2h', '3h', '4h', '6h', '12h',\n\tDay:\t'1d', '3d',\n\tWeek:\t'1w', '2w'")
        proceed = False
        
    if not isinstance(length, int) or length < 1:
        print("ERROR:\tPlease use a reasonable number for the argument 'length'.")
        proceed = False

    if type(include_current_candle) != bool:
        print("ERROR:\tPlease use boolean values for argument 'include_current_candle' only.")
        proceed = False

    if not(file_format == 'txt' or file_format == 'csv' or file_format == ['txt'] or file_format == ['csv'] or file_format == ['csv', 'txt'] or file_format == ['txt', 'csv'] or
            file_format == '' or file_format == [] or file_format == [''] or file_format == None):
        print("ERROR:\tAllowed values for argument 'file_format' are 'csv', 'txt', ['csv', 'txt'].\n\tIf you do not wish to save the data please use either '', [''], [], None.")
        proceed = False
        
    if file_format == '' or file_format == [] or file_format == [''] or file_format == None:
        file_format = []

    if file_format == 'csv':
        file_format = ['csv']
    if file_format == 'txt':
        file_format = ['txt']

    if not isinstance(api_cooldown_seconds, (int, float)) or api_cooldown_seconds < 0 or api_cooldown_seconds > 60:
        print("ERROR:\tPlease use a reasonable 'api_cooldown_seconds' number of seconds (between 0 and 60).")
        proceed = False

    if proceed == True:
        if timeframe in missing_timeframes.keys():
            if include_current_candle == True:
                n_bulk = (length * missing_timeframes[timeframe][1]) // data_limit
                remainder = (length * missing_timeframes[timeframe][1]) % data_limit
            if include_current_candle == False:
                n_bulk = ((length + 1) * missing_timeframes[timeframe][1]) // data_limit
                remainder = ((length + 1) * missing_timeframes[timeframe][1]) % data_limit

            while n_bulk > 0:
                since = round(ccxt.binance({}).milliseconds() - (ccxt.binance({}).milliseconds() % (missing_timeframes[timeframe][1] * missing_timeframes[timeframe][2])) - (n_bulk * data_limit * missing_timeframes[timeframe][2]) - (remainder * missing_timeframes[timeframe][2]))
                for block in ccxt.binance({}).fetch_ohlcv(symbol = symbol, timeframe = missing_timeframes[timeframe][0], since = (since + (missing_timeframes[timeframe][1] * missing_timeframes[timeframe][2])), limit = data_limit):
                    timestamp_temp.append(block[0])
                    openx_temp.append(block[1])
                    high_temp.append(block[2])
                    low_temp.append(block[3])
                    close_temp.append(block[4])
                    volume_temp.append(block[5])
                n_bulk -= 1
                if n_bulk > 0 or remainder > 0:
                    time.sleep(api_cooldown_seconds)

            if remainder > 0:
                since = round(ccxt.binance({}).milliseconds() - (ccxt.binance({}).milliseconds() % (missing_timeframes[timeframe][1] * missing_timeframes[timeframe][2])) - (remainder * missing_timeframes[timeframe][2]))
                for block in ccxt.binance({}).fetch_ohlcv(symbol = symbol, timeframe = missing_timeframes[timeframe][0], since = (since + (missing_timeframes[timeframe][1] * missing_timeframes[timeframe][2])), limit = remainder + 1):
                    timestamp_temp.append(block[0])
                    openx_temp.append(block[1])
                    high_temp.append(block[2])
                    low_temp.append(block[3])
                    close_temp.append(block[4])
                    volume_temp.append(block[5])

            if length > 1:
                for i in [num for num in range(0, len(timestamp_temp), missing_timeframes[timeframe][1])][:-1]:
                    timestamp.append(timestamp_temp[i])
                    openx.append(openx_temp[i])
                    high.append(max(high_temp[i:i + missing_timeframes[timeframe][1]]))
                    low.append(min(low_temp[i:i + missing_timeframes[timeframe][1]]))
                    close.append(close_temp[i + (missing_timeframes[timeframe][1] - 1)])
                    volume.append(sum(volume_temp[i:i + missing_timeframes[timeframe][1]]))

                
                timestamp.append(timestamp_temp[i + missing_timeframes[timeframe][1]])
                openx.append(openx_temp[i + missing_timeframes[timeframe][1]])
                high.append(max(high_temp[i + missing_timeframes[timeframe][1]:]))
                low.append(min(low_temp[i + missing_timeframes[timeframe][1]:]))
                close.append(close_temp[-1])
                volume.append(sum(volume_temp[i + missing_timeframes[timeframe][1]:]))

            if length == 1:
                timestamp.append(timestamp_temp[0])
                openx.append(openx_temp[0])
                high.append(max(high_temp[0:]))
                low.append(min(low_temp[0:]))
                close.append(close_temp[-1])
                volume.append(sum(volume_temp[0:]))

        if timeframe not in missing_timeframes.keys():
            if include_current_candle == True:
                n_bulk = length // data_limit
                remainder = length % data_limit
            if include_current_candle == False:
                n_bulk = (length + 1) // data_limit
                remainder = (length + 1) % data_limit

            while n_bulk > 0:
                since = ccxt.binance({}).milliseconds() - (n_bulk * data_limit * binance_timeframes[timeframe]) - (remainder * binance_timeframes[timeframe])
                for block in ccxt.binance({}).fetch_ohlcv(symbol = symbol, timeframe = timeframe, since = since, limit = data_limit):
                    timestamp.append(block[0])
                    openx.append(block[1])
                    high.append(block[2])
                    low.append(block[3])
                    close.append(block[4])
                    volume.append(block[5])
                n_bulk -= 1
                if n_bulk > 0 or remainder > 0:
                    time.sleep(api_cooldown_seconds)

            if remainder > 0:
                since = ccxt.binance({}).milliseconds() - (remainder * binance_timeframes[timeframe])
                for block in ccxt.binance({}).fetch_ohlcv(symbol = symbol, timeframe = timeframe, since = since, limit = remainder):
                    timestamp.append(block[0])
                    openx.append(block[1])
                    high.append(block[2])
                    low.append(block[3])
                    close.append(block[4])
                    volume.append(block[5])

        data_identifier = 'binance_' + ''.join(symbol.split('/')) + '_' + str(timeframe) + '_' + str(length) + ('_including_current_candle' if include_current_candle == True else '_NOT_including_current_candle')

        if file_format != []:
            for ending in file_format:
                
                with open(data_identifier + '.' + str(ending), 'w') as csvfile:
                    writer = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
                    writer.writerow([head for head in ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']])
                    if include_current_candle == True:
                        write = zip(timestamp, openx, high, low, close, volume)
                    if include_current_candle == False:
                        write = zip(timestamp[:-1], openx[:-1], high[:-1], low[:-1], close[:-1], volume[:-1])
                    for entry in write:
                        writer.writerow(entry)

        if include_current_candle == True:
            df = pd.DataFrame(list(zip(timestamp, openx, high, low, close, volume)), columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df.name = data_identifier
            return df
        if include_current_candle == False:
            df = pd.DataFrame(list(zip(timestamp[:-1], openx[:-1], high[:-1], low[:-1], close[:-1], volume[:-1])), columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df.name = data_identifier
            return df
