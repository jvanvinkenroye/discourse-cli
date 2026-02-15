"""Upload commands."""

import click

from discourse_cli.api.client import DiscourseClient
from discourse_cli.cli.options import api_command, render


@click.group("uploads")
def uploads() -> None:
    """Manage uploads."""


@uploads.command("create")
@click.option("--type", "type_", required=True,
              type=click.Choice(["avatar", "profile_background",
                                 "card_background", "custom_emoji",
                                 "composer"]),
              help="Upload type.")
@click.option("--user-id", type=int, help="User ID for the upload.")
@click.option("--synchronous", is_flag=True, help="Synchronous upload.")
@api_command
def create_upload(
    client: DiscourseClient,
    output_format: str,
    type_: str,
    user_id: int | None,
    synchronous: bool,
) -> None:
    """Create an upload."""
    data = client.create_upload(
        type_=type_,
        user_id=user_id,
        synchronous=synchronous or None,
    )
    render(data, output_format, title="Upload Created")


@uploads.command("create-multipart")
@click.option("--upload-type", required=True, help="Upload type.")
@click.option("--file-name", required=True, help="File name.")
@click.option("--file-size", required=True, type=int, help="File size.")
@api_command
def create_multipart(
    client: DiscourseClient,
    output_format: str,
    upload_type: str,
    file_name: str,
    file_size: int,
) -> None:
    """Create a multipart upload."""
    data = client.create_multipart_upload(
        upload_type=upload_type,
        file_name=file_name,
        file_size=file_size,
    )
    render(data, output_format, title="Multipart Upload Created")


@uploads.command("complete-external")
@click.option("--unique-identifier", required=True, help="Upload identifier.")
@api_command
def complete_external(
    client: DiscourseClient,
    output_format: str,
    unique_identifier: str,
) -> None:
    """Complete an external upload."""
    data = client.complete_external_upload(
        unique_identifier=unique_identifier,
    )
    render(data, output_format, title="External Upload Completed")
