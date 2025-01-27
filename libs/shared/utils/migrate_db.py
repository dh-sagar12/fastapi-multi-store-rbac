import logging
import re
import click
from ..config.settings import settings
from libs.shared.utils.logger import logger
from libs.shared.utils.permission_generator import PermissionCreator


def create_permissions(dry_run, verbose, model):
    """Create CRUD permissions for all models or specified models."""
    try:
        if verbose:
            logger.setLevel(logging.INFO)

        # Get database URL from settings if not provided
        db_url = settings.POSTGRES_WRITE_URL

        if not db_url:
            raise click.UsageError(
                "Database URL must be provided via DATABASE_URL environment variable"
            )

        masked_db_url = re.sub(r":([^@]+)@", ":***@", db_url)

        logger.info(f"Using database: {masked_db_url}")

        creator = PermissionCreator(db_url)

        all_models = creator.get_all_model_names()

        target_models = set(model) if model else set(all_models)
        invalid_models = target_models - set(all_models)
        if invalid_models:
            raise click.UsageError(
                f"Invalid models specified: {', '.join(invalid_models)}\n"
                f"Available models: {', '.join(all_models)}"
            )

        if dry_run:
            permissions = creator.get_pending_permissions(target_models)
            if not permissions:
                click.echo("No new permissions to create.")
                return

            click.echo("The following permissions would be created:")
            for perm in permissions:
                click.echo(f"  - {perm['name']}: {perm['code']}")
        else:
            creator.create_crud_permissions(target_models)
            click.echo("Permissions created successfully!")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise click.ClickException(str(e))


def list_permissions():
    """List all existing permissions in the database."""
    try:
        db_url = settings.POSTGRES_WRITE_URL
        creator = PermissionCreator(db_url)
        permissions = creator.list_permissions()

        if not permissions:
            click.echo("No permissions found in the database.")
            return

        # Group permissions by model
        by_model = {}
        for perm in permissions:
            if perm.model_name not in by_model:
                by_model[perm.model_name] = []
            by_model[perm.model_name].append(perm)

        # Display permissions
        for model, perms in sorted(by_model.items()):
            click.echo(f"\n{model}:")
            for perm in sorted(perms, key=lambda x: x.name):
                click.echo(f"  - {perm.name}")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise click.ClickException(str(e))
