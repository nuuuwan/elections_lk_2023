from dataclasses import dataclass

from gig import Ent, EntType

from elections_lk.core import PartyToVotes, Result, SummaryStatistics
from elections_lk.elections import Election


def correct_int(x):
    return (int)(round(x, 0))


@dataclass
class ElectionWithPDResults(Election):
    pd_results: list

    @classmethod
    def load(cls, year: int):
        gig_table = cls.get_gig_table(year)

        pd_list = Ent.load_list_for_type(EntType.PD)
        ed_list = Ent.load_list_for_type(EntType.ED)

        other_id_list = [ed.id + 'P' for ed in ed_list] + [
            'EC-11D'
        ]  # TODO: Must include all displaced votes.

        other_pd_list = []
        for other_id in other_id_list:
            other_pd_list.append(Ent(dict(id=other_id)))

        pd_results = []
        for ent in pd_list + other_pd_list:
            try:
                result_raw = ent.gig(gig_table)
            except BaseException:
                continue

            party_to_votes = {}
            for k, v in result_raw.dict.items():
                if k not in ['valid', 'rejected', 'polled', 'electors']:
                    party_to_votes[k] = correct_int(v)

            result = Result(
                region_id=ent.id,
                summary_statistics=SummaryStatistics(
                    valid=correct_int(result_raw.valid),
                    rejected=correct_int(result_raw.rejected),
                    polled=correct_int(result_raw.polled),
                    electors=correct_int(result_raw.electors),
                ),
                party_to_votes=PartyToVotes(party_to_votes),
            )
            pd_results.append(result)
        return cls(year, pd_results)
