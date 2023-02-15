"""
Ansible module for managing Service Connections in Prisma Access.
Copyright: (c) 2023, Calvin Remsburg (@cdot65) <cremsburg.dev@gmail.com>
"""
from __future__ import absolute_import, division, print_function
from traceback import format_exc
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from ..module_utils.api_spec import (
    PrismaAccessSpec,
)
from ..module_utils.authenticate import (
    get_authenticated_session,
)

# Prisma Access SDK
from panapi.config.network import ServiceConnection

__metaclass__ = type

DOCUMENTATION = r"""
---
module: service_connection

short_description: Manage Service Connections objects.

version_added: "0.1.6

description: Manage Service Connections objects within Prisma Access.

options:
    backup_sc:
        description:
            - Backup Service Connection.
        required: false
        type: str
    bgp_peer:
        description:
            - Parameters of the BGP session
        required: false
        type: dict
        options:
            local_ip_address:
                description:
                    - Local IPv4 address
                required: false
                type: str
            local_ipv6_address:
                description:
                    - Local IPv6 address
                required: false
                type: str
            peer_ip_address:
                description:
                    - Remote IPv4 address
                required: false
                type: str
            peer_ipv6_address:
                description:
                    - Remote IPv6 address
                required: false
                type: str
            same_as_primary:
                description:
                    - Flag if the BGP session is the same as the primary session
                required: false
                type: str
            secret:
                description:
                    - BGP secret
                required: false
                type: str
    folder:
        choices:
          - "Shared"
          - "Mobile Users"
          - "Remote Networks"
          - "Service Connections"
          - "Mobile Users Container"
          - "Mobile Users Explicit Proxy"
        description:
            - declare where the object should reside.
        required: true
        type: str
    ipsec_tunnel:
        description:
            - name of IPsec tunnel to use
        required: true
        type: str
    name:
        description:
            - name of service connection
        required: true
        type: str
    nat_pool:
        description:
            - name of NAT pool
        required: false
        type: str
    no_export_community:
        description:
            - disable export community
        required: false
        type: str
        choices:
            - "Disabled"
            - "Enabled-In"
            - "Enabled-Out"
            - "Enabled-Both"
    protocol:
        description:
            - protocol to use
        required: false
        type: dict
        options:
            bgp:
                description:
                    - BGP parameters
                required: false
                type: dict
                options:
                    - do_not_export_routes:
                        description:
                            - do not export routes
                        required: false
                        type: bool
                    - enable:
                        description:
                            - enable BGP
                        required: false
                        type: bool
                    - fast_failover:
                        description:
                            - fast failover
                        required: false
                        type: bool
                    - local_ip_address
                        description:
                            - local IP address
                        required: false
                        type: str
                    - originate_default_route:
                        description:
                            - originate default route
                        required: false
                        type: bool
                    - peer_as:
                        description:
                            - peer AS
                        required: false
                        type: str
                    - peer_ip_address:
                        description:
                            - peer IP address
                        required: false
                        type: str
                    - secret:
                        description:
                            - secret
                        required: false
                        type: str
                    - summarize_mobile_user_routes:
                        description:
                            - summarize mobile user routes
                        required: false
                        type: bool
    qos:
        description:
            - QoS parameters
        required: false
        type: dict
        options:
            enable:
                description:
                    - enable QoS
                required: false
                type: bool
            qos_profile:
                description:
                    - QoS profile
                required: false
                type: str
    onboarding_type:
        description:
            - onboarding type
        required: false
        type: str
        choices:
            - "classic"
    region:
        description:
            - region
        required: false
        type: str
        choices:
            - "af-south-1",
            - "ap-northeast-1",
            - "ap-northeast-2",
            - "ap-south-1",
            - "ap-southeast-1",
            - "ap-southeast-2",
            - "asia-east1",
            - "asia-east2",
            - "asia-northeast2",
            - "asia-south1",
            - "asia-south2",
            - "asia-southeast1",
            - "asia-southeast2",
            - "australia-southeast1",
            - "australia-southeast2",
            - "ca-central-1",
            - "europe-north1",
            - "europe-southwest1",
            - "europe-west1",
            - "europe-west3",
            - "europe-west4",
            - "europe-west6",
            - "europe-west8",
            - "europe-west9",
            - "eu-central-1",
            - "eu-west-1",
            - "eu-west-2",
            - "eu-west-3",
            - "me-south-1",
            - "me-west1",
            - "northamerica-northeast2",
            - "sa-east-1",
            - "southamerica-east1",
            - "southamerica-west1",
            - "us-central1",
            - "us-east-1",
            - "us-east1",
            - "us-east-2",
            - "us-east4",
            - "us-south1",
            - "us-west-1",
            - "us-west1",
            - "us-west-2",
    state:
        description:
            - declare whether you want the resource to exist or be deleted
        required: true
        choices:
          - 'absent'
          - 'present'
        type: str
    secondary_ipsec_tunnel:
        description:
            - backup IPsec tunnel
        required: false
        type: str
    source_nat:
        description:
            - enable source nat
        required: false
        type: book
    subnets:
        description:
            - subnets
        required: false
        type: list
        elements: str

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
    ---
    - name: Create Service Connection
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

        - name: Create Service Connection Ansible-IPsec-1
          cdot65.prisma_access.service_connection:
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

    - name: Delete Service Connection
      hosts: prisma
      connection: local
      gather_facts: False
      become: False
      collections:
        - cdot65.prisma_access

      tasks:
        - name: Delete Service Connection Ansible-IPsec-1
          cdot65.prisma_access.service_connection:
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

"""


