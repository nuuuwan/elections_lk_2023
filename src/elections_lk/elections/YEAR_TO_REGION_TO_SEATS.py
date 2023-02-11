from utils import JSONFile

FILE_PATH = 'src/elections_lk/elections/YEAR_TO_REGION_TO_SEATS.json'
YEAR_TO_REGION_TO_SEATS = dict(
    list(
        map(
            lambda x: (int(x[0]), x[1]),
            JSONFile(FILE_PATH).read().items(),
        )
    )
)
