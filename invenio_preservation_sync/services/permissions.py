# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Permissions for the service layer to process the Preservation Sync requests."""

from flask_principal import ActionNeed
from invenio_records_permissions import BasePermissionPolicy
from invenio_records_permissions.generators import Generator, SystemProcess
from invenio_search.engine import dsl

archiver_action = ActionNeed("archiver")


class Archiver(Generator):
    """Allows system_process role."""

    def needs(self, **kwargs):
        """Enabling Needs."""
        return [archiver_action]

    def query_filter(self, identity=None, **kwargs):
        """Filters for current identity as system process."""
        for need in identity.provides:
            if need == archiver_action:
                return dsl.Q("match_all")
        else:
            return []


class DefaultPreservationInfoPermissionPolicy(BasePermissionPolicy):
    """Default permission policy to read and write the PreservationInfo."""

    can_create = [Archiver(), SystemProcess()]
    can_read = [Archiver(), SystemProcess()]