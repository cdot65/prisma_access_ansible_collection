=======================================
cdot65.prisma_access.service_connection
=======================================

--------------------------
Manage Service Connections
--------------------------

service_connection
==================

This module will allow you to manage your Service Connections within Prisma Access.

Feature set as of version 0.1.6:
  - manage service connections
  - idempotent

Under construction

Example
-------

Here is a basic example of using the module to mange your tags in Prisma Access

.. code-block:: yaml

    - name: CREATE Service Connection
      hosts: prisma
      connection: local
      gather_facts: False
      become: False
      collections:
        - cdot65.prisma_access

      tasks:
        - name: CREATE IKE Gateway Ansible-IKE-1
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

        - name: CREATE IPsec Tunnel Ansible-IPsec-1
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

        - name: CREATE Service Connection
          cdot65.prisma_access.service_connection:
            provider:
              client_id: "{{ client_id }}"
              client_secret: "{{ client_secret }}"
              scope: "{{ scope }}"
            name: "Ansible-SC-1"
            folder: "Service Connections"
            ipsec_tunnel: "Ansible-IPsec-1"
            region: "us-central1"
            subnets:
              - "192.168.111.0/24"
              - "192.168.112.0/24"
            state: "present"

    - name: DELETE Service Connection
      hosts: prisma
      connection: local
      gather_facts: False
      become: False
      collections:
        - cdot65.prisma_access

      tasks:
        - name: DELETE Service Connection
          cdot65.prisma_access.service_connection:
            provider:
              client_id: "{{ client_id }}"
              client_secret: "{{ client_secret }}"
              scope: "{{ scope }}"
            name: "Ansible-SC-1"
            folder: "Service Connections"
            ipsec_tunnel: "Ansible-IPsec-1"
            region: "us-central1"
            subnets:
              - "192.168.111.0/24"
              - "192.168.112.0/24"
            state: "absent"

        - name: DELETE IPsec Tunnel Ansible-IPsec-1
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

        - name: DELETE IKE Gateway Ansible-IKE-1
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
    def service_connection_spec():
        """Return the Service Connection object spec."""
        return dict(
            backup_sc=dict(
                required=False,
                type="str",
            ),
            bgp_peer=dict(
                required=False,
                type="dict",
                options=dict(
                    local_ip_address=dict(
                        required=False,
                        type="str",
                    ),
                    local_ipv6_address=dict(
                        required=False,
                        type="str",
                    ),
                    peer_ip_address=dict(
                        required=False,
                        type="str",
                    ),
                    peer_ipv6_address=dict(
                        required=False,
                        type="str",
                    ),
                    same_as_primary=dict(
                        required=False,
                        type="bool",
                    ),
                    secret=dict(
                        required=False,
                        type="str",
                    ),
                ),
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
            nat_pool=dict(
                required=False,
                type="str",
            ),
            no_export_community=dict(
                required=False,
                type="str",
                choices=[
                    "Disabled",
                    "Enabled-In",
                    "Enabled-Out",
                    "Enabled-Both",
                ],
            ),
            protocol=dict(
                required=False,
                type="dict",
                options=dict(
                    bgp=dict(
                        required=False,
                        type="dict",
                        options=dict(
                            do_not_export_routes=dict(
                                required=False,
                                type="bool",
                            ),
                            enable=dict(
                                required=False,
                                type="bool",
                            ),
                            fast_failover=dict(
                                required=False,
                                type="bool",
                            ),
                            local_ip_address=dict(
                                required=False,
                                type="str",
                            ),
                            originate_default_route=dict(
                                required=False,
                                type="bool",
                            ),
                            peer_as=dict(
                                required=False,
                                type="str",
                            ),
                            peer_ip_address=dict(
                                required=False,
                                type="str",
                            ),
                            secret=dict(
                                required=False,
                                type="str",
                            ),
                            summarize_mobile_user_routes=dict(
                                required=False,
                                type="bool",
                            ),
                        ),
                    ),
                ),
            ),
            qos=dict(
                required=False,
                type="dict",
                options=dict(
                    enable=dict(
                        required=False,
                        type="bool",
                    ),
                    qos_profile=dict(
                        required=False,
                        type="str",
                    ),
                ),
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
            secondary_ipsec_tunnel=dict(
                required=False,
                type="str",
            ),
            source_nat=dict(
                required=False,
                type="bool",
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
