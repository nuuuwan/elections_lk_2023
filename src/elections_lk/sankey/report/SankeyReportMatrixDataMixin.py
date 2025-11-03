from utils import Log, TSVFile

log = Log("SankeyReportMatrixDataMixin")


class SankeyReportMatrixDataMixin:
    @property
    def matrix_data_file_path(self):
        return self.file_base + ".matrix_data.tsv"

    def save_tsv(self):
        TSVFile(self.matrix_data_file_path).write(self.d_list)
        log.info(f"Wrote {self.matrix_data_file_path}")
