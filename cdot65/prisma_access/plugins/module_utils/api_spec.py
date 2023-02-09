"""
This module provides a helper class for interacting with the Prisma Access API.

Copyright: (c) 2023, Calvin Remsburg (@cdot65) <cremsburg.dev@gmail.com.com>
Apache 2.0 License
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class PrismaAccessSpec:
    """Prisma Access Spec."""

    @staticmethod
    def tag_spec():
        """Return the tag object spec."""
        return dict(
            color=dict(
                type="str",
                required=False,
                default=False,
            ),
            comments=dict(
                type="str",
                required=False,
                default=False,
            ),
            folder=dict(
                required=True,
                choices=[
                    "GlobalProtect",
                    "Mobile Users",
                    "Remote Networks",
                    "Service Connections",
                    "Shared",
                ],
                type="str",
            ),
            name=dict(
                required=True,
                type="str",
            ),
            provider=dict(
                required=True,
                type="dict",
                options=dict(
                    client_id=dict(
                        required=True,
                        type="str",
                    ),
                    client_secret=dict(
                        required=True,
                        type="str",
                    ),
                    scope=dict(
                        required=True,
                        type="str",
                    ),
                ),
            ),
            state=dict(
                required=True,
                choices=["absent", "present"],
                type="str",
            ),
        )

    @staticmethod
    def addresses_spec():
        """Return the address object spec."""
        return dict(
            description=dict(
                max_length=1023,
                required=True,
                type="str",
            ),
            folder=dict(
                required=True,
                choices=[
                    "GlobalProtect",
                    "Mobile Users",
                    "Remote Networks",
                    "Service Connections",
                    "Shared",
                ],
                type="str",
            ),
            fqdn=dict(
                required=False,
                type="str",
            ),
            ip_netmask=dict(
                required=False,
                type="str",
            ),
            ip_range=dict(
                required=False,
                type="str",
            ),
            ip_wildcard=dict(
                required=False,
                type="str",
            ),
            name=dict(
                max_length=63,
                required=True,
                type="str",
            ),
            provider=dict(
                required=True,
                type="dict",
                options=dict(
                    client_id=dict(
                        required=True,
                        type="str",
                    ),
                    client_secret=dict(
                        required=True,
                        type="str",
                    ),
                    scope=dict(
                        required=True,
                        type="str",
                    ),
                ),
            ),
            state=dict(
                required=True,
                choices=["absent", "present"],
                type="str",
            ),
            tag=dict(
                elements="str",
                max_items=64,
                required=False,
                type="list",
            ),
        )
