"""Discourse API client modules."""
from discourse_cli.api.client import DiscourseClient
from discourse_cli.api.admin import AdminMixin
from discourse_cli.api.backups import BackupsMixin
from discourse_cli.api.badges import BadgesMixin
from discourse_cli.api.categories import CategoriesMixin
from discourse_cli.api.events import EventsMixin
from discourse_cli.api.groups import GroupsMixin
from discourse_cli.api.invites import InvitesMixin
from discourse_cli.api.notifications import NotificationsMixin
from discourse_cli.api.posts import PostsMixin
from discourse_cli.api.private_messages import PrivateMessagesMixin
from discourse_cli.api.search import SearchMixin
from discourse_cli.api.site import SiteMixin
from discourse_cli.api.tags import TagsMixin
from discourse_cli.api.topics import TopicsMixin
from discourse_cli.api.uploads import UploadsMixin
from discourse_cli.api.users import UsersMixin

__all__ = ['DiscourseClient', 'AdminMixin', 'BackupsMixin', 'BadgesMixin', 'CategoriesMixin', 'EventsMixin', 'GroupsMixin', 'InvitesMixin', 'NotificationsMixin', 'PostsMixin', 'PrivateMessagesMixin', 'SearchMixin', 'SiteMixin', 'TagsMixin', 'TopicsMixin', 'UploadsMixin', 'UsersMixin']
