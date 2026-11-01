# azure-env-crypt
Enhance AZ CLI to store service principal credentials in AES formats
1. Using service principal you can provide access to specific path inside a storage container
2. Using AES you can store the credentials encrypted and only upon run setup them to env variables for access the container
3. Since the credentails are stored in aes encrypted file, it can be versioned control on github (non-public repos...)

# Usage
### Storage SAS registration
For the current storage SAS registration script:

```bash
cd /datadrive/creds
uv run --project "$HOME/azure_scripts" ~/azure_scripts/storage/az_register_container.py -a ACCOUNT -n CONTAINER
```

The script prompts for the AES file password and writes
`storage--ACCOUNT--CONTAINER.aes` in the current working directory. It does not
create RBAC roles. `--project` selects the environment without changing that
directory; do not replace it with `--directory`.
### Setting up env variables from .aes file

```bash
cd /datadrive/creds
source ~/azure_scripts/env_from_aes_file.sh credentials.aes
```

Then you will be prompted for the password without echoing it.

# Setup

For the Azure scripts workspace, keep this checkout at
`~/python_lib/azure_env_crypt` and use its Python 3.13 uv environment:

```bash
uv sync --locked --project "$HOME/azure_scripts"
```

The workspace installs this package editably in `~/azure_scripts/.venv`, while
credential files stay in the directory from which you run the scripts.
Standalone installation into an
existing compatible Python environment is also supported:

```bash
python -m pip install -e ~/python_lib/azure_env_crypt
```

`requirements.txt` remains available for dependency-only installation, but does
not itself install this local package. Current Azure CLI requires modern Python;
the Azure scripts workspace uses and tests Python 3.13.

## Azure CLI helpers

`az_cli(command, verbose=True, debug=False)` invokes the embedded CLI, suppresses
normal command output, and returns its Python result, including empty results.
CLI failures raise the original exception; a nonzero exit without an exception
raises `RuntimeError`. Quoted arguments are parsed with `shlex`, and the existing
`#`-for-spaces argument convention is retained. Explicit debug output can include
command arguments; do not enable it for commands containing secrets.

`az_login()` first requests a management token using the cached CLI session,
without printing or returning the access token. When the user must sign in,
it starts device-code login and verifies authentication again afterward. Complete
the displayed browser instructions and MFA if required. This remains interactive,
and tenant policy can prohibit device-code login.

The helper temporarily disables the CLI's new subscription selector for its own
login, restoring the environment setting afterward and leaving saved CLI config
unchanged. Microsoft Graph permissions are no longer needed just to check login.
Permission, network, invalid credential, and configuration failures propagate
instead of being reported as successful authentication.

Tests for the shared library live in the consuming Azure scripts workspace:

```bash
uv run --project "$HOME/azure_scripts" python -m unittest discover -s "$HOME/azure_scripts/tests" -v
```
