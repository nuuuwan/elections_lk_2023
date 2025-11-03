from elections_lk.sankey.report.transitions.TransitionConsistentNonVoters import \
    TransitionConsistentNonVoters  # noqa: E501
from elections_lk.sankey.report.transitions.TransitionDisengagedOrFormerVoters import \
    TransitionDisengagedOrFormerVoters  # noqa: E501
from elections_lk.sankey.report.transitions.TransitionLoyalVoters import \
    TransitionLoyalVoters
from elections_lk.sankey.report.transitions.TransitionPartySwitchers import \
    TransitionPartySwitchers
from elections_lk.sankey.report.transitions.TransitionReengagedOrFirstTimeVoters import \
    TransitionReengagedOrFirstTimeVoters  # noqa: E501


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
            TransitionConsistentNonVoters(),
        ]

    @staticmethod
    def get_transition_idx():
        transitions = VoteTransitionFactory.get_transitions()
        return {transition.label: transition for transition in transitions}

    @staticmethod
    def split_transitions(transitions):
        idx = {}
        for label in VoteTransitionFactory.get_transition_idx().keys():
            idx[label] = []

        for party_x, party_y, votes in transitions:
            has_match = False
            for (
                label,
                transition,
            ) in VoteTransitionFactory.get_transition_idx().items():
                is_match = transition.is_match(party_x, party_y)
                if is_match:
                    if has_match:
                        raise VoteTransitionFactoryException(
                            "Transition match conflict: "
                            + str(party_x, party_y, votes)
                        )
                    has_match = True
                    idx[label].append((party_x, party_y, votes))

            if not has_match:
                raise VoteTransitionFactoryException(
                    "No transition match found: "
                    + str(party_x, party_y, votes)
                )

        return idx
