=================================
cdot65.prisma_access.ipsec_tunnel
=================================

---------------------------
Manage IPsec Tunnel objects
---------------------------

ipsec_tunnel
============

This module will allow you to manage your IPsec Tunnel objects within Prisma Access.

Feature set as of version 0.1.5:
  - manage tags
  - idempotent

Under construction

Example
-------

Here is a basic example of using the module to mange your tags in Prisma Access

.. code-block:: yaml

    ---
    - name: Create IPsec Tunnel
      hosts: prisma
      connection: local
      gather_facts: False
      become: False
      collections:
        - cdot65.prisma_access

      tasks:
        - name: Create IKE Gateway Ansible-IKE-1
          cdot65.prisma_access.ike_gateway:
            provider:
              client_id: "{{ client_id }}"
              client_secret: "{{ client_secret }}"
              scope: "{{ scope }}"
            name: "Ansible-IKE-1"
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

        - name: Create IPsec Tunnel Ansible-IPsec-1
          cdot65.prisma_access.ipsec_tunnel:
            provider:
              client_id: "{{ client_id }}"
              client_secret: "{{ client_secret }}"
              scope: "{{ scope }}"
            name: "Ansible-IPsec-1"
            folder: "Service Connections"
            auto_key:
              ike_gateway:
                - name: "Ansible-IKE-1"
              ipsec_crypto_profile: "PaloAlto-Networks-IPSec-Crypto"
            anti_replay: True
            tunnel_monitor:
              enable: True
              destination_ip: "192.168.100.1"
            state: "present"

    - name: Delete IPsec Tunnel
      hosts: prisma
      connection: local
      gather_facts: False
      become: False
      collections:
        - cdot65.prisma_access

      tasks:
        - name: Delete IPsec Tunnel Ansible-IPsec-1
          cdot65.prisma_access.ipsec_tunnel:
            provider:
              client_id: "{{ client_id }}"
              client_secret: "{{ client_secret }}"
              scope: "{{ scope }}"
            name: "Ansible-IPsec-1"
            folder: "Service Connections"
            auto_key:
              ike_gateway:
                - name: "Ansible-IKE-1"
              ipsec_crypto_profile: "PaloAlto-Networks-IPSec-Crypto"
            anti_replay: True
            tunnel_monitor:
              enable: True
              destination_ip: "192.168.100.1"
            state: "absent"

        - name: Delete IKE Gateway Ansible-IKE-1
          cdot65.prisma_access.ike_gateway:
            provider:
              client_id: "{{ client_id }}"
              client_secret: "{{ client_secret }}"
              scope: "{{ scope }}"
            name: "Ansible-IKE-1"
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

Data Model
----------

If you'd like to see the options available for you within the module, have a look at the data model provided below. 

.. code-block:: python

    @staticmethod
    def ipsec_tunnel_spec():
        """Return the IPsec Tunnel object spec."""
        return dict(
            anti_replay=dict(
                required=False,
                type="bool",
                default=False,
            ),
            auto_key=dict(
                required=True,
                type="dict",
                options=dict(
                    ike_gateway=dict(
                        required=True,
                        type="list",
                        elements="dict",
                        options=dict(
                            name=dict(
                                required=True,
                                type="str",
                            ),
                        ),
                    ),
                    ipsec_crypto_profile=dict(
                        required=True,
                        type="str",
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
            tunnel_interface=dict(
                required=False,
                type="str",
                default="tunnel",
            ),
            tunnel_monitor=dict(
                required=True,
                type="dict",
                options=dict(
                    enable=dict(
                        required=False,
                        type="bool",
                        default=False,
                    ),
                    destination_ip=dict(
                        required=False,
                        type="str",
                    ),
                ),
            ),
        )
