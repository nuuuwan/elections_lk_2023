import os

DIR_DATA = 'data/local_authority/2018'


def get_district_pdf_file(district_id):
    return os.path.join(DIR_DATA, f'{district_id}.pdf')
