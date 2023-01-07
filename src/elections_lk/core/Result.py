from dataclasses import dataclass

from elections_lk.core.StrToInt import StrToInt
from elections_lk.core.SummaryStatistics import SummaryStatistics


@dataclass
class Result:
    region_id: str
    summary_statistics: SummaryStatistics
    party_to_votes: StrToInt

    @property
    def valid_long(self):
        return sum(self.party_to_votes.values())

    def get_party_votes(self, party):
        return self.party_to_votes[party]

    def get_party_votes_p(self, party):
        return self.get_party_votes(party) / self.summary_statistics.valid

    @classmethod
    def concat(cls, concat_region_id, result_list):
        summary_statistics = SummaryStatistics.concat(
            [r.summary_statistics for r in result_list]
        )

        party_to_votes = StrToInt.concat(
            [r.party_to_votes for r in result_list]
        )

        return cls(
            region_id=concat_region_id,
            summary_statistics=summary_statistics,
            party_to_votes=party_to_votes,
        )

    @classmethod
    def mapAndConcat(cls, result_list, func_map) -> list:
        concat_region_id_to_result_list = {}
        for result in result_list:
            concat_region_id = func_map(result.region_id)
            if concat_region_id not in concat_region_id_to_result_list:
                concat_region_id_to_result_list[concat_region_id] = []
            concat_region_id_to_result_list[concat_region_id].append(result)

        result2_list = []
        for (
            concat_region_id,
            result_list,
        ) in concat_region_id_to_result_list.items():
            result2_list.append(cls.concat(concat_region_id, result_list))

        return result2_list
