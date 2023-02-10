===================================
cdot65.prisma_access.address_groups
===================================

----------------------------
Manage address group objects
----------------------------

address_groups
==============

This module will allow you to manage your address group objects within Prisma Access.

Feature set as of version 0.1.1:
  - manage address objects
  - idempotent

Under construction

Example
-------

Here is a basic example of using the module to mange your address objects in Prisma Access.

.. code-block:: yaml

    ---
    # CONFIGURE ADDRESS GROUP OBJECTS
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
            name: "ansible-test"
            color: "Salmon"
            comments: "This tag is used by Ansible"
            folder: "Service Connections"
            state: "present"

        - name: Create ip-netmask address objects
          cdot65.prisma_access.addresses:
            provider:
              client_id: "{{ client_id }}"
              client_secret: "{{ client_secret }}"
              scope: "{{ scope }}"
            description: "This is a test object"
            folder: "Service Connections"
            ip_netmask: "192.168.77.0/24"
            name: "AnsibleTestAddress"
            state: "present"
            tag: "ansible-test"

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


Data Model
----------

If you'd like to see the options available for you within the module, have a look at the data model provided below. 

.. code-block:: python

    def address_groups_spec():
        """Return the address groups object spec."""
        return dict(
            description=dict(
                max_length=1023,
                required=True,
                type="str",
            ),
            dynamic=dict(
                required=False,
                type="dict",
                options=dict(
                    filter=dict(
                        required=True,
                        type="str",
                    ),
                ),
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
                max_length=63,
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
            static=dict(
                elements="str",
                max_items=64,
                required=False,
                type="list",
            ),
            tag=dict(
                elements="str",
                max_items=64,
                required=False,
                type="list",
            ),
        )
