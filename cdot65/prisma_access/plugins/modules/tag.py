"""
Ansible module for managing tags in Prisma Access.
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
from panapi.config.objects import Tag

# jwt is not a float and causes an error of the token not being valid yet, ugh
import time

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
        required=False,
        type='str'
    state:
        description:
            - declare whether you want the resource to exist or be deleted
        required: true
        choices:
          - 'absent'
          - 'present'
        type: str

extends_documentation_fragment:
    - cdot65.prisma_access.tag

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
    """
    The main function is the entry point for the script.
    It performs actions to create or delete a tag based on the state parameter.

    Summary of the main function:
      - sets up the required parameters
      - creates the necessary objects
      - performs actions on the objects.

    If the `state` parameter is set to "absent": the function will delete the tag (if it exists).

    If the `state` parameter is set to anything else: the function will create the tag (if it does not exist).

    If the tag already exists or is successfully deleted, the function will exit with a changed value of False.

    If the tag is successfully created or deleted, the function will exit with a changed value of True.

    The function may raise an Exception and will fail if an error occurs.
    """
    module = AnsibleModule(argument_spec=PrismaAccessSpec.tag_spec())

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

        tag = Tag(
            folder=module.params["folder"],
            name=module.params["name"],
            comments=module.params["comments"],
            color=module.params["color"],
            state=module.params["state"],
        )

        already_exists = False
        existing_tags = tag.list(session)

        for each in existing_tags:
            if tag.name == each.name:
                already_exists = True
                tag.id = each.id

        if module.params["state"] == "absent":
            if already_exists is True:
                tag.delete(session)
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
                    changed=False, data="Tag does not exist, exiting"
                )

        else:
            if already_exists is False:
                tag.create(session)
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
