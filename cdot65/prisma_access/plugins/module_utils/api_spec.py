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
    def address_spec():
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

    @staticmethod
    def address_group_spec():
        """Return the address groups object spec."""
        return dict(
            description=dict(
                max_length=1023,
                required=True,
                type="str",
            ),
            dynamic=dict(
                required=False,
                type="dict",
                options=dict(
                    filter=dict(
                        required=True,
                        type="str",
                    ),
                ),
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
            static=dict(
                elements="str",
                max_items=64,
                required=False,
                type="list",
            ),
            tag=dict(
                elements="str",
                max_items=64,
                required=False,
                type="list",
            ),
        )

    @staticmethod
    def ike_gateway_spec():
        """Return the IKE gateway object spec."""
        return dict(
            authentication=dict(
                required=True,
                type="dict",
                options=dict(
                    pre_shared_key=dict(
                        required=False,
                        type="str",
                    ),
                    certificate=dict(
                        required=False,
                        type="dict",
                        options=dict(
                            allow_id_payload_mismatch=dict(
                                required=False,
                                type="bool",
                            ),
                            certificate_profile=dict(
                                required=False,
                                type="str",
                            ),
                            local_certificate=dict(
                                required=False,
                                type="dict",
                                options=dict(
                                    local_certificate_name=dict(
                                        required=False,
                                        type="str",
                                    ),
                                ),
                            ),
                            strict_validation_revocation=dict(
                                required=False,
                                type="bool",
                            ),
                            use_management_as_source=dict(
                                required=False,
                                type="bool",
                            ),
                        ),
                    ),
                ),
            ),
            folder=dict(
                required=True,
                choices=[
                    "Mobile Users",
                    "Mobile Users Container",
                    "Mobile Users Explicit Proxy",
                    "Remote Networks",
                    "Service Connections",
                    "Shared",
                ],
                type="str",
            ),
            local_id=dict(
                required=False,
                type="dict",
                options=dict(
                    id=dict(
                        required=False,
                        type="str",
                    ),
                    type=dict(
                        required=False,
                        type="str",
                    ),
                ),
            ),
            name=dict(
                max_length=63,
                required=True,
                type="str",
            ),
            peer_address=dict(
                required=True,
                type="dict",
                options=dict(
                    ip=dict(
                        required=False,
                        type="str",
                    ),
                    fqdn=dict(
                        required=False,
                        type="str",
                        max_length=255,
                    ),
                    dynamic=dict(
                        required=False,
                        type="bool",
                    ),
                ),
            ),
            peer_id=dict(
                required=True,
                type="dict",
                options=dict(
                    id=dict(
                        required=True,
                        type="str",
                        max_length=1024,
                    ),
                    type=dict(
                        required=True,
                        type="str",
                        choices=[
                            "ipaddr",
                            "keyid",
                            "fqdn",
                            "ufqdn",
                        ],
                    ),
                ),
            ),
            protocol=dict(
                required=True,
                type="dict",
                options=dict(
                    ikev1=dict(
                        required=False,
                        type="dict",
                        options=dict(
                            dpd=dict(
                                required=False,
                                type="dict",
                                options=dict(
                                    enable=dict(
                                        required=False,
                                        type="bool",
                                    ),
                                ),
                            ),
                            ike_crypto_profile=dict(
                                required=False,
                                type="str",
                            ),
                        ),
                    ),
                    ikev2=dict(
                        required=False,
                        type="dict",
                        options=dict(
                            dpd=dict(
                                required=False,
                                type="dict",
                                options=dict(
                                    enable=dict(
                                        required=False,
                                        type="bool",
                                    ),
                                ),
                            ),
                            ike_crypto_profile=dict(
                                required=False,
                                type="str",
                            ),
                        ),
                    ),
                    version=dict(
                        required=False,
                        type="str",
                        choices=[
                            "ikev2-preferred",
                            "ikev1",
                            "ikev2",
                        ],
                    ),
                ),
            ),
            protocol_common=dict(
                required=False,
                type="dict",
                options=dict(
                    fragmentation=dict(
                        required=False,
                        type="dict",
                        options=dict(
                            enable=dict(
                                required=False,
                                type="bool",
                            ),
                        ),
                    ),
                    nat_traversal=dict(
                        required=False,
                        type="dict",
                        options=dict(
                            enable=dict(
                                required=False,
                                type="bool",
                            ),
                        ),
                    ),
                    passive_mode=dict(
                        required=False,
                        type="bool",
                    ),
                ),
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
