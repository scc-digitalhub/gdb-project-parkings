
from kfp import dsl
import mlrun

URL = "https://opendata.comune.bologna.it/api/explore/v2.1/catalog/datasets/disponibilita-parcheggi-storico/exports/csv?lang=it&timezone=UTC&use_labels=true&delimiter=%3B"

@dsl.pipeline(name="Demo ETL pipeline")
def pipeline():
    """
    This function represents a demo ETL pipeline.

    It performs the following steps:
    1. Downloads a dataset.
    2. Extracts parking information from the dataset.
    3. Aggregates parking data.
    4. Runs a prediction on the aggregated data.
    5. Stores the aggregated and extracted parking data in a database.
    """

    # Get the current project
    project = mlrun.get_current_project()

    # Step 1: Download the dataset
    run_download = project.run_function("download-all", inputs={'url': URL}, outputs=["dataset"])

    # Step 2: Extract parking information
    run_parkings = project.run_function("extract-parkings", inputs={'di': run_download.outputs["dataset"]}, outputs=["parkings"])

    # Step 3: Aggregate parking data
    run_aggregate = project.run_function("aggregate-parkings", inputs={'di': run_download.outputs["dataset"]}, outputs=["parking_data_aggregated"])

    # Step 4: Run prediction on aggregated data
    project.run_function("predict-day", inputs={'parkings_di': run_download.outputs["dataset"]}, outputs=["parking_data_predicted"])

    # Step 5: Store aggregated and extracted parking data in database
    project.run_function("to-db", inputs={'agg_di': run_aggregate.outputs["parking_data_aggregated"], 'parkings_di': run_parkings.outputs["parkings"]})
