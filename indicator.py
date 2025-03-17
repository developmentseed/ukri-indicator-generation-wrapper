import json
import logging
import os
from enum import Enum
from typing import Dict, Optional, Any, List
from hazard import services

import pydantic
from stactools.osc_hazard.commands import cubify_invocation, collection_invocation, item_invocation

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SourceDataset(str, Enum):
    cmip6 = "NEX-GDDP-CMIP6"
    ukcp18 = "UKCP18"

class IndicatorType(str, Enum):
    degree_days = "degree_days_indicator"
    days_tas_above = "days_tas_above_indicator"

class IndicatorGenerationInput(pydantic.BaseModel):
    source_dataset: SourceDataset = "NEX-GDDP-CMIP6"
    source_dataset_kwargs: Optional[Dict[str, Any]] = None
    gcm_list: List[str] = ["NorESM2-MM"]
    scenario_list: List[str] = ["ssp585"]
    threshold_list: List[float] = [20]
    threshold_temperature: float = 32
    central_year_list: List[int] = [2090]
    central_year_historical: int = 2005
    window_years: int = 1
    bucket: Optional[str] = None
    prefix: Optional[str] = None
    store: Optional[str] = None
    write_xarray_compatible_zarr: Optional[bool] = False
    dask_cluster_kwargs: Optional[Dict[str, Any]] = None
    ceda_username: str
    ceda_password: str
    indicator: IndicatorType = "degree_days_indicator"

import typer
from typing_extensions import Annotated

app = typer.Typer()

def parse_input(val: str):
    return IndicatorGenerationInput(**json.loads(val))

def degree_days_indicator(indicator_generation_params: Annotated[IndicatorGenerationInput, typer.Argument(parser=parse_input)]):
    if indicator_generation_params.ceda_password and indicator_generation_params.ceda_username:
        os.environ["CEDA_USERNAME"] = indicator_generation_params.ceda_username
        os.environ["CEDA_PASSWORD"] = indicator_generation_params.ceda_password
    services.degree_days_indicator(
        source_dataset=indicator_generation_params.source_dataset.value,
        source_dataset_kwargs=indicator_generation_params.source_dataset_kwargs,
        gcm_list=indicator_generation_params.gcm_list,
        scenario_list=indicator_generation_params.scenario_list,
        threshold_temperature=indicator_generation_params.threshold_temperature,
        central_year_list=indicator_generation_params.central_year_list,
        central_year_historical=indicator_generation_params.central_year_historical,
        window_years=indicator_generation_params.window_years,
        bucket=indicator_generation_params.bucket,
        prefix=indicator_generation_params.prefix,
        store=indicator_generation_params.store,
        write_xarray_compatible_zarr=False,
        dask_cluster_kwargs=indicator_generation_params.dask_cluster_kwargs,
    )

def days_tas_above_indicator(indicator_generation_params: Annotated[IndicatorGenerationInput, typer.Argument(parser=parse_input)]):
    if indicator_generation_params.ceda_password and indicator_generation_params.ceda_username:
        os.environ["CEDA_USERNAME"] = indicator_generation_params.ceda_username
        os.environ["CEDA_PASSWORD"] = indicator_generation_params.ceda_password
    services.days_tas_above_indicator(
        source_dataset=indicator_generation_params.source_dataset.value,
        source_dataset_kwargs=indicator_generation_params.source_dataset_kwargs,
        gcm_list=indicator_generation_params.gcm_list,
        scenario_list=indicator_generation_params.scenario_list,
        threshold_list=indicator_generation_params.threshold_list,
        central_year_list=indicator_generation_params.central_year_list,
        central_year_historical=indicator_generation_params.central_year_historical,
        window_years=indicator_generation_params.window_years,
        bucket=indicator_generation_params.bucket,
        prefix=indicator_generation_params.prefix,
        store=indicator_generation_params.store,
        write_xarray_compatible_zarr=False,
        dask_cluster_kwargs=indicator_generation_params.dask_cluster_kwargs,
    )

@app.command()
def generate_indicators(indicator_generation_params: Annotated[IndicatorGenerationInput, typer.Argument(parser=parse_input)]):
    if indicator_generation_params.indicator == IndicatorType.degree_days:
        logger.info("Generating Degree Days Indicators")
        degree_days_indicator(indicator_generation_params)
    if indicator_generation_params.indicator == IndicatorType.days_tas_above:
        logger.info("Generating Days TAS Above Indicators")
        days_tas_above_indicator(indicator_generation_params)

@app.command()
def cubify_indicator(store_path: str, output_dir: str, indicator_name: str):
    cubify_invocation(store_path, output_dir, indicator_name)

@app.command()
def create_collection(sources: str, destination: str):
    collection_invocation(sources, destination)

@app.command()
def create_item(source: str, destination: str):
    item_invocation(source, destination)

if __name__ == "__main__":
    app()
