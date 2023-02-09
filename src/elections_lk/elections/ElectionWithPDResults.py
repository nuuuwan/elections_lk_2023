from gig import Ent, EntType, GIGTable

from elections_lk import Election


def correct_int(x):
    return (int)(round(x, 0))


class ElectionWithPDResults(Election):
    @classmethod
    def get_gig_table(cls, year: int):
        measurement = f'government-elections-{cls.get_election_type()}'
        region_str = 'regions-ec'
        time_str = str(year)
        return GIGTable(measurement, region_str, time_str)

    @property
    def pd_results(self):
        return self.results

    @property
    def pd_results_idx(self):
        return {
            pd_result.region_id: pd_result for pd_result in self.pd_results
        }

    @classmethod
    def get_ent_list(cls):
        pd_list = Ent.list_from_type(EntType.PD)
        ed_list = Ent.list_from_type(EntType.ED)

        other_id_list = [ed.id + 'P' for ed in ed_list] + [
            'EC-11D'
        ]  # TODO: Must include all displaced votes.

        other_pd_list = []
        for other_id in other_id_list:
            other_pd_list.append(Ent(dict(id=other_id)))

        return pd_list + other_pd_list
