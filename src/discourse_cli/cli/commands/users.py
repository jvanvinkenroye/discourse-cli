"""User management commands."""

import click

from discourse_cli.api.client import DiscourseClient
from discourse_cli.cli.options import api_command, render


@click.group("users")
def users() -> None:
    """Manage users."""


@users.command("list")
@click.option("--flag", type=click.Choice(
    ["active", "new", "staff", "suspended", "blocked", "suspect"]
), help="Filter users by flag.")
@click.option("--order", help="Sort order field.")
@click.option("--asc", is_flag=True, help="Sort ascending.")
@click.option("--page", type=int, help="Page number.")
@click.option("--show-emails", is_flag=True, help="Show email addresses.")
@click.option("--email", help="Filter by email.")
@click.option("--ip", help="Filter by IP address.")
@api_command
def list_users(
    client: DiscourseClient,
    output_format: str,
    flag: str | None,
    order: str | None,
    asc: bool,
    page: int | None,
    show_emails: bool,
    email: str | None,
    ip: str | None,
) -> None:
    """List users (admin)."""
    if flag:
        data = client.admin_list_users_flag(
            flag,
            order=order,
            asc="true" if asc else None,
            page=page,
            show_emails=show_emails or None,
            email=email,
            ip=ip,
        )
    else:
        data = client.admin_list_users(
            order=order,
            asc="true" if asc else None,
            page=page,
            show_emails=show_emails or None,
            email=email,
            ip=ip,
        )
    # admin_list_users returns a list directly
    if isinstance(data, list):
        rows = [
            {
                "id": u.get("id"),
                "username": u.get("username"),
                "email": u.get("email", ""),
                "active": u.get("active"),
                "admin": u.get("admin"),
                "trust_level": u.get("trust_level"),
            }
            for u in data
        ]
        render(rows, output_format, title="Users")
    else:
        render(data, output_format, title="Users")


@users.command("get")
@click.argument("username")
@api_command
def get_user(
    client: DiscourseClient, output_format: str, username: str
) -> None:
    """Get user details by username."""
    data = client.get_user(username)
    user = data.get("user", data)
    render(user, output_format, title=f"User: {username}")


@users.command("get-by-id")
@click.argument("user_id", type=int)
@api_command
def get_user_by_id(
    client: DiscourseClient, output_format: str, user_id: int
) -> None:
    """Get user details by ID (admin)."""
    data = client.admin_get_user(user_id)
    render(data, output_format, title=f"User #{user_id}")


@users.command("create")
@click.option("--name", required=True, help="Display name.")
@click.option("--email", required=True, help="Email address.")
@click.option("--password", required=True, prompt=True, hide_input=True,
              help="Password.")
@click.option("--username", required=True, help="Username.")
@click.option("--active/--no-active", default=None, help="Activate immediately.")
@click.option("--approved/--no-approved", default=None, help="Approve immediately.")
@api_command
def create_user(
    client: DiscourseClient,
    output_format: str,
    name: str,
    email: str,
    password: str,
    username: str,
    active: bool | None,
    approved: bool | None,
) -> None:
    """Create a new user."""
    data = client.create_user(
        name=name,
        email=email,
        password=password,
        username=username,
        active=active,
        approved=approved,
    )
    render(data, output_format, title="Created User")


@users.command("update")
@click.argument("username")
@click.option("--name", help="New display name.")
@api_command
def update_user(
    client: DiscourseClient,
    output_format: str,
    username: str,
    name: str | None,
) -> None:
    """Update a user."""
    data = client.update_user(username, name=name)
    render(data, output_format, title=f"Updated User: {username}")


@users.command("delete")
@click.argument("user_id", type=int)
@click.option("--delete-posts", is_flag=True, help="Also delete user's posts.")
@click.option("--block-email", is_flag=True, help="Block the user's email.")
@click.option("--block-urls", is_flag=True, help="Block the user's URLs.")
@click.option("--block-ip", is_flag=True, help="Block the user's IP.")
@click.option("--yes", is_flag=True, help="Skip confirmation.")
@api_command
def delete_user(
    client: DiscourseClient,
    output_format: str,
    user_id: int,
    delete_posts: bool,
    block_email: bool,
    block_urls: bool,
    block_ip: bool,
    yes: bool,
) -> None:
    """Delete a user (admin)."""
    if not yes:
        click.confirm(f"Delete user #{user_id}?", abort=True)
    data = client.delete_user(
        user_id,
        delete_posts=delete_posts or None,
        block_email=block_email or None,
        block_urls=block_urls or None,
        block_ip=block_ip or None,
    )
    render(data, output_format, title="Deleted User")


@users.command("emails")
@click.argument("username")
@api_command
def get_emails(
    client: DiscourseClient, output_format: str, username: str
) -> None:
    """Get user's email addresses (admin)."""
    data = client.get_user_emails(username)
    render(data, output_format, title=f"Emails: {username}")


@users.command("update-username")
@click.argument("username")
@click.option("--new-username", required=True, help="New username.")
@api_command
def update_username(
    client: DiscourseClient,
    output_format: str,
    username: str,
    new_username: str,
) -> None:
    """Change a user's username."""
    data = client.update_username(username, new_username=new_username)
    render(data, output_format, title="Username Updated")


@users.command("update-email")
@click.argument("username")
@click.option("--email", required=True, help="New email address.")
@api_command
def update_email(
    client: DiscourseClient,
    output_format: str,
    username: str,
    email: str,
) -> None:
    """Change a user's email."""
    data = client.update_email(username, email=email)
    render(data, output_format, title="Email Updated")


@users.command("reset-password")
@click.argument("login")
@api_command
def reset_password(
    client: DiscourseClient, output_format: str, login: str
) -> None:
    """Send a password reset email."""
    data = client.send_password_reset_email(login=login)
    render(data, output_format, title="Password Reset")


@users.command("actions")
@click.argument("username")
@click.option("--filter", "filter_", required=True,
              help="Action type filter (e.g. '1' for likes).")
@click.option("--offset", type=int, default=0, help="Offset.")
@api_command
def user_actions(
    client: DiscourseClient,
    output_format: str,
    username: str,
    filter_: str,
    offset: int,
) -> None:
    """List user actions."""
    data = client.list_user_actions(
        offset=offset, username=username, filter=filter_
    )
    actions = data.get("user_actions", data)
    render(actions, output_format, title=f"Actions: {username}")


@users.command("by-external-id")
@click.argument("external_id")
@api_command
def by_external_id(
    client: DiscourseClient, output_format: str, external_id: str
) -> None:
    """Get user by external ID."""
    data = client.get_user_external_id(external_id)
    render(data, output_format, title=f"User (external: {external_id})")


@users.command("public")
@click.option("--period", required=True,
              type=click.Choice(["daily", "weekly", "monthly", "quarterly",
                                 "yearly", "all"]),
              help="Time period.")
@click.option("--order", required=True,
              type=click.Choice(["likes_received", "likes_given",
                                 "topic_count", "post_count",
                                 "topics_entered", "posts_read",
                                 "days_visited"]),
              help="Sort order.")
@click.option("--asc", is_flag=True, help="Sort ascending.")
@click.option("--page", type=int, help="Page number.")
@api_command
def public_users(
    client: DiscourseClient,
    output_format: str,
    period: str,
    order: str,
    asc: bool,
    page: int | None,
) -> None:
    """List public user directory."""
    data = client.list_users_public(
        period=period,
        order=order,
        asc="true" if asc else None,
        page=page,
    )
    users_list = data.get("directory_items", data)
    render(users_list, output_format, title="Public Users")
