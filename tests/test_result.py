from unittest import TestCase

from elections_lk.core import Result, SummaryStatistics

TEST_RESULT = Result(
    entity_id='EC-01A',
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
)

TEST_RESULT2 = Result(
    entity_id='EC-01B',
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
)


class TestResult(TestCase):
    def test_init(self):
        result = TEST_RESULT

        self.assertEqual(result.entity_id, 'EC-01A')
        self.assertEqual(
            result.summary_statistics,
            SummaryStatistics(
                valid=900,
                rejected=100,
                polled=1000,
                electors=1250,
            ),
        )
        self.assertEqual(
            result.party_to_votes,
            dict(
                UNP=500,
                SLFP=400,
            ),
        )

    def test_concat(self):
        result = Result.concat('EC-01', [TEST_RESULT, TEST_RESULT2])

        self.assertEqual(result.entity_id, 'EC-01')
        self.assertEqual(
            result.summary_statistics,
            SummaryStatistics(
                valid=1300,
                rejected=110,
                polled=1410,
                electors=1701,
            ),
        )

        self.assertEqual(
            result.party_to_votes,
            dict(
                UNP=600,
                SLFP=700,
            ),
        )

    def test_map_and_concat(self):
        result = Result.mapAndConcat(
            [TEST_RESULT, TEST_RESULT2], lambda x: x[:5]
        )[0]

        self.assertEqual(result.entity_id, 'EC-01')
        self.assertEqual(
            result.summary_statistics,
            SummaryStatistics(
                valid=1300,
                rejected=110,
                polled=1410,
                electors=1701,
            ),
        )
