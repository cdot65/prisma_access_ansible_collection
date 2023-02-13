"""
Ansible module for managing IPsec tunnels in Prisma Access.
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
from panapi.config.network import IPSecTunnel

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ipsec_tunnel

short_description: Manage IPsec tunnels objects.

version_added: "0.1.5"

description: Manage IPsec tunnels objects within Prisma Access.

options:
    anti_replay:
        description:
            - Enable or disable anti-replay.
        required: false
        type: bool
    auto_key:
        description:
            - Parameters of the IPsec tunnel
        required: true
        type: dict
        options:
            ike_gateway:
                description:
                    - IKE gateway name
                required: true
                type: list
                elements: dict
                options:
                    name:
                        description:
                            - IKE gateway name
                        required: true
                        type: str
            ipsec_crypto_profile:
                description:
                    - IPsec crypto profile name
                required: true
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
    state:
        description:
            - declare whether you want the resource to exist or be deleted
        required: true
        choices:
          - 'absent'
          - 'present'
        type: str
    tunnel_interface:
        description:
            - for future use
        required: false
        type: str
        default: "tunnel"
    tunnel_monitor:
        description:
            - monitor the tunnel interface
        required: true
        type: dict
        options:
            enable:
                description:
                    - enable or disable tunnel monitoring
                required: false
                type: bool
            destination_ip:
                description:
                    - destination IP address
                required: false
                type: str


author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
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

"""


def main():
    """This is the main function that contains the logic for creating, modifying, and deleting an IPsec tunnels on
        the Prisma Access platform.

    It takes no arguments and returns no values.

    It uses the AnsibleModule class to get the module's argument specification and process the results of the
        module's actions.

    Raises an exception if an error occurs during the module's execution.
    """
    module = AnsibleModule(argument_spec=PrismaAccessSpec.ipsec_tunnel_spec())

    # -------------------------------------------------------------------------------------------------------------- #
    # 1. Authenticate the session object using the client_id, client_secret, scope, and token_url parameters passed
    #    through the Ansible module.
    # -------------------------------------------------------------------------------------------------------------- #
    try:
        # get the provider parameter from the Ansible module, which includes the authentication credentials
        session = get_authenticated_session(module)

    except Exception as exception_error:
        # if an exception occurs during the authentication process, fail the module and return an error message
        module.fail_json(msg=to_native(exception_error), exception=format_exc())

    # -------------------------------------------------------------------------------------------------------------- #
    # 2. Create a dictionary representing the configuration settings for an IPsec tunnel.                             #
    # -------------------------------------------------------------------------------------------------------------- #
    ipsec_tunnel = {
        "name": module.params["name"],
        "folder": module.params["folder"],
        # "tunnel_interface": module.params["tunnel_interface"],
        "auto_key": module.params["auto_key"],
        "anti_replay": module.params["anti_replay"],
        "tunnel_monitor": module.params["tunnel_monitor"],
    }

    # -------------------------------------------------------------------------------------------------------------- #
    # 3. create an instance of the "IPSecTunnel" class using the ipsec_tunnel dictionary.                              #
    # -------------------------------------------------------------------------------------------------------------- #
    try:
        # Create an IPSecTunnel object with the ipsec_tunnel dictionary
        tunnel = IPSecTunnel(**ipsec_tunnel)

        # Check if an IPsec tunnel with the same name already exists
        already_exists = False
        existing_ipsec_tunnel = tunnel.list(session)

        for each in existing_ipsec_tunnel:
            if tunnel.name == each.name:
                already_exists = True
                tunnel.id = each.id

        # Check the state parameter to see if the IPsec tunnel should be created or deleted
        if module.params["state"] == "absent":
            if already_exists is True:
                # Delete the IPsec tunnel if it exists
                tunnel.delete(session)
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
                # Exit the module with a message saying the IPsec tunnel doesn't exist
                module.exit_json(
                    changed=False, data="Group does not exist, exiting"
                )
        else:
            if already_exists is False:
                # Create the IPsec tunnel if it doesn't exist
                tunnel.create(session)
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
                # Exit the module with a message saying the IPsec tunnel already exists
                module.exit_json(
                    changed=False,
                    data=session.response.json(),
                )

    except Exception as exception_error:
        # If an exception occurs, fail the module and return an error message
        module.fail_json(msg=to_native(exception_error), exception=format_exc())


if __name__ == "__main__":
    main()
