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
from panapi.config.objects import AddressGroup

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
    """This is the main function that contains the logic for creating, modifying,
        and deleting an Address Group on the Prisma Access platform.

    It takes no arguments and returns no values.

    It uses the AnsibleModule class to get the module's argument specification
        and process the results of the module's actions.

    Raises an exception if an error occurs during the module's execution.
    """
    module = AnsibleModule(argument_spec=PrismaAccessSpec.address_groups_spec())

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
    # 2. Create a dictionary representing the configuration settings for an Address Group.                           #
    # -------------------------------------------------------------------------------------------------------------- #
    address_group = {
        "description": module.params["description"],
        "folder": module.params["folder"],
        "name": module.params["name"],
    }

    # -------------------------------------------------------------------------------------------------------------- #
    # 3. Update the address_group configuration dictionary based on key/value pairs passed in Ansible module.        #
    # -------------------------------------------------------------------------------------------------------------- #
    if module.params["tag"]:
        address_group["tag"] = module.params["tag"]

    if module.params["static"]:
        address_group["static"] = module.params["static"]
    elif module.params["dynamic"]:
        address_group["dynamic"] = module.params["dynamic"]
    else:
        module.fail_json(
            msg="Must define either static or dynamic address group"
        )

    # -------------------------------------------------------------------------------------------------------------- #
    # 4. create an instance of the "AddressGroup" class using the address_group dictionary.                          #
    # -------------------------------------------------------------------------------------------------------------- #
    try:
        # Create an AddressGroup object with the ike_gateway dictionary
        group = AddressGroup(**address_group)

        # Check if an AddressGroup with the same name already exists
        already_exists = False
        existing_address_groups = group.list(session)

        for each in existing_address_groups:
            if group.name == each.name:
                already_exists = True
                group.id = each.id

        # Check the state parameter to see if the AddressGroup should be created or deleted
        if module.params["state"] == "absent":
            if already_exists is True:
                # Delete the AddressGroup if it exists
                group.delete(session)
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
                # Exit the module with a message saying the AddressGroup doesn't exist
                module.exit_json(
                    changed=False, data="Group does not exist, exiting"
                )

        else:
            if already_exists is False:
                # Create the AddressGroup if it doesn't exist
                group.create(session)
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
                # Exit the module with a message saying the AddressGroup already exists
                module.exit_json(
                    changed=False,
                    data=session.response.json(),
                )

    except Exception as exception_error:
        # If an exception occurs, fail the module and return an error message
        module.fail_json(msg=to_native(exception_error), exception=format_exc())


if __name__ == "__main__":
    main()
