"""
Ansible module for managing address objects in Prisma Access.
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
from panapi.config.objects import AddressGroup

# jwt is not a float and causes an error of the token not being valid yet, ugh
import time

__metaclass__ = type

DOCUMENTATION = r"""
---
module: address groups

short_description: Manage address group objects.

version_added: "0.1.2"

description: Manage address group objects within Prisma Access.

options:
    description:
        description:
            - Description of the address object.
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
    fqdn:
        description:
            - value of a fully qualified domain name
        required: false
        type: str
    ip_netmask:
        description:
            - value of a standard ip prefix formatted address
        required: false
        type: str
    ip_range:
        description:
            - value of a range of IP address groups
        required: false
        type: str
    ip_wildcard:
        description:
            - wildcard formatted ip address
        required: false
        type: str
    name:
        description:
            - Value of the address object's name
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


extends_documentation_fragment:
    - cdot65.prisma_access.address_groups

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
    - name: Create ip-netmask address group objects
      cdot65.prisma_access.address_groups:
        provider:
          client_id: "{{ client_id }}"
          client_secret: "{{ client_secret }}"
          scope: "{{ scope }}"
        description: "this is an example description"
        folder: "Service Connections"
        ip_netmask: "100.10.254.0/24"
        name: "Ansible Test"
        state: "present"
        tag: "Automation"

    - name: Create ip-range address group objects
      cdot65.prisma_access.address_groups:
        provider:
          client_id: "{{ client_id }}"
          client_secret: "{{ client_secret }}"
          scope: "{{ scope }}"
        description: "this is an example description"
        folder: "Service Connections"
        ip_range: "100.10.254.10-100.10.254.99"
        name: "Ansible Test"
        state: "present"
        tag: "Automation"

    - name: Create fqdn address group objects
      cdot65.prisma_access.address_groups:
        provider:
          client_id: "{{ client_id }}"
          client_secret: "{{ client_secret }}"
          scope: "{{ scope }}"
        description: "this is an example description"
        folder: "Service Connections"
        fqdn: "redtail.com"
        name: "Ansible Test"
        state: "present"
        tag: "Automation"

    - name: Create wildcard address group objects
      cdot65.prisma_access.address_groups:
        provider:
          client_id: "{{ client_id }}"
          client_secret: "{{ client_secret }}"
          scope: "{{ scope }}"
        description: "this is an example description"
        folder: "Service Connections"
        ip_wildcard: "100.0.6.0/0.0.248.255"
        name: "Ansible Test"
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
    module = AnsibleModule(argument_spec=PrismaAccessSpec.address_groups_spec())

    try:
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

        group = AddressGroup(
            description=module.params["description"],
            folder=module.params["folder"],
            name=module.params["name"],
            state=module.params["state"],
        )

        if module.params["static"]:
            group.__setattr__("static", module.params["static"])
        elif module.params["dynamic"]:
            group.__setattr__("dynamic", module.params["dynamic"])
        else:
            module.fail_json(
                msg="Must define either static or dynamic address group"
            )

        already_exists = False
        existing_address_groups = group.list(session)

        for each in existing_address_groups:
            if group.name == each.name:
                already_exists = True
                group.id = each.id

        # raise Exception(already_exists)

        if module.params["state"] == "absent":
            if already_exists is True:
                group.delete(session)
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
                group.create(session)
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
