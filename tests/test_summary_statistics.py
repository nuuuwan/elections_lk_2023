from unittest import TestCase

from elections_lk import SummaryStatistics

TEST_RESULT = SummaryStatistics(
    valid=900,
    rejected=100,
    polled=1000,
    electors=1250,
)


class TestSummaryStatistics(TestCase):
    def test_init(self):
        summary_statistics = TEST_RESULT

        self.assertEqual(summary_statistics.valid, 900)
        self.assertEqual(summary_statistics.rejected, 100)
        self.assertEqual(summary_statistics.polled, 1000)
        self.assertEqual(summary_statistics.electors, 1250)

    def test_p_rejected(self):
        summary_statistics = TEST_RESULT
        self.assertEqual(summary_statistics.p_rejected, 0.1)

    def test_p_valid(self):
        summary_statistics = TEST_RESULT
        self.assertEqual(summary_statistics.p_valid, 0.9)

    def test_p_turnout(self):
        summary_statistics = TEST_RESULT
        self.assertEqual(summary_statistics.p_turnout, 0.8)

    def test_concat(self):
        self.assertEqual(
            SummaryStatistics.concat([TEST_RESULT, TEST_RESULT]),
            SummaryStatistics(
                valid=1_800,
                rejected=200,
                polled=2_000,
                electors=2_500,
            ),
        )
