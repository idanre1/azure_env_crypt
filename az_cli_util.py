import os
import re
import shlex
import sys

from azure.cli.core import get_default_cli
from azure.cli.core.azclierror import AuthenticationError
from knack.util import CLIError


def az_cli(args_str, verbose=True, debug=False):
    """Invoke an embedded Azure CLI command, returning its result or raising its error."""
    args = [arg.replace('#', ' ') for arg in shlex.split(args_str)]
    args.extend(['-o', 'none'])
    if debug:
        print(args)

    cli = get_default_cli()
    exit_code = cli.invoke(args)
    if cli.result.error is not None:
        if verbose:
            print(cli.result.error, file=sys.stderr)
        raise cli.result.error
    if exit_code != 0:
        raise RuntimeError(f'Azure CLI failed with exit code {exit_code}')
    return cli.result.result


def _login_required(error):
    if isinstance(error, AuthenticationError):
        if error.msal_error:
            # Retry only interactive/expired-token errors, not invalid credentials or policy denials.
            kind = error.msal_error.get('error')
            codes = set(error.msal_error.get('error_codes') or [])
            return (
                kind in {'interaction_required', 'invalid_grant'}
                and (
                    (not codes and kind == 'interaction_required')
                    or (bool(codes) and codes <= {50058, 50076, 50079, 50173, 70043, 700082, 700084})
                )
            )
        return str(error) == "Can't find token from MSAL cache."
    return (
        str(error) == "Please run 'az login' to setup account."
        or re.fullmatch(r"User '.+' does not exist in MSAL token cache\. Run `az login`\.", str(error))
        is not None
    )


def az_login():
    """Reuse usable cached authentication, otherwise start interactive device-code login."""
    probe = 'account get-access-token --resource-type arm --query expires_on'
    try:
        az_cli(probe, verbose=False)
    except CLIError as error:
        if not _login_required(error):
            raise
    else:
        print('az already logged_in')
        return

    print('az is not logged in, please complete device-code login')
    # Preserve the old login UX without changing the user's persistent CLI configuration.
    setting = 'AZURE_CORE_LOGIN_EXPERIENCE_V2'
    previous = os.environ.get(setting)
    os.environ[setting] = 'off'
    try:
        az_cli('login --use-device-code')
    finally:
        if previous is None:
            os.environ.pop(setting, None)
        else:
            os.environ[setting] = previous
    az_cli(probe, verbose=False)
