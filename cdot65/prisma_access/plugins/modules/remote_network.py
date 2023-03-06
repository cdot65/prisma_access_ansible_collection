"""
Ansible module for managing Remote Networks in Prisma Access.
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
from panapi.config.network import RemoteNetwork

__metaclass__ = type

DOCUMENTATION = r"""
---
module: remote_network

short_description: Manage Remote Networks objects.

version_added: "0.1.8

description: Manage Remote Networks objects within Prisma Access.

options:
    bgp_peer:
        description: BGP peer information.
        options:
            - local_ip_address:
                description: "local IP address"
                required: false
                type: str
            - peer_ip_address:
                description: "peer IP address"
                required: false
                type: str
            - secret:
                description: "BGP shared secret"
                required: false
                type: str
        required: false
        type: dict
    ecmp_load_balancing:
        choices:
            - "disabled"
            - "enabled"
        description: Determine if ECMP is enabled.
        required: false
        type: str
    ecmp_tunnels:
        description: ECMP tunnel information.
        options:
            - do_not_export_routes:
                description: "prevent exporting of routes"
                required: false
                type: bool
            - ipsec_tunnel:
                description: "name of IPsec tunnel"
                required: true
                type: str
            - local_ip_address:
                description: "local IP address"
                required: false
                type: str
            - name:
                description: "name of ECMP tunnel"
                required: false
                type: str
            - originate_default_route:
                description: "determine if default route is originated"
                required: false
                type: bool
            - peer_as:
                description: "BGP peer AS"
                required: false
                type: str
            - peer_ip_address:
                description: "Peer IP address"
                required: false
                type: str
            - peering_type:
                choices:
                    - exchange-v4-over-v4
                    - exchange-v4-v6-over-v4
                    - exchange-v4-over-v4-v6-over-v6
                    - exchange-v6-over-v6
                description: "Peering types"
                required: false
                type: str
            - secret:
                description: "BGP shared secret"
                required: false
                type: str
            - summarize_mobile_user_routes:
                description: "Determine if mobile user routes are summarized"
                required: false
                type: bool
        required: false
        type: dict
    folder:
        choices:
          - "Shared"
          - "Mobile Users"
          - "Remote Networks"
          - "Remote Networks"
          - "Mobile Users Container"
          - "Mobile Users Explicit Proxy"
        description:
            - declare where the object should reside.
        required: true
        type: str
    ipsec_tunnel:
        description: name of IPsec tunnel to use
        required: true
        type: str
    license_type:
        choices:
            - "FWAAS-AGGREGATE"
        default: "FWAAS-AGGREGATE"
        description: name of license type
        required: true
        type: str
    name:
        description: name of Remote Network
        required: true
        type: str
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
    region:
        description:
            - QoS parameters
        required: false
        type: dict
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
    secondary_ipsec_tunnel:
        description: backup IPsec tunnel
        required: false
        type: str
    spn_name:
        description: name of SPN
        required: false
        type: str
    state:
        description:
            - declare whether you want the resource to exist or be deleted
        required: true
        choices:
          - 'absent'
          - 'present'
        type: str
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
- name: CREATE Remote Networks
  hosts: prisma
  connection: local
  gather_facts: False
  become: False
  collections:
    - cdot65.prisma_access

  tasks:
    - name: CREATE IKE Gateway Ansible-RN-IKE-1
      cdot65.prisma_access.ike_gateway:
        provider:
          client_id: "{{ client_id }}"
          client_secret: "{{ client_secret }}"
          scope: "{{ scope }}"
        name: "Ansible-RN-IKE-1"
        folder: "Remote Networks"
        peer_id:
          id: "73.206.3.129"
          type: "ipaddr"
        authentication:
          pre_shared_key: "paloalto1!"
        peer_address:
          ip: "73.206.3.129"
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

    - name: CREATE IPsec Tunnel Ansible-RN-IPsec-1
      cdot65.prisma_access.ipsec_tunnel:
        provider:
          client_id: "{{ client_id }}"
          client_secret: "{{ client_secret }}"
          scope: "{{ scope }}"
        name: "Ansible-RN-IPsec-1"
        folder: "Remote Networks"
        auto_key:
          ike_gateway:
            - name: "Ansible-RN-IKE-1"
          ipsec_crypto_profile: "PaloAlto-Networks-IPSec-Crypto"
        anti_replay: True
        tunnel_monitor:
          enable: True
          destination_ip: "192.168.100.1"
        state: "present"

    - name: CREATE Remote Network Ansible-RN-1
      cdot65.prisma_access.remote_network:
        provider:
          client_id: "{{ client_id }}"
          client_secret: "{{ client_secret }}"
          scope: "{{ scope }}"
        name: "Ansible-RN-1"
        folder: "Remote Networks"
        ecmp_load_balancing: "disable"
        ipsec_tunnel: "Ansible-RN-IPsec-1"
        license_type: "FWAAS-AGGREGATE"
        protocol:
          bgp:
            enable: True
            local_ip_address: "192.168.1.1"
            peer_as: "65001"
            peer_ip_address: "192.168.1.2"
            peering_type: "exchange-v4-over-v4"
            secret: "thisisjustasecret"
            summarize_mobile_user_routes: True
        bgp_peer:
          local_ip_address: "192.168.1.1"
          peer_ip_address: "192.168.1.2"
          secret: "thisisjustasecret"
        region: "us-south1"
        secondary_ipsec_tunnel: "GUI-Test-Tunnel2"
        spn_name: "us-south-raspberry"
        state: "present"

