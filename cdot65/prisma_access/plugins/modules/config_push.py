"""
Ansible module for pushing configuration in Prisma Access.
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
from panapi.config.management import ConfigVersion

__metaclass__ = type

DOCUMENTATION = r"""
---
module: config_push

short_description: Push candidate configuration to Prisma.

version_added: "0.1.7

description: Push candidate configuration to Prisma.

options:
    description:
        description:
            - Provide a description for the commit operation.
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
        elements: "str"
        required: true
        type: list

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
    ---
    - name: Push candidate configuration
      hosts: prisma
      connection: local
      gather_facts: False
      become: False
      collections:
        - cdot65.prisma_access

      tasks:
        - name: Push candidate configuration
          cdot65.prisma_access.config_push:
            provider:
              client_id: "{{ client_id }}"
              client_secret: "{{ client_secret }}"
              scope: "{{ scope }}"
            description: "Test push from Ansible"
            folders:
              - "Remote Networks"

"""


def main():
    """This is the main function that contains the logic for performing candidate configuration pushes on
        the Prisma Access platform.

    It takes no arguments and returns no values.

    It uses the AnsibleModule class to get the module's argument specification and process the results of the
        module's actions.

    Raises an exception if an error occurs during the module's execution.
    """
    module = AnsibleModule(
        argument_spec=PrismaAccessSpec.config_push()
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
    # 2. Create a dictionary representing the candidate configuration push parameters from the playbook.             #
    # -------------------------------------------------------------------------------------------------------------- #
    config_push = {
        "description": module.params["description"],
        "folders": module.params["folders"],
    }

    # -------------------------------------------------------------------------------------------------------------- #
    # 3. create an instance of the "ConfigVersion" class using the config_push dictionary.                           #
    # -------------------------------------------------------------------------------------------------------------- #
    try:
        # Create an ConfigVersion object with the config_push dictionary
        candidate_config_push = ConfigVersion(**config_push)

        # Push candidate configuration
        candidate_config_push.push(session)
        if session.response.status_code != 200:
            module.fail_json(
                msg=f"Did not receive proper response: {session.response.text} with code {session.response.status_code}"
            )
        # Exit the module with a success message
        module.exit_json(
            changed=True,
            data=session.response.json(),
        )

    except Exception as exception_error:
        # If an exception occurs, fail the module and return an error message
        module.fail_json(msg=to_native(exception_error), exception=format_exc())


if __name__ == "__main__":
    main()
