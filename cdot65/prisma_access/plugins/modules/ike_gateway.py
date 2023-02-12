"""
Ansible module for managing IKE Gateways in Prisma Access.
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
from panapi.config.network import IKEGateway

# jwt is not a float and causes an error of the token not being valid yet, ugh
import time

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ike_gateway

short_description: Manage IKE Gateway objects.

version_added: "0.1.3"

description: Manage IKE Gateway objects within Prisma Access.

options:
    description:
        description:
            - Description of the address object.
        required: false
        type: str
    dynamic:
        description:
            - declare the address group object is dynamic
        required: false
        type: dict
        options:
            filter:
                required: True
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
    name:
        description:
            - Value of the address group object's name
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
    static:
        description:
            - declare whether the address group object is static
        required: false
        type: list


extends_documentation_fragment:
    - cdot65.prisma_access.ike_gateway

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
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

"""


def main():
    """This is the main function that contains the logic for creating, modifying, and deleting an IKE Gateway on
        the Prisma Access platform.

    It takes no arguments and returns no values.

    It uses the AnsibleModule class to get the module's argument specification and process the results of the
        module's actions.

    Raises an exception if an error occurs during the module's execution.
    """
    module = AnsibleModule(argument_spec=PrismaAccessSpec.ike_gateway_spec())

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
    # 2. Create a dictionary representing the configuration settings for an IKE gateway.                             #
    #    `authentication`, `peer_address`, and `protocol_common` will be generated in the steps below.               #
    # -------------------------------------------------------------------------------------------------------------- #
    ike_gateway = {
        "name": module.params["name"],
        "folder": module.params["folder"],
        "local_address": {"interface": "vlan"},
        "peer_id": module.params["peer_id"],
        "protocol": module.params["protocol"],
        "authentication": {},
        "peer_address": {},
        "protocol_common": {},
    }

    # -------------------------------------------------------------------------------------------------------------- #
    # 3. Update the IKE gateway configuration dictionary with the selected authentication schema.                    #
    # -------------------------------------------------------------------------------------------------------------- #
    authentication = module.params["authentication"]

    if authentication["pre_shared_key"]:
        ike_gateway["authentication"]["pre_shared_key"] = {
            "key": authentication["pre_shared_key"]
        }
    elif authentication["certificate"]:
        ike_gateway["authentication"]["certificate"] = authentication[
            "certificate"
        ]
    else:
        module.fail_json(msg="Authentication method not specified")

    # -------------------------------------------------------------------------------------------------------------- #
    # 4. The following code updates the IKE gateway configuration dictionary with the selected peer_address.         #
    # -------------------------------------------------------------------------------------------------------------- #
    peer_address = module.params["peer_address"]
    if peer_address["ip"]:
        ike_gateway["peer_address"]["ip"] = peer_address["ip"]
    elif peer_address["fqdn"] or peer_address["dynamic"]:
        ike_gateway["peer_address"]["dynamic"] = {}
    else:
        module.fail_json(msg="Peer address not specified")

    # -------------------------------------------------------------------------------------------------------------- #
    # 5. The following code overrides the default values for the "protocol_common" dictionary of the IKE gateway     #
    #    configuration dictionary.                                                                                   #
    # -------------------------------------------------------------------------------------------------------------- #
    if module.params["protocol_common"]:
        # if protocol_common parameters are specified, use them to update the ike_gateway dictionary
        common = module.params["protocol_common"]
        if common["nat_traversal"]:
            ike_gateway["protocol_common"]["nat_traversal"] = {
                "enable": common["nat_traversal"]["enable"]
            }
        if common["fragmentation"]:
            ike_gateway["protocol_common"]["fragmentation"] = {
                "enable": common["fragmentation"]["enable"]
            }
    else:
        # if no protocol_common parameters are specified, use default values
        ike_gateway["protocol_common"] = {
            "nat_traversal": {"enable": True},
            "fragmentation": {"enable": False},
        }

    # -------------------------------------------------------------------------------------------------------------- #
    # 6. create an instance of the "IKEGateway" class using the ike_gateway dictionary.                              #
    # -------------------------------------------------------------------------------------------------------------- #
    try:
        # Create an IKEGateway object with the ike_gateway dictionary
        gateway = IKEGateway(**ike_gateway)

        # Check if an IKE gateway with the same name already exists
        already_exists = False
        existing_ike_gateway = gateway.list(session)

        for each in existing_ike_gateway:
            if gateway.name == each.name:
                already_exists = True
                gateway.id = each.id

        # Check the state parameter to see if the IKE gateway should be created or deleted
        if module.params["state"] == "absent":
            if already_exists is True:
                # Delete the IKE gateway if it exists
                gateway.delete(session)
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
                # Exit the module with a message saying the IKE gateway doesn't exist
                module.exit_json(
                    changed=False, data="Group does not exist, exiting"
                )
        else:
            if already_exists is False:
                # Create the IKE gateway if it doesn't exist
                gateway.create(session)
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
                # Exit the module with a message saying the IKE gateway already exists
                module.exit_json(
                    changed=False,
                    data=session.response.json(),
                )

    except Exception as exception_error:
        # If an exception occurs, fail the module and return an error message
        module.fail_json(msg=to_native(exception_error), exception=format_exc())


if __name__ == "__main__":
    main()
