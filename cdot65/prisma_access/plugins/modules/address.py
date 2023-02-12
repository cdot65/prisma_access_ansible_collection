"""
Ansible module for managing address objects in Prisma Access.
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
from panapi.config.objects import Address

__metaclass__ = type

DOCUMENTATION = r"""
---
module: address

short_description: Manage address objects.

version_added: "0.1.1"

description: Manage address objects within Prisma Access.

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
            - value of a range of IP addresses
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


author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
    - name: Create ip-netmask address objects
      cdot65.prisma_access.address:
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

    - name: Create ip-range address objects
      cdot65.prisma_access.address:
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

    - name: Create fqdn address objects
      cdot65.prisma_access.address:
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

    - name: Create wildcard address objects
      cdot65.prisma_access.address:
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
    """This is the main function that contains the logic for creating, modifying,
        and deleting an Address Object on the Prisma Access platform.

    It takes no arguments and returns no values.

    It uses the AnsibleModule class to get the module's argument specification
        and process the results of the module's actions.

    Raises an exception if an error occurs during the module's execution.
    """
    module = AnsibleModule(argument_spec=PrismaAccessSpec.address_spec())

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
    # 2. Create a dictionary representing the configuration settings for an Address.                                 #
    # -------------------------------------------------------------------------------------------------------------- #
    address = {
        "description": module.params["description"],
        "folder": module.params["folder"],
        "name": module.params["name"],
    }

    # -------------------------------------------------------------------------------------------------------------- #
    # 3. Update the address configuration dictionary based on key/value pairs passed in Ansible module.              #
    # -------------------------------------------------------------------------------------------------------------- #
    if module.params["tag"]:
        address["tag"] = module.params["tag"]

    if module.params["fqdn"]:
        address["fqdn"] = module.params["fqdn"]
    elif module.params["ip_netmask"]:
        address["ip_netmask"] = module.params["ip_netmask"]
    elif module.params["ip_range"]:
        address["ip_range"] = module.params["ip_range"]
    elif module.params["ip_wildcard"]:
        address["ip_wildcard"] = module.params["ip_wildcard"]
    else:
        module.fail_json(
            msg="Must define ip_netmask, ip_range, ip_wildcard, or fqdn"
        )

    # -------------------------------------------------------------------------------------------------------------- #
    # 4. create an instance of the "Address" class using the address dictionary.                                     #
    # -------------------------------------------------------------------------------------------------------------- #
    try:
        # Create an Address object with the address dictionary
        address = Address(**address)

        # Check if an Address with the same name already exists
        already_exists = False
        existing_address = address.list(session)

        for each in existing_address:
            if address.name == each.name:
                already_exists = True
                address.id = each.id

        # Check the state parameter to see if the Address should be created or deleted
        if module.params["state"] == "absent":
            if already_exists is True:
                # Delete the Address if it exists
                address.delete(session)
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
                # Exit the module with a message saying the Address doesn't exist
                module.exit_json(
                    changed=False, data="Address does not exist, exiting"
                )

        else:
            if already_exists is False:
                # Create the Address if it doesn't exist
                address.create(session)
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
                # Exit the module with a message saying the Address already exists
                module.exit_json(
                    changed=False,
                    data=session.response.json(),
                )

    except Exception as exception_error:
        # If an exception occurs, fail the module and return an error message
        module.fail_json(msg=to_native(exception_error), exception=format_exc())


if __name__ == "__main__":
    main()
