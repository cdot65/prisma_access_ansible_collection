# Ansible Collection needs three new modules

## Ansible Modules to create

1. Create IKE Gateway:

   ```bash
   "{{baseUrl}}/sse/config/v1/ike-gateways?folder=Service Connections"
   ```

2. Create IPsec VPN:
   
   ```bash
   "{{baseUrl}}/sse/config/v1/ipsec-tunnels?folder=Service Connections"
   ```

3. Create a Service Connection

    ```bash
    "{{baseUrl}}/sse/config/v1/service-connections?folder=Service Connections"
    ```
