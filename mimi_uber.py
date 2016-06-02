from uber_rides.client import UberRidesClient
from auth_example import get_session
uber = UberRidesClient(get_session(), sandbox_mode=True)

# Info required to request a ride
UBER_SUV_PRODUCT_ID = '65aaf0c2-655a-437d-bf72-5d935cf95ec9'
# Geopt del Panamar
LAT = 8.996285
LON = -79.496408

# Examples
def products_available_at_location(lat=LAT, lon=LON):
    response = uber.get_products(lat, lon)
    products = response.json.get('products')
    return products

def pickup_time_estimates():
    response = uber.get_pickup_time_estimates(LAT, LON)
    l = [[est['display_name'], est['estimate']]for est in response.json.get('times')]
    label = lambda n, s: n + ': ' + str(s/60) + ' minutos'
    return [label(name, seconds) for name, seconds in l]

def uber_suv_pickup_time_estimate():
    response = uber.get_pickup_time_estimates(LAT, LON, UBER_SUV_PRODUCT_ID)
    estimate_in_seconds = response.json.get('times')[0].get('estimate')
    return str(estimate_in_seconds / 60) + ' minutos'

def request_suv_to_panamar(lat=LAT, lon=LON):
    response = uber.request_ride(
        product_id=UBER_SUV_PRODUCT_ID,
        start_latitude=lat,
        start_longitude=lon
    )
    print response

if __name__ == '__main__':
    # print pickup_time_estimates()
    print products_available_at_location()
    # print uber_suv_pickup_time_estimate()
    # print request_suv_to_panamar()
