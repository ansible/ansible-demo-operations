# Ansible Tower Demo Operations
> Ansible Tower demo environment automation.

## Overview
This project contains Ansible resources for automating creation and management of a shared Ansible Tower demo environment. All demo content added to the Tower server is maintained by the Automation SME team as official demo content.

## Requirements
The following must be performed in order to use the playbooks in this project. Keep in mind that there are also various variables in [group_vars](group_vars) that can be modified, but that is not required.

#### Environment Variables
Rather than use [Ansible Vault](http://docs.ansible.com/ansible/playbooks_vault.html), this project looks up environment variables for almost all configuration that is deployment-specific. This is so that different deployments can use different passwords and other related config items.

###### AWS Account Access
These environment variables are used to automate creation of resources in the target AWS account.
- `ANSIBLE_AWS_ACCESS_KEY_ID`: AWS_ACCESS_KEY_ID for the target AWS account
- `ANSIBLE_AWS_SECRET_ACCESS_KEY`: AWS_SECRET_ACCESS_KEY for the target AWS account
- `ANSIBLE_AWS_REGION`: AWS_REGION for the target AWS account

###### AWS Demo Environment Configuration
These environment variables make it possible to reliably automate creation of AWS resources on potentially multiple accounts. Things like subnet mappings and AMIs will change across accounts.
- `ANSIBLE_AWS_PUBLIC_SUBNET_A_AZ`: The AZ to create the first public subnet in
- `ANSIBLE_AWS_PUBLIC_SUBNET_B_AZ`: The AZ to create the second public subnet in
- `ANSIBLE_AWS_PUBLIC_SUBNET_C_AZ`: The AZ to create the third public subnet in
- `ANSIBLE_ENVIRONMENT_NAME`: The name to prefix to all AWS resources created for this demo environment
- `ANSIBLE_DEMO_KEYPAIR_NAME`: The name of the keypair to use when creating the Tower EC2 instance
- `ANSIBLE_TOWER_ADMIN_PASSWORD`: The password to assign to the admin user
- `ANSIBLE_TOWER_AMI`: The AMI used when creating the Tower EC2 instance
- `ANSIBLE_TOWER_DB_PASSWORD`: The password to use when creating the Tower PostgreSQL DB
- `ANSIBLE_TOWER_LICENSE_PATH`: Path on the Ansible control host to the license file for this Tower deployment

One approach is to create an `env.sh` file and source it before running.

```
export ANSIBLE_AWS_ACCESS_KEY_ID="eggs"
export ANSIBLE_AWS_SECRET_ACCESS_KEY="spam"
export ANSIBLE_AWS_REGION="us-east-1"
export ANSIBLE_AWS_PUBLIC_SUBNET_A_AZ="us-east-1b"
export ANSIBLE_AWS_PUBLIC_SUBNET_B_AZ="us-east-1d"
export ANSIBLE_AWS_PUBLIC_SUBNET_C_AZ="us-east-1e"
export ANSIBLE_ENVIRONMENT_NAME="ansible-demo"
export ANSIBLE_DEMO_KEYPAIR_NAME="tower"
export ANSIBLE_TOWER_ADMIN_PASSWORD="coffee"
export ANSIBLE_TOWER_AMI="ami-2051294a"
export ANSIBLE_TOWER_DB_PASSWORD="donuts"
export ANSIBLE_TOWER_LICENSE_PATH="/path/to/ansible-demo-tower-license.json"
```

**Note**: your available AZs might be different than, literally, A, B, and C.

## Usage
1. Set up your demo environment
      ```
      ssh-agent bash
      ssh-add /path/to/tower-key.pem
      source env.sh
      ansible-playbook tower.yml
      ```
2. Create forms for any job templates that need them. This will be automated soon.

## Documentation
- [administration](docs/administration.md)
