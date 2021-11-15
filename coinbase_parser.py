from coinbase.wallet.client import Client
client = Client(api_key, api_secret)

supported_native_currencies = client.get_currencies()
exchange_rates = client.get_exchange_rates()
buy_price = client.get_buy_price(currency_pair = 'BTC-USD')
sell_price = client.get_sell_price(currency_pair = 'BTC-USD')
spot_price = client.get_spot_price(currency_pair = 'BTC-USD')
get_account = client.get_account(account_id)
transactions_for_an_address = client.get_address_transactions(account_id, address_id)
deposits = client.get_deposits(account_id)


