from gig import GIGTable

from elections_lk.core.PartyToVotes import PartyToVotes
from elections_lk.core.Result import Result
from elections_lk.core.SummaryStatistics import SummaryStatistics


def correct_int(x):
    return (int)(round(x, 0))


class ElectionLoaderMixin:

    @classmethod
    def __extract_party_to_votes__(cls, result_raw):
        party_to_votes = {}
        for k, v in result_raw.dict.items():
            if k not in SummaryStatistics.FIELDS:
                party_to_votes[k] = correct_int(v)
        return PartyToVotes(party_to_votes)

    @classmethod
    def __extract_summary_statistics__(cls, result_raw):
        return SummaryStatistics(
            valid=correct_int(result_raw.valid),
            rejected=correct_int(result_raw.rejected),
            polled=correct_int(result_raw.polled),
            electors=correct_int(result_raw.electors),
        )

    @classmethod
    def load_result(cls, gig_table, ent):
        try:
            result_raw = ent.gig(gig_table)
        except BaseException:
            return None

        party_to_votes = cls.__extract_party_to_votes__(result_raw)

        # HACK Fix for 2000 Parliamentary Election missing Summary Statistics
        if (
            gig_table.measurement == "government-elections-parliamentary"
            and gig_table.time_group == "2000"
        ):
            gig_table2 = GIGTable(
                gig_table.measurement, gig_table.ent_type_group, "2001"
            )
            result_raw2 = ent.gig(gig_table2)
            summary_statistics = cls.__extract_summary_statistics__(
                result_raw2
            )
            valid = party_to_votes.total
            summary_statistics.valid = valid
        else:
            summary_statistics = cls.__extract_summary_statistics__(
                result_raw
            )

        return Result(
            region_id=ent.id,
            summary_statistics=summary_statistics,
            party_to_votes=party_to_votes,
        )

    @classmethod
    def from_year(cls, year):
        date = None
        for date in cls.get_dates():
            if int(date[:4]) == year:
                break
        if date is None:
            raise ValueError(f"Election year {year} not found.")

        ent_list = cls.get_ent_list()
        gig_table = cls.get_gig_table(year)
        results = []
        for ent in ent_list:
            result = cls.load_result(gig_table, ent)
            if result:
                results.append(result)
        return cls(date=date, results=results)
