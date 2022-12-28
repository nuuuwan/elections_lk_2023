from unittest import TestCase

from elections_lk.core.Result import Result

TEST_RESULT = Result.loadFromDict(
    dict(
        entity_id='EC-01A',
        valid=900,
        rejected=100,
        polled=1000,
        electors=1250,
        UNP=500,
        SLFP=400,
    )
)

TEST_RESULT2 = Result.loadFromDict(
    dict(
        entity_id='EC-01B',
        valid=400,
        rejected=10,
        polled=410,
        electors=451,
        UNP=100,
        SLFP=300,
    )
)


class TestResult(TestCase):
    def test_load_from_dict(self):
        result = TEST_RESULT

        self.assertEqual(result.region_id, 'EC-01A')
        self.assertEqual(result.valid, 900)
        self.assertEqual(result.rejected, 100)
        self.assertEqual(result.polled, 1000)
        self.assertEqual(result.electors, 1250)
        self.assertEqual(
            result.party_to_votes,
            dict(
                UNP=500,
                SLFP=400,
            ),
        )

    def test_p_rejected(self):
        result = TEST_RESULT
        self.assertEqual(result.p_rejected, 0.1)

    def test_p_valid(self):
        result = TEST_RESULT
        self.assertEqual(result.p_valid, 0.9)

    def test_p_turnout(self):
        result = TEST_RESULT
        self.assertEqual(result.p_turnout, 0.8)

    def test_concat(self):
        result = Result.concat('EC-01', [TEST_RESULT, TEST_RESULT2])

        self.assertEqual(result.region_id, 'EC-01')
        self.assertEqual(result.valid, 1300)
        self.assertEqual(result.rejected, 110)
        self.assertEqual(result.polled, 1410)
        self.assertEqual(result.electors, 1701)
        self.assertEqual(
            result.party_to_votes,
            dict(
                UNP=600,
                SLFP=700,
            ),
        )