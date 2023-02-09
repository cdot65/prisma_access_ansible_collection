========================
cdot65.prisma_access.tag
========================

------------------
Manage tag objects
------------------

tag
===

This module will allow you to manage your tag objects within Prisma Access.

Feature set as of version 0.1.0:
  - manage tags
  - idempotent

Under construction

Example
-------

Here is a basic example of using the module to mange your tags in Prisma Access

.. code-block:: yaml

    ---
    # CONFIGURE TAG OBJECTS
    - hosts: prisma
      connection: local
      gather_facts: False
      become: False
      collections:
        - cdot65.prisma_access

      tasks:
        - name: Create tags
          cdot65.prisma_access.tag:
            provider:
              client_id: "{{ client_id }}"
              client_secret: "{{ client_secret }}"
              scope: "{{ scope }}"
            name: "ansible"
            color: "Lavender"
            comments: "This is a test tag"
            folder: "Service Connections"
            state: "present"



Data Model
----------

If you'd like to see the options available for you within the module, have a look at the data model provided below. 

.. code-block:: python

    def tag_spec():
        """Return the tag object spec."""
        return dict(
            color=dict(
                type="str",
                required=False,
                default=False,
            ),
            comments=dict(
                type="str",
                required=False,
                default=False,
            ),
            folder=dict(
                required=True,
                choices=[
                    "GlobalProtect",
                    "Mobile Users",
                    "Remote Networks",
                    "Service Connections",
                    "Shared",
                ],
                type="str",
            ),
            name=dict(
                required=True,
                type="str",
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
            state=dict(
                required=True,
                choices=["absent", "present"],
                type="str",
            ),
        )
