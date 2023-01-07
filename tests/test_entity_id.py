from unittest import TestCase

from gig.ent_types import ENTITY_TYPE

from elections_lk.core import EntityID


class TestEntityID(TestCase):
    def test_entity_type(self):
        for entity_id, entity_type in [
            ['LK', ENTITY_TYPE.COUNTRY],
        ]:
            self.assertEqual(EntityID(entity_id).entity_type, entity_type)
