from abc import ABCMeta

from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage, metaclass=ABCMeta):
    location = "static"
    default_acl = 'private'

    def _get_security_token(self):
        return None


class PublicMediaStorage(S3Boto3Storage, metaclass=ABCMeta):
    location = "media"
    default_acl = "private"
    file_overwrite = False

    def _get_security_token(self):
        return None


class PrivateMediaStorage(S3Boto3Storage, metaclass=ABCMeta):
    location = "private"
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False

    def _get_security_token(self):
        return None
