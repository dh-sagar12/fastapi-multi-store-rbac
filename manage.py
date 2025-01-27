import subprocess
import click

from alembic.seed.seeder import seed_master_data
from libs.shared.utils.logger import logger
from libs.shared.utils.migrate_db import create_permissions


@click.group
def commands():
    pass


@commands.command()
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what permissions would be created without actually creating them.",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
@click.option(
    "--model",
    "-m",
    multiple=True,
    help="Create permissions only for specific models. Can be used multiple times.",
)
@click.option(
    "--version",
    multiple=False,
    help="Create permissions only for specific alembic Version",
)
def migrate(dry_run, verbose, model, version):
    logger.info("Running database migrations...")
    alembic_command = ["alembic", "upgrade", version if version else "head"]
    result = subprocess.run(alembic_command, capture_output=True, text=True)
    if result.returncode == 0:
        create_permissions(dry_run, verbose, model)


@commands.command()
def seed():
    seed_master_data()


if __name__ == "__main__":
    commands()
