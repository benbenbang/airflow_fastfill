"""
Automize backfill for Airflow

command examples:
    - afill -d all -p -m 30 -y
    - afill -d paco_bsf
explain:
    - run fastfill for the past 30 days without prompt, and only fill if all the dags which have status == pause
    - run fastfill for dag id == `paco_bsf` with maximum default backfill days == 365
note that the run id will be `migration_yyyy-mm-ddthh:mm:ss+00:00`
"""

# standard library
from pathlib import Path

# pypi/conda library
import click

# afill plugin
from afill.catchup import Datetime, fastfill
from afill.helpers.cfutils import logger, parse_date_cli


@click.command()
@click.option(
    "dag_id", "-d", default="", type=click.STRING, help="the dag name you want to backfill [dag_id or all]",
)
@click.option(
    "start_date",
    "-sd",
    default="",
    type=click.STRING,
    help="start date you want to backfill, default will fetch the start_date defined in the config of that dag",
    callback=parse_date_cli,
)
@click.option(
    "maximum", "-m", default=365, type=click.IntRange(min=0, max=365, clamp=True), help="maximum days to backfill",
)
@click.option("config_path", "-cp", default="", type=click.STRING, help="config for auto fastfill if have one")
@click.option("-i", default=False, is_flag=True, help="fill all ignore it just ran recently")
@click.option("-p", default=False, is_flag=True, help="only fill paused dags")
@click.option("-y", default=False, is_flag=True, help="confirm by default")
@click.option("-v", default=False, is_flag=True, help="print traceback if got error")
def ffcli(dag_id: str, start_date: Datetime, maximum: int, config_path: str, i: bool, p: bool, y: bool, v: bool):
    if not dag_id and not Path(f"{config_path}").is_file():
        logger.error("Need to assign a dag id or a path to config yaml")
        raise click.Abort()

    fastfill(dag_id, start_date, maximum, config_path, i, p, y, v)


if __name__ == "__main__":
    ffcli()
