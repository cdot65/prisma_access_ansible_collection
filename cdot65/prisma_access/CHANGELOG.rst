==================================
cdot65.prisma_access Release Notes
==================================

.. contents:: Topics


v0.1.4
======

Release Summary
---------------

Create module_util file to handle authentication, all modules refactored to take advantage.

Renamed modules to be more consistent with other collections.


New Modules
-----------

- cdot65.prisma_access.address - Renamed module, was previously `addresses`.
- cdot65.prisma_access.address_group - Renamed module, was previously `address_group`.

v0.1.3
======

Release Summary
---------------

Adds support for IKE Gateway objects.


New Modules
-----------

- cdot65.prisma_access.ike_gateway - Creates or removes IKE Gateway objects within Prisma Access.

v0.1.2
======

Release Summary
---------------

Adds support for address group objects.


New Modules
-----------

- cdot65.prisma_access.address_group - Creates or removes address group objects within Prisma Access.

v0.1.1
======

Release Summary
---------------

This corrects authentication and adds support for address objects.


New Modules
-----------

- cdot65.prisma_access.addresses - Creates or removes address objects within Prisma Access.

v0.1.0
======

Release Summary
---------------

This is the first official release of an Ansible Collection for Prisma Access.


New Modules
-----------

- cdot65.prisma_access.tag - Creates or removes tags within Prisma Access.
