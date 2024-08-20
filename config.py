import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://nyameget:17cvsOhOqdY8Kc6ylEi2KNMyioBE3I8h@dpg-cqln8dlumphs7397crmg-a.oregon-postgres.render.com/dbname_ksxs')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY = "nnzZn3wOmR6ADC3MaPtS36rBRYAOmvXHFPFjGRAy8wvqS3nVlE"
    IDENTIFICATION_URL = "https://plant.id/api/v3/identification?details=common_names,url,description,taxonomy,rank,gbif_id,inaturalist_id,image,synonyms,edible_parts,watering,propagation_methods&language=en"
    SERVER_URL = "http://localhost:5000"
