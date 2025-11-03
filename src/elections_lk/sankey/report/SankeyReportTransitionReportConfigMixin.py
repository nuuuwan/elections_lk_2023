from elections_lk.sankey.report.transitions.VoteTransitionFactory import \
    VoteTransitionFactory


class SankeyReportTransitionReportConfigMixin:
    @staticmethod
    def get_config_list():
        config_list = []
        for transition in VoteTransitionFactory.get_transitions():
            config_list.append(
                [
                    transition.label,
                    transition.is_match,
                    transition.get_description,
                ]
            )
        return config_list
