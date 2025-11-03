class AbstractTransition:
    NO_VOTE = "no vote"

    @property
    def label(self):
        raise NotImplementedError

    def is_match(self, party_x, party_y):
        raise NotImplementedError

    def get_description(self, election_x, election_y):
        raise NotImplementedError
