def valid_price(price):
    if 0 < price:
        return price
    raise ValueError("[ERROR]The invalid price!!!")
