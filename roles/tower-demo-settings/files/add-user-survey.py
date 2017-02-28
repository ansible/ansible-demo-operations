#!/usr/bin/env python

from __future__ import print_function
import os
import requests
from requests.utils import quote
import json
import sys

try:
    import tower_cli
    import tower_cli.utils.exceptions as exc
    from tower_cli.utils import parser
    from tower_cli.conf import settings

    HAS_TOWER_CLI = True
except ImportError:
    HAS_TOWER_CLI = False


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def exit_failure(msg):
    eprint(msg)
    sys.exit(1)


def tower_config():
    config_file = '~/.tower_cli.cfg'
    config_file = os.path.expanduser(config_file)
    if not os.path.exists(config_file):
        module.fail_json(msg='file not found: %s' % config_file)

    with open(config_file, 'rb') as f:
        return parser.string_to_dict(f.read())


def find_job_template(tower_config, job_template_name):
    url = 'https://{0}/api/v1/job_templates/?search={1}'.format(
        tower_config['host'],
        quote(job_template_name))

    headers = {'Content-type': 'application/json'}

    response = requests.get(
        url,
        verify=False,
        auth=(tower_config['username'], tower_config['password']),
        headers=headers)

    if response.status_code != 200:
        exit_failure('job template not found: %s' % job_template_name)

    return response.json()['results'][0]['id']


def create_survey_spec(tower_config, job_template_id, name, description, spec):
    url = 'https://{0}/api/v1/job_templates/{1}/survey_spec/'.format(
        tower_config['host'],
        job_template_id)

    headers = {'Content-type': 'application/json'}

    response = requests.post(
        url,
        verify=False,
        auth=(tower_config['username'], tower_config['password']),
        headers=headers,
        data=json.dumps({
            'name': name,
            'description': description,
            'spec': spec}))

    if response.status_code != 200:
        exit_failure('error creating job template survey')

    return response

def enable_survey(tower_config, job_template_id):
    url = 'https://{0}/api/v1/job_templates/{1}/'.format(
        tower_config['host'],
        job_template_id)

    headers = {'Content-type': 'application/json'}

    response = requests.patch(
        url,
        verify=False,
        auth=(tower_config['username'], tower_config['password']),
        headers=headers,
        data=json.dumps({
            'survey_enabled': True}))

    if response.status_code != 200:
        exit_failure('error enabling job template survey')


def main():
    common_spec = [
        {
            "type": "text",
            "question_name": "First Name",
            "question_description": "First name of the user?",
            "variable": "first_name",
            "required": True
        },
        {
            "type": "text",
            "question_name": "Last Name",
            "question_description": "Last name of the user?",
            "variable": "last_name",
            "required": True
        },
        {
            "type": "text",
            "question_name": "Username",
            "question_description": "What username should be created in Tower?",
            "variable": "username",
            "required": True
        },
        {
            "type": "text",
            "question_name": "Email",
            "question_description": "What's the user's email address?",
            "variable": "email",
            "required": True
        }
    ]

    admin_survey = {
        "name": "Add Demo Admin",
        "description": "Onboard a user that should be a demo admin."
    }

    user_survey = {
        "name": "Add Demo User",
        "description": "Onboard a user that should be a demo user."
    }

    if not HAS_TOWER_CLI:
        exit_failure('tower-cli not installed on remote host')
    else:
        tower_auth = tower_config()
        for survey in [admin_survey, user_survey]:
            job_template_id = find_job_template(
                tower_auth,
                survey['name'])

            create_survey_spec(
                tower_auth,
                job_template_id,
                survey['name'],
                survey['description'],
                common_spec)

            enable_survey(tower_auth, job_template_id)

main()
