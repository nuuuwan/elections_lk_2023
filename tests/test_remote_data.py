from unittest import TestCase

from elections_lk.core import remote_data


class TestRemoteData(TestCase):
    def test_init(self):
        raw_result_list = remote_data.get_raw_result_list(
            'presidential', 2019
        )
        self.assertEqual(len(raw_result_list), 14510)
