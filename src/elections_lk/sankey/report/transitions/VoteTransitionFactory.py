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
