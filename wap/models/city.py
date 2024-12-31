import Levenshtein
from geonamescache import GeonamesCache
from unidecode import unidecode


class City:
    def __init__(self, name: str):
        self.name = name
        # self.country = None
        self.region = None
        # self.lat = None
        # self.lon = None
        self.temp = None
        self.description = None

    def normalize_name(self):
        self.name = unidecode(self.name).strip().title()

    def search_city(self):
        gc = GeonamesCache()
        gc.get_cities_by_name(self.name)
        searched_city_list = gc.search_cities(self.name)
        if not searched_city_list:
            self._correct_name()
            return
        city = searched_city_list.__getitem__(0)
        self.name = city.get('name')
        # self.lat = city.get('latitude')
        # self.lon = city.get('longitude')
        # self.country_code = city.get('countrycode')

    def _correct_name(self):
        gc = GeonamesCache()
        cities = gc.get_cities()
        closest_city = None
        min_distance = float('inf')
        for city, data in cities.items():
            distance = Levenshtein.distance(self.name.lower(), data.get('name').lower())
            if distance < min_distance:
                min_distance = distance
                closest_city = data
        if closest_city:
            self.name = closest_city.get('name')
            # self.lat = closest_city.get('latitude')
            # self.lon = closest_city.get('longitude')
            # self.country_code = closest_city.get('countrycode')
        return

    def set_region(self, city_data):
        self.region = city_data.get("timezone").split("/")[0]
