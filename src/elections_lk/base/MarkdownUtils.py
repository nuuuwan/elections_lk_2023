class MarkdownUtils:

    @staticmethod
    def md_table_row(*values) -> str:
        assert isinstance(values, tuple) and len(values) >= 1
        return "| " + " | ".join([str(v).strip() for v in values]) + " |"
