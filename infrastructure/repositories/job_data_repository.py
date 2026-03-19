from application.ports.output_ports import JobDataRepositoryPort
from domain.entities.job_offer import JobOffer
from infrastructure.etl.pipeline import JobOfferETL


class FileJobDataRepository(JobDataRepositoryPort):
    def __init__(self, etl: JobOfferETL | None = None) -> None:
        self.etl = etl or JobOfferETL()

    def load_job_offers(self, source: str) -> list[JobOffer]:
        df = self.etl.load_dataframe(source)
        clean_df = self.etl.preprocess(df)
        return self.etl.to_entities(clean_df)
