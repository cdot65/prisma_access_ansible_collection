"""
Ansible module for managing IKE Gateways in Prisma Access.
Copyright: (c) 2023, Calvin Remsburg (@cdot65) <cremsburg.dev@gmail.com>
"""
from __future__ import absolute_import, division, print_function
from traceback import format_exc
from ansible.module_utils.basic import (
    AnsibleModule,
)
from ansible.module_utils._text import (
    to_native,
)
from ansible_collections.cdot65.prisma_access.plugins.module_utils.api_spec import (
    PrismaAccessSpec,
)

# Prisma Access SDK
from panapi import PanApiSession
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
    - name: Create address group
      cdot65.prisma_access.address_groups:
        provider:
          client_id: "{{ client_id }}"
          client_secret: "{{ client_secret }}"
          scope: "{{ scope }}"
        name: "AnsibleTestGroupStatic"
        folder: "Service Connections"
        description: "This is just a test"
        static:
          - "AnsibleTestAddress"
        tag:
          - "ansible-test"
        state: "present"

    - name: Create address group
      cdot65.prisma_access.address_groups:
        provider:
          client_id: "{{ client_id }}"
          client_secret: "{{ client_secret }}"
          scope: "{{ scope }}"
        name: "AnsibleTestGroupDynamic"
        folder: "Service Connections"
        description: "This is just a test"
        dynamic:
          filter: "'ansible-test'"
        tag:
          - "ansible-test"
        state: "present"

"""


def main():
    """
    The main function is the entry point for the script.
    It performs actions to create or delete an address based on the state parameter.

    Summary of the main function:
      - sets up the required parameters
      - creates the necessary objects
      - performs actions on the objects.

    If the `state` parameter is set to "absent": the function will delete the address (if it exists).

    If the `state` parameter is set to anything else: the function will create the address (if it does not exist).

    If the address already exists or is successfully deleted, the function will exit with a changed value of False.

    If the address is successfully created or deleted, the function will exit with a changed value of True.

    The function may raise an Exception and will fail if an error occurs.
    """
    module = AnsibleModule(argument_spec=PrismaAccessSpec.ike_gateway_spec())

    try:
        # create an authenticated session object
        auth = module.params.get("provider")
        session = PanApiSession()
        session.authenticate(
            client_id=auth["client_id"],
            client_secret=auth["client_secret"],
            scope=f'profile tsg_id:{auth["scope"]} email',
            token_url="https://auth.apps.paloaltonetworks.com/am/oauth2/access_token",
        )

        # jwt isn't a float, causing an error of the token not being valid yet
        time.sleep(1)

        ike_gateway = {
            "name": module.params["name"],
            "folder": module.params["folder"],
            "local_address": {"interface": "vlan"},
            "authentication": {},
            "peer_id": module.params["peer_id"],
            "peer_address": {},
            "protocol_common": {},
            "protocol": {
                "ikev1": {
                    "ike_crypto_profile": "PaloAlto-Networks-IKE-Crypto",
                    "dpd": {"enable": True},
                },
                "ikev2": {
                    "ike_crypto_profile": "PaloAlto-Networks-IKE-Crypto",
                    "dpd": {"enable": True},
                },
                "version": "ikev2-preferred",
            },
        }

        # update parameters with the selected authentication schema
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

        # update parameters with the selected peer_address
        peer_address = module.params["peer_address"]
        if peer_address["ip"]:
            ike_gateway["peer_address"]["ip"] = peer_address["ip"]
        elif peer_address["fqdn"] or peer_address["dynamic"]:
            ike_gateway["peer_address"]["dynamic"] = {}
        else:
            module.fail_json(msg="Peer address not specified")

        # override defaults for protocol_common
        if module.params["protocol_common"]:
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
            ike_gateway["protocol_common"] = {
                "nat_traversal": {"enable": True},
                "fragmentation": {"enable": False},
            }

        # raise Exception(ike_gateway)

        gateway = IKEGateway(**ike_gateway)

        already_exists = False
        existing_ike_gateway = gateway.list(session)

        for each in existing_ike_gateway:
            if gateway.name == each.name:
                already_exists = True
                gateway.id = each.id

        # raise Exception(already_exists)

        if module.params["state"] == "absent":
            if already_exists is True:
                gateway.delete(session)
                if session.response.status_code != 200:
                    module.fail_json(
                        msg=f"Did not receive proper response: {session.response.text}"
                    )
                module.exit_json(
                    changed=True,
                    data=session.response.json(),
                )
            else:
                module.exit_json(
                    changed=False, data="Group does not exist, exiting"
                )

        else:
            if already_exists is False:
                gateway.create(session)
                if session.response.status_code != 201:
                    module.fail_json(
                        msg=f"Did not receive proper response: {session.response.text}"
                    )
                module.exit_json(
                    changed=True,
                    data=session.response.json(),
                )
            else:
                module.exit_json(
                    changed=False,
                    data=session.response.json(),
                )

    except Exception as exception_error:
        module.fail_json(msg=to_native(exception_error), exception=format_exc())


if __name__ == "__main__":
    main()
