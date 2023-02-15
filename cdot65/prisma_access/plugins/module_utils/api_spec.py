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
    def ike_gateway_spec():
        """Return the IKE gateway object spec."""
        return dict(
            authentication=dict(
                options=dict(
                    certificate=dict(
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
                                options=dict(
                                    local_certificate_name=dict(
                                        required=False,
                                        type="str",
                                    ),
                                ),
                                required=False,
                                type="dict",
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
                        required=False,
                        type="dict",
                    ),
                    pre_shared_key=dict(
                        required=False,
                        type="str",
                    ),
                ),
                required=True,
                type="dict",
            ),
            folder=dict(
                choices=[
                    "Mobile Users",
                    "Mobile Users Container",
                    "Mobile Users Explicit Proxy",
                    "Remote Networks",
                    "Service Connections",
                    "Shared",
                ],
                required=True,
                type="str",
            ),
            local_id=dict(
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
                required=False,
                type="dict",
            ),
            name=dict(
                max_length=63,
                required=True,
                type="str",
            ),
            peer_address=dict(
                options=dict(
                    dynamic=dict(
                        required=False,
                        type="bool",
                    ),
                    fqdn=dict(
                        max_length=255,
                        required=False,
                        type="str",
                    ),
                    ip=dict(
                        required=False,
                        type="str",
                    ),
                ),
                required=True,
                type="dict",
            ),
            peer_id=dict(
                options=dict(
                    id=dict(
                        max_length=1024,
                        required=True,
                        type="str",
                    ),
                    type=dict(
                        choices=[
                            "ipaddr",
                            "keyid",
                            "fqdn",
                            "ufqdn",
                        ],
                        required=True,
                        type="str",
                    ),
                ),
                required=True,
                type="dict",
            ),
            protocol=dict(
                options=dict(
                    ikev1=dict(
                        options=dict(
                            dpd=dict(
                                options=dict(
                                    enable=dict(
                                        required=False,
                                        type="bool",
                                    ),
                                ),
                                required=False,
                                type="dict",
                            ),
                            ike_crypto_profile=dict(
                                required=False,
                                type="str",
                            ),
                        ),
                        required=False,
                        type="dict",
                    ),
                    ikev2=dict(
                        options=dict(
                            dpd=dict(
                                options=dict(
                                    enable=dict(
                                        required=False,
                                        type="bool",
                                    ),
                                ),
                                required=False,
                                type="dict",
                            ),
                            ike_crypto_profile=dict(
                                required=False,
                                type="str",
                            ),
                        ),
                        required=False,
                        type="dict",
                    ),
                    version=dict(
                        choices=[
                            "ikev2-preferred",
                            "ikev1",
                            "ikev2",
                        ],
                        required=False,
                        type="str",
                    ),
                ),
                required=True,
                type="dict",
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

    @staticmethod
    def ipsec_tunnel_spec():
        """Return the IPsec Tunnel object spec."""
        return dict(
            anti_replay=dict(
                default=False,
                required=False,
                type="bool",
            ),
            auto_key=dict(
                options=dict(
                    ike_gateway=dict(
                        elements="dict",
                        options=dict(
                            name=dict(
                                required=True,
                                type="str",
                            ),
                        ),
                        required=True,
                        type="list",
                    ),
                    ipsec_crypto_profile=dict(
                        required=True,
                        type="str",
                    ),
                ),
                required=True,
                type="dict",
            ),
            folder=dict(
                choices=[
                    "Mobile Users",
                    "Mobile Users Container",
                    "Mobile Users Explicit Proxy",
                    "Remote Networks",
                    "Service Connections",
                    "Shared",
                ],
                required=True,
                type="str",
            ),
            name=dict(
                max_length=63,
                required=True,
                type="str",
            ),
            provider=dict(
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
                required=True,
                type="dict",
            ),
            state=dict(
                choices=["absent", "present"],
                required=True,
                type="str",
            ),
            tunnel_interface=dict(
                default="tunnel",
                required=False,
                type="str",
            ),
            tunnel_monitor=dict(
                options=dict(
                    enable=dict(
                        default=False,
                        required=False,
                        type="bool",
                    ),
                    destination_ip=dict(
                        required=False,
                        type="str",
                    ),
                ),
                required=True,
                type="dict",
            ),
        )

    @staticmethod
    def service_connection_spec():
        """Return the Service Connection object spec."""
        return dict(
            folder=dict(
                choices=[
                    "Mobile Users",
                    "Mobile Users Container",
                    "Mobile Users Explicit Proxy",
                    "Remote Networks",
                    "Service Connections",
                    "Shared",
                ],
                required=True,
                type="str",
            ),
            ipsec_tunnel=dict(
                max_length=63,
                required=True,
                type="str",
            ),
            name=dict(
                max_length=63,
                required=True,
                type="str",
            ),
            onboarding_type=dict(
                choices=[
                    "classic",
                ],
                default="classic",
                required=False,
                type="str",
            ),
            provider=dict(
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
                required=True,
                type="dict",
            ),
            region=dict(
                choices=[
                    "af-south-1",
                    "ap-northeast-1",
                    "ap-northeast-2",
                    "ap-south-1",
                    "ap-southeast-1",
                    "ap-southeast-2",
                    "asia-east1",
                    "asia-east2",
                    "asia-northeast2",
                    "asia-south1",
                    "asia-south2",
                    "asia-southeast1",
                    "asia-southeast2",
                    "australia-southeast1",
                    "australia-southeast2",
                    "ca-central-1",
                    "europe-north1",
                    "europe-southwest1",
                    "europe-west1",
                    "europe-west3",
                    "europe-west4",
                    "europe-west6",
                    "europe-west8",
                    "europe-west9",
                    "eu-central-1",
                    "eu-west-1",
                    "eu-west-2",
                    "eu-west-3",
                    "me-south-1",
                    "me-west1",
                    "northamerica-northeast2",
                    "sa-east-1",
                    "southamerica-east1",
                    "southamerica-west1",
                    "us-central1",
                    "us-east-1",
                    "us-east1",
                    "us-east-2",
                    "us-east4",
                    "us-south1",
                    "us-west-1",
                    "us-west1",
                    "us-west-2",
                ],
                required=True,
                type="str",
            ),
            state=dict(
                choices=["absent", "present"],
                required=True,
                type="str",
            ),
            subnets=dict(
                elements="str",
                max_items=64,
                required=True,
                type="list",
            ),
        )

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
