import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://nyameget:xU9xKSe8zsSaeLqrUeotCAsdWNTzSwXX@dpg-cr938hq3esus73bfgb7g-a.oregon-postgres.render.com/dbname_skju')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY = "NVOQ06FFhwbHBjlEi54WjwcJA2wXKL2w5ygGyuGVxrfQ1MAbkF"
    IDENTIFICATION_URL = "https://plant.id/api/v3/identification?details=common_names,url,description,taxonomy,rank,gbif_id,inaturalist_id,image,synonyms,edible_parts,watering,propagation_methods&language=en"
    SERVER_URL = "http://localhost:5000"
