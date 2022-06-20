import datetime

from sqlalchemy.ext.declarative import declared_attr

from flask import request

from ...utils.timezone_helpers import get_formatted_local_time
from ...utils import constants

from ..base import db


class AuditColumnsMixin:
    @declared_attr
    def created_by(self):
        return db.Column(
            db.String(20), nullable=False, default="system", server_default="system"
        )

    @declared_attr
    def created_at(self):
        return db.Column(
            db.DateTime,
            nullable=False,
            default=datetime.datetime.utcnow,
            server_default=db.text("NOW()"),
        )

    @declared_attr
    def updated_by(self):
        return db.Column(
            db.String(20), nullable=False, default="system", server_default="system"
        )

    @declared_attr
    def updated_at(self):
        return db.Column(
            db.DateTime,
            nullable=False,
            default=datetime.datetime.utcnow,
            server_default=db.text("NOW()"),
            onupdate=datetime.datetime.utcnow,
            server_onupdate=db.text("NOW()"),
        )

    def get_local_time(
        self,
        datetime_in_db,
        datetime_format=constants.FORMAT_DATETIME_STANDARD_FOR_DISPLAY,
    ):
        return get_formatted_local_time(
            request.user.time_zone, datetime_in_db, datetime_format
        )
