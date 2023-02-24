================================
cdot65.prisma_access.config_push
================================

-----------------------------
Push candidate configurations
-----------------------------

config_push
===========

This module will allow you to push your candidate configurations within Prisma Access.

Feature set as of version 0.1.7:
  - push configurations

Under construction

Example
-------

Here is a basic example of using the module to mange your tags in Prisma Access

.. code-block:: yaml

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


Data Model
----------

If you'd like to see the options available for you within the module, have a look at the data model provided below. 

.. code-block:: python

    @staticmethod
    def config_push():
        """Return the address object spec."""
        return dict(
            description=dict(
                max_length=1023,
                required=False,
                type="str",
            ),
            folders=dict(
                choices=[
                    "Mobile Users",
                    "Mobile Users Container",
                    "Mobile Users Explicit Proxy",
                    "Remote Networks",
                    "Service Connections",
                ],
                elements="str",
                required=True,
                type="list",
            ),
            provider=dict(
                required=True,
                type="dict",
                options=dict(
                    client_id=dict(
                        required=True,
                        type="str",
                    ),
                    client_secret=dict(
                        required=True,
                        type="str",
                    ),
                    scope=dict(
                        required=True,
                        type="str",
                    ),
                ),
            ),
        )
