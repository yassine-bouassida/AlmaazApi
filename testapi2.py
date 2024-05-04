import aiohttp
import asyncio
import pandas as pd

#http://host.docker.internal:5000
async def fetch_newest_time(session, symbol):
    async with session.get(f'http://localhost:5000/copy_rates_from/{symbol}') as response:
        res = (await response.text()).split("\n")
        newest_time = res[-1].split(",")[0][2:]
        newest_time = int(newest_time)
        newest_time = pd.to_datetime(newest_time, unit='s')
        hour = newest_time.hour
        if hour != symb_dict[symbol]:
            symb_dict[symbol] = hour
            print("newest time of ", symbol, " is: ", newest_time)
            price = res[-1].split(",")[1]
            print("price: ", price)
            return (price,symbol)
        else:
            await asyncio.sleep(10000)
            return await fetch_newest_time(session, symbol)

async def get_newest_time_async(symbol):
    async with aiohttp.ClientSession() as session:
        return await fetch_newest_time(session, symbol)

async def main():
    # Read symbols from file
    with open("symb.csv", "r") as file:
        symbols = file.read().strip().split("\n")[1:]
    
    # Initialize dict symb as key and time as value
    global symb_dict
    symb_dict = {symbol: -1 for symbol in symbols}

    # Fetch newest time asynchronously for each symbol
    tasks = [get_newest_time_async(symbol) for symbol in symbols]
    for task in asyncio.as_completed(tasks):
        price,sym = await task
        print("***Price for", sym," is: ",price)

# Run the asyncio event loop
asyncio.run(main())
