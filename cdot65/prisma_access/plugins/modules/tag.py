"""
Ansible module for managing tags in Prisma Access.
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
from panapi.config.objects import Tag

__metaclass__ = type

DOCUMENTATION = r"""
---
module: tag

short_description: Manage tag objects.

version_added: "0.1.0"

description: Manage tag objects within Prisma Access.

options:
    token:
        description:
            - used to authenticate to the API
        required: true
        type: str
    folder:
        description:
            - The folder you would like to associate to these tags goes here
        choices:
          - 'GlobalProtect'
          - 'Mobile Users'
          - 'Remote Networks'
          - 'Service Connections'
          - 'Shared'
        required: true
        type: str
    name:
        description:
            - Value of the tag's name
        required: true
        type: str
    comments:
        description:
            - Additional comments about the tag
        required: False
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
    - name: Create tags
      cdot65.prisma_access.tag:
        provider:
          client_id: "automation@1111111111.iam.panserviceaccount.com"
          client_secret: "11111111-1111-1111-1111-111111111111"
          scope: "1111111111"
        name: "{{ item.name }}"
        color: "{{ item.color }}"
        comments: "{{ item.comments }}"
        folder: "Service Connections"
        state: "present"
      loop:
        - name: "ansible-test"
          color: "Lavender"
          comments: "This is a test from Ansible"
"""


def main():
    """This is the main function that contains the logic for creating, modifying, and deleting an IKE Gateway on
        the Prisma Access platform.

    It takes no arguments and returns no values.

    It uses the AnsibleModule class to get the module's argument specification and process the results of the
        module's actions.

    Raises an exception if an error occurs during the module's execution.
    """
    module = AnsibleModule(argument_spec=PrismaAccessSpec.tag_spec())

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
    # 2. Create a dictionary representing the configuration settings for a tag.                                      #
    # -------------------------------------------------------------------------------------------------------------- #
    tag_object = {
        "name": module.params["name"],
        "folder": module.params["folder"],
        "color": module.params["color"],
        "comments": module.params["comments"],
    }

    # -------------------------------------------------------------------------------------------------------------- #
    # 3. create an instance of the "Tag" class using the tag_object dictionary.                                      #
    # -------------------------------------------------------------------------------------------------------------- #
    try:
        # Create an Tag object with the tag_object dictionary
        tag = Tag(**tag_object)

        # Check if a Tag with the same name already exists
        already_exists = False
        existing_tags = tag.list(session)

        for each in existing_tags:
            if tag.name == each.name:
                already_exists = True
                tag.id = each.id

        # Check the state parameter to see if the tag should be created or deleted
        if module.params["state"] == "absent":
            if already_exists is True:
                # Delete the tag if it exists
                tag.delete(session)
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
                # Exit the module with a message saying the tag doesn't exist
                module.exit_json(
                    changed=False, data="Tag does not exist, exiting"
                )

        else:
            if already_exists is False:
                # Create the tag if it doesn't exist
                tag.create(session)
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
                # Exit the module with a message saying the tag already exists
                module.exit_json(
                    changed=False,
                    data=session.response.json(),
                )

    except Exception as exception_error:
        # If an exception occurs, fail the module and return an error message
        module.fail_json(msg=to_native(exception_error), exception=format_exc())


if __name__ == "__main__":
    main()
