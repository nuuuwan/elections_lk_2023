from unittest import TestCase

from elections_lk.core.FinalResult import FinalResult
from elections_lk.core.SummaryStatistics import SummaryStatistics

TEST_RESULT = FinalResult(
    region_id='EC-01A',
    summary_statistics=SummaryStatistics(
        valid=900,
        rejected=100,
        polled=1000,
        electors=1250,
    ),
    party_to_votes=dict(
        UNP=500,
        SLFP=400,
    ),
    seats=1,
    party_to_seats=dict(
        UNP=1,
    ),
)

TEST_RESULT2 = FinalResult(
    region_id='EC-01B',
    summary_statistics=SummaryStatistics(
        valid=400,
        rejected=10,
        polled=410,
        electors=451,
    ),
    party_to_votes=dict(
        UNP=100,
        SLFP=300,
    ),
    seats=1,
    party_to_seats=dict(
        SLFP=1,
    ),
)


class TestResult(TestCase):
    def test_init(self):
        result = TEST_RESULT
        self.assertEqual(result.seats, 1)
        self.assertEqual(
            result.party_to_seats,
            dict(
                UNP=1,
            ),
        )

    def test_concat(self):
        result = FinalResult.concat('EC-01', [TEST_RESULT, TEST_RESULT2])
        self.assertEqual(result.seats, 2)
        self.assertEqual(
            result.party_to_seats,
            dict(
                UNP=1,
                SLFP=1,
            ),
        )
