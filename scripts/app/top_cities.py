import pandas as pd

# based on website
# https://wptravel.io/most-visited-cities-in-the-world/
# The top 30 cities of 2022 and their rank and country


# list for rank the cities
rnk = []
for i in range(1, 31):
    rnk.append(i)

# list for cities
cities = ['Paris',
'Dubai',
'Amsterdam',
'Madrid',
'Rome',
'London',
'Munich',
'Berlin',
'Barcelona',
'New York',
'Prague',
'Lisbon',
'Milan',
'Los Angeles',
'Singapore',
'Vienna',
'Frankfurt',
'Dublin',
'Stockholm',
'Tokyo',
'Florence',
'Orlando',
'Athens',
'Abu Dhabi',
'Istanbul',
'Seoul',
'Venice',
'Zurich',
'Toronto',
'Miami']

# list for countries of cities
countries = ['France',
'United Arab Emirates',
'Netherlands',
'Spain',
'Italy',
'United Kingdom',
'Germany',
'Germany',
'Spain',
'United States',
'Czech Republic',
'Portugal',
'Italy',
'United States',
'Singapore',
'Austria',
'Germany',
'Ireland',
'Sweden',
'Japan',
'Italy',
'United States',
'Greece',
'United Arab Emirates',
'Turkey',
'South Korea',
'Italy',
'Switzerland',
'Canada',
'United States']

# merge all lists into dict
data_dict = {'rank': rnk, 'city':cities, 'country': countries}

# convert dict into data frame
df_cities = pd.DataFrame(data_dict)


