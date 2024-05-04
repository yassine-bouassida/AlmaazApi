from flask import Flask
from datetime import datetime
import MetaTrader5 as mt5
import pytz
# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()

app = Flask(__name__)

@app.route('/get_LastTick_Of/<string:symbol>')
def get_LastTick_Of(symbol):
    # get the last tick of EURUSD
    symbol_info_tick = mt5.symbol_info_tick(symbol)
    if symbol_info_tick is None:
        print(symbol, "not found, can't call symbol_info_tick()")
        return symbol + " not found, can't call symbol_info_tick()"
    else:
        return str(symbol_info_tick)

@app.route('/copy_rates_from/<string:symbol>')
def copy_rates_from(symbol):
    timezone = pytz.timezone("Etc/UTC")
    utc_from = datetime.now(tz=timezone)
    rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M1, utc_from, 1000)



if __name__ == '__main__':
    app.run(debug=True)