"""


def main():
    """This is the main function that contains the logic for creating, modifying, and deleting a Remote Networks on
        the Prisma Access platform.

    It takes no arguments and returns no values.

    It uses the AnsibleModule class to get the module's argument specification and process the results of the
        module's actions.

    Raises an exception if an error occurs during the module's execution.
    """
    module = AnsibleModule(argument_spec=PrismaAccessSpec.remote_network_spec())

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
    # 2. Create a dictionary representing the configuration settings for a Remote Network.                           #
    # -------------------------------------------------------------------------------------------------------------- #
    remote_network = {
        "name": module.params["name"],
        "folder": module.params["folder"],
        "license_type": module.params["license_type"],
        "protocol": module.params["protocol"],
        "region": module.params["region"],
    }

    # -------------------------------------------------------------------------------------------------------------- #
    # 3. account for optional parameters, appending them to the dictionary only if they are declared in the playbook #
    # -------------------------------------------------------------------------------------------------------------- #
    if module.params["ecmp_load_balancing"]:
        remote_network["ecmp_load_balancing"] = module.params[
            "ecmp_load_balancing"
        ]

    if module.params["ecmp_tunnels"]:
        remote_network["ecmp_tunnels"] = module.params["ecmp_tunnels"]

    if module.params["ipsec_tunnel"]:
        remote_network["ipsec_tunnel"] = module.params["ipsec_tunnel"]

    if module.params["secondary_ipsec_tunnel"]:
        remote_network["secondary_ipsec_tunnel"] = module.params[
            "secondary_ipsec_tunnel"
        ]

    if module.params["spn_name"]:
        remote_network["spn_name"] = module.params["spn_name"]

    if module.params["subnets"]:
        remote_network["subnets"] = module.params["subnets"]

    # -------------------------------------------------------------------------------------------------------------- #
    # 4. create an instance of the "RemoteNetwork" class using the remote_network dictionary.                        #
    # -------------------------------------------------------------------------------------------------------------- #
    try:
        # Create an RemoteNetwork object with the remote_network dictionary
        connection = RemoteNetwork(**remote_network)

        # Check if an Remote Network with the same name already exists
        already_exists = False
        existing_remote_network = connection.list(session)

        for each in existing_remote_network:
            if connection.name == each.name:
                already_exists = True
                connection.id = each.id

        # Check the state parameter to see if the Remote Network should be created or deleted
        if module.params["state"] == "absent":
            if already_exists is True:
                # Delete the Remote Network if it exists
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
                # Exit the module with a message saying the Remote Network doesn't exist
                module.exit_json(
                    changed=False, data="Group does not exist, exiting"
                )
        else:
            if already_exists is False:
                # Create the Remote Network if it doesn't exist
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
                # Exit the module with a message saying the Remote Network already exists
                module.exit_json(
                    changed=False,
                    data=session.response.json(),
                )

    except Exception as exception_error:
        # If an exception occurs, fail the module and return an error message
        module.fail_json(msg=to_native(exception_error), exception=format_exc())


if __name__ == "__main__":
    main()
