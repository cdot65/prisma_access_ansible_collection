================================
cdot65.prisma_access.ike_gateway
================================

--------------------------
Manage IKE Gateway objects
--------------------------

ike_gateway
===========

This module will allow you to manage your IKE Gateway objects within Prisma Access.

Feature set as of version 0.1.3:
  - manage tags
  - idempotent

Under construction

Example
-------

Here is a basic example of using the module to mange your tags in Prisma Access

.. code-block:: yaml

  ---
  # TEST
  - hosts: prisma
    connection: local
    gather_facts: False
    become: False
    collections:
      - cdot65.prisma_access

    tasks:
      - name: Create IKE Gateway AnsibleIKE-1
        cdot65.prisma_access.ike_gateway:
          provider:
            client_id: "{{ client_id }}"
            client_secret: "{{ client_secret }}"
            scope: "{{ scope }}"
          name: "AnsibleIKE-1"
          folder: "Service Connections"
          peer_id:
            id: "1.1.1.3"
            type: "ipaddr"
          authentication:
            pre_shared_key: "paloalto1!"
          peer_address:
            ip: "1.1.1.2"
          protocol:
            ikev1:
              ike_crypto_profile: "PaloAlto-Networks-IKE-Crypto"
              dpd:
                enable: True
            ikev2:
              ike_crypto_profile: "PaloAlto-Networks-IKE-Crypto"
              dpd:
                enable: True
            version: "ikev2-preferred"
          state: "present"

      - name: Create IKE Gateway AnsibleIKE-2
        cdot65.prisma_access.ike_gateway:
          provider:
            client_id: "{{ client_id }}"
            client_secret: "{{ client_secret }}"
            scope: "{{ scope }}"
          name: "AnsibleIKE-2"
          folder: "Service Connections"
          peer_id:
            id: "vpn.redtail.com"
            type: "fqdn"
          authentication:
            pre_shared_key: "paloalto1!"
          peer_address:
            dynamic: True
          protocol_common:
            nat_traversal:
              enable: True
            fragmentation:
              enable: False
          protocol:
            ikev1:
              ike_crypto_profile: "PaloAlto-Networks-IKE-Crypto"
              dpd:
                enable: True
            ikev2:
              ike_crypto_profile: "PaloAlto-Networks-IKE-Crypto"
              dpd:
                enable: True
            version: "ikev2-preferred"
          state: "present"

      - name: Create IKE Gateway AnsibleIKE-3
        cdot65.prisma_access.ike_gateway:
          provider:
            client_id: "{{ client_id }}"
            client_secret: "{{ client_secret }}"
            scope: "{{ scope }}"
          name: "AnsibleIKE-3"
          folder: "Service Connections"
          peer_id:
            id: "calvin@vpn.redtail.com"
            type: "ufqdn"
          authentication:
            pre_shared_key: "paloalto1!"
          peer_address:
            dynamic: True
          protocol:
            ikev1:
              ike_crypto_profile: "PaloAlto-Networks-IKE-Crypto"
              dpd:
                enable: True
            ikev2:
              ike_crypto_profile: "PaloAlto-Networks-IKE-Crypto"
              dpd:
                enable: True
            version: "ikev2-preferred"
          state: "present"

      - name: Create IKE Gateway AnsibleIKE-4
        cdot65.prisma_access.ike_gateway:
          provider:
            client_id: "{{ client_id }}"
            client_secret: "{{ client_secret }}"
            scope: "{{ scope }}"
          name: "AnsibleIKE-4"
          folder: "Service Connections"
          peer_id:
            id: "deadbeef"
            type: "keyid"
          authentication:
            pre_shared_key: "paloalto1!"
          peer_address:
            dynamic: True
          protocol:
            ikev1:
              ike_crypto_profile: "PaloAlto-Networks-IKE-Crypto"
              dpd:
                enable: True
            ikev2:
              ike_crypto_profile: "PaloAlto-Networks-IKE-Crypto"
              dpd:
                enable: True
            version: "ikev2-preferred"
          state: "present"

  # DELETE
  - hosts: prisma
    connection: local
    gather_facts: False
    become: False
    collections:
      - cdot65.prisma_access

    tasks:
      - name: Delete IKE Gateway AnsibleIKE-1
        cdot65.prisma_access.ike_gateway:
          provider:
            client_id: "{{ client_id }}"
            client_secret: "{{ client_secret }}"
            scope: "{{ scope }}"
          name: "AnsibleIKE-1"
          folder: "Service Connections"
          peer_id:
            id: "1.1.1.3"
            type: "ipaddr"
          authentication:
            pre_shared_key: "paloalto1!"
          peer_address:
            ip: "1.1.1.2"
          protocol:
            ikev1:
              ike_crypto_profile: "PaloAlto-Networks-IKE-Crypto"
              dpd:
                enable: True
            ikev2:
              ike_crypto_profile: "PaloAlto-Networks-IKE-Crypto"
              dpd:
                enable: True
            version: "ikev2-preferred"
          state: "absent"

      - name: Delete IKE Gateway AnsibleIKE-2
        cdot65.prisma_access.ike_gateway:
          provider:
            client_id: "{{ client_id }}"
            client_secret: "{{ client_secret }}"
            scope: "{{ scope }}"
          name: "AnsibleIKE-2"
          folder: "Service Connections"
          peer_id:
            id: "vpn.redtail.com"
            type: "fqdn"
          authentication:
            pre_shared_key: "paloalto1!"
          peer_address:
            dynamic: True
          protocol_common:
            nat_traversal:
              enable: True
            fragmentation:
              enable: False
          protocol:
            ikev1:
              ike_crypto_profile: "PaloAlto-Networks-IKE-Crypto"
              dpd:
                enable: True
            ikev2:
              ike_crypto_profile: "PaloAlto-Networks-IKE-Crypto"
              dpd:
                enable: True
            version: "ikev2-preferred"
          state: "absent"

      - name: Delete IKE Gateway AnsibleIKE-3
        cdot65.prisma_access.ike_gateway:
          provider:
            client_id: "{{ client_id }}"
            client_secret: "{{ client_secret }}"
            scope: "{{ scope }}"
          name: "AnsibleIKE-3"
          folder: "Service Connections"
          peer_id:
            id: "calvin@vpn.redtail.com"
            type: "ufqdn"
          authentication:
            pre_shared_key: "paloalto1!"
          peer_address:
            ip: "1.1.1.2"
          protocol:
            ikev1:
              ike_crypto_profile: "PaloAlto-Networks-IKE-Crypto"
              dpd:
                enable: True
            ikev2:
              ike_crypto_profile: "PaloAlto-Networks-IKE-Crypto"
              dpd:
                enable: True
            version: "ikev2-preferred"
          state: "absent"

      - name: Delete IKE Gateway AnsibleIKE-4
        cdot65.prisma_access.ike_gateway:
          provider:
            client_id: "{{ client_id }}"
            client_secret: "{{ client_secret }}"
            scope: "{{ scope }}"
          name: "AnsibleIKE-4"
          folder: "Service Connections"
          peer_id:
            id: "deadbeef"
            type: "keyid"
          authentication:
            pre_shared_key: "paloalto1!"
          peer_address:
            dynamic: True
          protocol:
            ikev1:
              ike_crypto_profile: "PaloAlto-Networks-IKE-Crypto"
              dpd:
                enable: True
            ikev2:
              ike_crypto_profile: "PaloAlto-Networks-IKE-Crypto"
              dpd:
                enable: True
            version: "ikev2-preferred"
          state: "absent"


Data Model
----------

If you'd like to see the options available for you within the module, have a look at the data model provided below. 

.. code-block:: python

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
