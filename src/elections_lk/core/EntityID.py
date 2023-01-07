from gig import ent_types


class EntityID:
    def __init__(self, entity_id):
        self.entity_id = entity_id

    @property
    def entity_type(self):
        return ent_types.get_entity_type(self.entity_id)
