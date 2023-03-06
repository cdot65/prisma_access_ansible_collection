# Ansible Collection - cdot65.prisma_access

- [Ansible Collection - cdot65.prisma\_access](#ansible-collection---cdot65prisma_access)
  - [Overview](#overview)
  - [Compatibility 📋](#compatibility-)
    - [Prisma Access version](#prisma-access-version)
    - [Ansible version compatibility](#ansible-version-compatibility)
  - [Current supported modules ⚙️](#current-supported-modules-️)
  - [Executing the playbook 🚀](#executing-the-playbook-)
  - [More examples](#more-examples)

## Overview

The goal of this collection is to provide an easier way to interact with
Palo Alto Networks's Prisma Access solution.

While nothing will stop you from using the built-in `uri` module against
Prisma's REST API, you may find that working with pre-packaged modules can
simplify the development of your playbook, or it may just be easier to support
as a team.

## Compatibility 📋

### Prisma Access version

Prisma Access is maintained by Palo Alto Networks, preventing you from
having to concern yourself with the underlying infrastructure. This prevents
you from worrying about version compatibility.

### Ansible version compatibility

Ansible is going through some rapid changes and while those changes get worked
out we will continue to test for Ansible 2.10.x.

It is unlikely that something will break on later Ansible versions,
but it is something to keep in mind.

## Current supported modules ⚙️

Here is a short list of modules included within the collection, expect feature
parity with the API spec before this project hits version 1.0.0

| Name                                    | Description                          |
| --------------------------------------- | ------------------------------------ |
| cdot65.prisma_access.address            | Manage addresses                     |
| cdot65.prisma_access.address_group      | Manage address groups                |
| cdot65.prisma_access.ike_gateway        | Manage IPsec IKE Gateways            |
| cdot65.prisma_access.ipsec_tunnel       | Manage IPsec Tunnels                 |
| cdot65.prisma_access.push_config        | Push candidate configuration changes |
| cdot65.prisma_access.remote_network     | Manage Remote Networks               |
| cdot65.prisma_access.service_connection | Manage Service Connections           |
| cdot65.prisma_access.tag                | Manage tags                          |

## Executing the playbook 🚀

After installing the collections, you can call the modules by using their full name path.

tag.yaml

```yaml
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
```

Then simply run your playbook

```bash
ansible-playbook tag.yaml
```

## More examples

Examples for each module can be found within the [tests](https://github.com/cdot65/prisma_access_ansible_collection/tree/main/cdot65/prisma_access/tests) directory.
