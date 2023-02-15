from ansible.module_utils._text import (
    to_native,
)
from traceback import format_exc
from ansible.module_utils.basic import AnsibleModule  # noqa: F401
from panapi import PanApiSession
import time


def get_authenticated_session(module):
    try:
        # create an authenticated session object
        auth = module.params.get("provider")
        session = PanApiSession()
        session.authenticate(
            client_id=auth["client_id"],
            client_secret=auth["client_secret"],
            scope=f'profile tsg_id:{auth["scope"]} email',
            token_url="https://auth.apps.paloaltonetworks.com/am/oauth2/access_token",
        )

        # jwt isn't a float, causing an error of the token not being valid yet
        time.sleep(1.1)

        return session

    except Exception as exception_error:
        module.fail_json(msg=to_native(exception_error), exception=format_exc())
