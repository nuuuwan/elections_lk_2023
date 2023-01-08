import os

import humanize
from gig import ents
from gig.ent_types import ENTITY_TYPE

DIR_DATA = 'data/local_authority/2018'

WGET_OPTIONS = ' '.join(['--no-check-certificate', '--no-verbose'])


def download(url, local_file):
    if os.path.exists(local_file):
        print(f'"{local_file}" already exists. Skipping download...')
        return
    print(f'Downloading "{url}" to "{local_file}"...')
    os.system(f'wget {WGET_OPTIONS} -O "{local_file}" "{url}"')
    file_size = humanize.naturalsize(os.path.getsize(local_file))
    print(f'Downloaded {file_size}')


def init():
    if not os.path.exists(DIR_DATA):
        os.makedirs(DIR_DATA)


def download_pdf_for_district(district_id, district_name):
    url = os.path.join(
        'https://elections.gov.lk',
        'web/wp-content/uploads/election-results',
        'local-authorities-elections/2018',
        f'nu-of-mem-elected/{district_name}_Si.pdf',
    )

    pdf_file_name = os.path.join(DIR_DATA, f'{district_id}.pdf')
    download(url, pdf_file_name)
    return pdf_file_name


def download_all_pdfs():
    districts = ents.get_entities(ENTITY_TYPE.DISTRICT)
    for district in districts:
        district_name = district['name']
        district_id = district['id']
        download_pdf_for_district(district_id, district_name)


def main():
    init()
    download_all_pdfs()


if __name__ == '__main__':
    main()
