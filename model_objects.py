import pprint as pprint

# This is example code from Ashwin's group that I tried to fill in based on our database project terms
# this will help define the objects of our application

# animal object
class animal(object):

# holds id, capacity, price_per_km, arrival
# How do I do multiple constructors
    def __init__(self):

        self.name = name

    def __repr__(self):
        return pprint.pformat(vars(self))

    def get_readable_string(self):
        var_dict_keys = vars(self).keys()

        readable_string = "["

        for key in var_dict_keys:
            readable_string = readable_string + str(key) + ": " + str(vars(self)[key]) + ", "

        readable_string = readable_string[:-3] + "]"

        return readable_string


class user(object):

    def __init__(self, user_id = None, email = None, password = None, first_name = None, last_name = None ):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return pprint.pformat(vars(self))

    def populate_user_with_login_response_dict(self, query_response_dict):

        self.user_id = query_response_dict['user_id']
        self.email = query_response_dict['email']
        self.password = query_response_dict['password']
        self.first_name = query_response_dict['first_name']
        self.last_name = query_response_dict['last_name']

        print(self.last_name)

class Exhibit(object):

    def __init__(self, name, num_animals, water_bool):
        self.name = name
        self.num_animals = num_animals
        self.water_bool = water_bool

    def __repr__(self):
        return pprint.pformat(vars(self))

    def populate_city_with_station_query_response_dict(self, query_response_dict):

        self.address_id = query_response_dict['address_id']
        self.name = query_response_dict['name']

        print(self)
