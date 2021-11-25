import math

def distance_to(source, target):
    """Calculate the distance in Kilometers between two points on Earth

    Args:
        source (tuple): (float(latt), float(long))
        target (tuple): (float(latt), float(long))

    Returns:
        float: Distance between source and target in Kilometers
    """
    r = 6371 # Earth radius in Kilometers
    try:
        source_lat, source_lon = source
        target_lat, target_lon = target
        source_phi, target_phi = math.radians(source_lat), math.radians(target_lat)
        source_lam, target_lam = math.radians(source_lon), math.radians(target_lon)
        h = (math.sin((target_phi - source_phi) / 2)**2 
            + math.cos(source_phi) * math.cos(target_phi) 
            * math.sin((target_lam - source_lam) / 2)**2)
    except Exception:
        return -1
    
    return 2 * r * math.asin(math.sqrt(h))

if __name__ == '__main__':
    print('Get:', round(distance_to((51.5085,-0.1257), (40.4165,-3.7026))), 'Expected:', 1264)