def main():
    """This is the main function that contains the logic for creating, modifying, and deleting a Service Connections on
        the Prisma Access platform.

    It takes no arguments and returns no values.

    It uses the AnsibleModule class to get the module's argument specification and process the results of the
        module's actions.

    Raises an exception if an error occurs during the module's execution.
    """
    module = AnsibleModule(
        argument_spec=PrismaAccessSpec.service_connection_spec()
    )

    # -------------------------------------------------------------------------------------------------------------- #
    # 1. Authenticate the session object using the client_id, client_secret, scope, and token_url parameters passed  #
    #    through the Ansible module.                                                                                 #
    # -------------------------------------------------------------------------------------------------------------- #
    try:
        # get the provider parameter from the Ansible module, which includes the authentication credentials
        session = get_authenticated_session(module)

    except Exception as exception_error:
        # if an exception occurs during the authentication process, fail the module and return an error message
        module.fail_json(msg=to_native(exception_error), exception=format_exc())

    # -------------------------------------------------------------------------------------------------------------- #
    # 2. Create a dictionary representing the configuration settings for a Service Connection.                       #
    # -------------------------------------------------------------------------------------------------------------- #
    service_connection = {
        "name": module.params["name"],
        "folder": module.params["folder"],
        "ipsec_tunnel": module.params["ipsec_tunnel"],
        "region": module.params["region"],
        "subnets": module.params["subnets"],
    }

    # -------------------------------------------------------------------------------------------------------------- #
    # 3. account for optional parameters, appending them to the dictionary only if they are declared in the playbook #
    # -------------------------------------------------------------------------------------------------------------- #
    if module.params["backup_sc"]:
        service_connection["backup_sc"] = module.params["backup_sc"]

    if module.params["bgp_peer"]:
        service_connection["bgp_peer"] = module.params["bgp_peer"]

    if module.params["nat_pool"]:
        service_connection["nat_pool"] = module.params["nat_pool"]

    if module.params["no_export_community"]:
        service_connection["no_export_community"] = module.params[
            "no_export_community"
        ]

    if module.params["protocol"]:
        service_connection["protocol"] = module.params["protocol"]

    if module.params["qos"]:
        service_connection["qos"] = module.params["qos"]

    if module.params["secondary_ipsec_tunnel"]:
        service_connection["secondary_ipsec_tunnel"] = module.params[
            "secondary_ipsec_tunnel"
        ]

    if module.params["source_nat"]:
        service_connection["source_nat"] = module.params["source_nat"]

    # -------------------------------------------------------------------------------------------------------------- #
    # 4. create an instance of the "ServiceConnection" class using the service_connection dictionary.                #
    # -------------------------------------------------------------------------------------------------------------- #
    try:
        # Create an ServiceConnection object with the service_connection dictionary
        connection = ServiceConnection(**service_connection)

        # Check if an Service Connection with the same name already exists
        already_exists = False
        existing_service_connection = connection.list(session)

        for each in existing_service_connection:
            if connection.name == each.name:
                already_exists = True
                connection.id = each.id

        # Check the state parameter to see if the Service Connection should be created or deleted
        if module.params["state"] == "absent":
            if already_exists is True:
                # Delete the Service Connection if it exists
                connection.delete(session)
                if session.response.status_code != 200:
                    module.fail_json(
                        msg=f"Did not receive proper response: {session.response.text}"
                    )
                # Exit the module with a success message
                module.exit_json(
                    changed=True,
                    data=session.response.json(),
                )
            else:
                # Exit the module with a message saying the Service Connection doesn't exist
                module.exit_json(
                    changed=False, data="Group does not exist, exiting"
                )
        else:
            if already_exists is False:
                # Create the Service Connection if it doesn't exist
                connection.create(session)
                if session.response.status_code != 201:
                    module.fail_json(
                        msg=f"Did not receive proper response: {session.response.text}"
                    )
                # Exit the module with a success message
                module.exit_json(
                    changed=True,
                    data=session.response.json(),
                )
            else:
                # Exit the module with a message saying the Service Connection already exists
                module.exit_json(
                    changed=False,
                    data=session.response.json(),
                )

    except Exception as exception_error:
        # If an exception occurs, fail the module and return an error message
        module.fail_json(msg=to_native(exception_error), exception=format_exc())


if __name__ == "__main__":
    main()
