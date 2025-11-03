from elections_lk.sankey.report.transitions.TransitionDisengagedOrFormerVoters import (
    TransitionDisengagedOrFormerVoters,
)  # noqa: E501
from elections_lk.sankey.report.transitions.TransitionLoyalVoters import (
    TransitionLoyalVoters,
)
from elections_lk.sankey.report.transitions.TransitionNonVoters import (
    TransitionNonVoters,
)  # noqa: E501
from elections_lk.sankey.report.transitions.TransitionPartySwitchers import (
    TransitionPartySwitchers,
)
from elections_lk.sankey.report.transitions.TransitionReengagedOrFirstTimeVoters import (
    TransitionReengagedOrFirstTimeVoters,
)  # noqa: E501


class VoteTransitionFactoryException(Exception):
    pass


class VoteTransitionFactory:
    @staticmethod
    def get_transitions():
        return [
            TransitionLoyalVoters(),
            TransitionPartySwitchers(),
            TransitionReengagedOrFirstTimeVoters(),
            TransitionDisengagedOrFormerVoters(),
            TransitionNonVoters(),
        ]

    @staticmethod
    def get_transition_idx():
        transitions = VoteTransitionFactory.get_transitions()
        return {transition.label: transition for transition in transitions}

    @staticmethod
    def get_transition_for_party_transition(party_x, party_y):
        matched_transition = None
        for transition in VoteTransitionFactory.get_transitions():
            is_match = transition.is_match(party_x, party_y)
            if is_match:
                if matched_transition is not None:
                    raise VoteTransitionFactoryException(
                        "Duplicate Transition match: " + str(party_x, party_y)
                    )
                matched_transition = transition
        if matched_transition is None:
            raise VoteTransitionFactoryException(
                "No transition match found: " + str(party_x, party_y)
            )
        return matched_transition

    @staticmethod
    def split_transitions(transitions):
        idx = {}
        for label in VoteTransitionFactory.get_transition_idx().keys():
            idx[label] = []

        for party_x, party_y, votes in transitions:
            transition = (
                VoteTransitionFactory.get_transition_for_party_transition(
                    party_x, party_y
                )
            )
            idx[transition.label].append((party_x, party_y, votes))
        return idx
