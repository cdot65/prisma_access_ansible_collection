==============================
cdot65.prisma_access.addresses
==============================

----------------------
Manage address objects
----------------------

addresses
=========

This module will allow you to manage your address objects within Prisma Access.

Feature set as of version 0.1.1:
  - manage address objects
  - idempotent

Under construction

Example
-------

Here is a basic example of using the module to mange your address objects in Prisma Access.

.. code-block:: yaml

    ---
    # CONFIGURE ADDRESS OBJECTS
    - hosts: prisma
      connection: local
      gather_facts: False
      become: False
      collections:
        - cdot65.prisma_access

      tasks:
        - name: Create ip-netmask address objects
          cdot65.prisma_access.addresses:
            provider:
              client_id: "{{ client_id }}"
              client_secret: "{{ client_secret }}"
              scope: "{{ scope }}"
            description: "This is an IP-Netmask address object"
            folder: "Service Connections"
            ip_netmask: "1.1.1.1/32"
            name: "Ansible-Test-1"
            state: "present"
            tag: "Automation"
        
        - name: Create ip-range address objects
          cdot65.prisma_access.addresses:
            provider:
              client_id: "{{ client_id }}"
              client_secret: "{{ client_secret }}"
              scope: "{{ scope }}"
            description: "This is an IP-Range address object"
            folder: "Service Connections"
            ip_range: "192.168.1.10-192.168.1.99"
            name: "Ansible-Test-2"
            state: "present"
            tag: "Automation"

        - name: Create fqdn address objects
          cdot65.prisma_access.addresses:
            provider:
              client_id: "{{ client_id }}"
              client_secret: "{{ client_secret }}"
              scope: "{{ scope }}"
            description: "This is an FQDN address object"
            folder: "Shared"
            fqdn: "this.is.an.fqdn"
            name: "Ansible-Test-3"
            state: "present"
            tag: "Automation"
        
        - name: Create wildcard address objects
          cdot65.prisma_access.addresses:
            provider:
              client_id: "{{ client_id }}"
              client_secret: "{{ client_secret }}"
              scope: "{{ scope }}"
            description: "This is a wildcard address object"
            folder: "Shared"
            ip_wildcard: "10.20.1.0/0.0.248.255"
            name: "Ansible-Test-4"
            state: "present"


Data Model
----------

If you'd like to see the options available for you within the module, have a look at the data model provided below. 

.. code-block:: python

    def addresses_spec():
        """Return the address object spec."""
        return dict(
            description=dict(
                max_length=1023,
                required=True,
                type="str",
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
            fqdn=dict(
                required=False,
                type="str",
            ),
            ip_netmask=dict(
                required=False,
                type="str",
            ),
            ip_range=dict(
                required=False,
                type="str",
            ),
            ip_wildcard=dict(
                required=False,
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
            tag=dict(
                elements="str",
                max_items=64,
                required=False,
                type="list",
            ),
        )

