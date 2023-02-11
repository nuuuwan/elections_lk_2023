from utils import JSONFile

FILE_PATH = 'src/elections_lk/elections/YEAR_TO_REGION_TO_SEATS.json'
YEAR_TO_REGION_TO_SEATS = JSONFile(FILE_PATH).read()
