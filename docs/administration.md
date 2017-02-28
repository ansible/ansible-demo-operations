# Tower Demo Administration

The [administration playbooks](../roles/tower-demo-settings/files/ansible-demo-admin) are used to automate the workflows associated with managing access to shared demos. Below is information on how to use them.

### [`add-demo-user.yml`](../roles/tower-demo-settings/files/ansible-demo-admin/add-demo-user.yml)
This playbook will onboard a new demo user. This is the most commonly used playbook for Tower demo management. See the playbook for visibility on what operations are performed.

### [`add-demo-admin.yml`](../roles/tower-demo-settings/files/ansible-demo-admin/add-demo-admin.yml)
This playbook will onboard a new demo admin. It should only be used when somebody really needs the ability to give new users the ability to run demos. See the playbook for visibility on what operations are performed.
