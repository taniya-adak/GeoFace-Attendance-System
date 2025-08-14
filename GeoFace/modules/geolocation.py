import geocoder

def get_current_location():
    """Get current geolocation data"""
    g = geocoder.ip('me')
    if g.ok:
        return {
            "latitude": g.latlng[0],
            "longitude": g.latlng[1],
            "place": g.address
        }
    return None