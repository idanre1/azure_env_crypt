# aes-env-crypt

Keep a small JSON dict of secrets (API keys, SAS tokens) in an AES-256 encrypted
file, and decrypt it only when a script needs it: as a Python dict, as Bash
`export` lines, or as a plain JSON file. Encryption uses
[pyAesCrypt](https://pypi.org/project/pyAesCrypt/), its only dependency.

```bash
pip install aes-env-crypt        # or: uv add aes-env-crypt
```

## Python

```python
from aes_env_crypt import aesCryptJson

aesCryptJson('service.aes', password).encrypt({'API_TOKEN': '...'})
secrets = aesCryptJson('service.aes', password).decrypt()   # -> dict
```

A wrong password or a corrupt file raises `ValueError`.

## Command line

| Command | Does |
|---|---|
| `args-to-aes-file -f NAME -p PASSWORD -d VAR=value ...` | writes `NAME.aes` |
| `env-from-aes-file -f NAME.aes -p PASSWORD` | prints `export VAR="value"` lines (names upper-cased) |
| `json-from-aes-file -f NAME.aes -p PASSWORD` | writes plain-text `NAME.json` next to the file |

Load secrets into the current Bash shell without echoing the password:

```bash
read -rsp 'Password: ' pw; echo
eval "$(env-from-aes-file -f service.aes -p "$pw")"; unset pw
```

## Security notes

- `-p` puts the password on the command line, where other local users can see it
  in the process list while the command runs. Prefer the Python API on shared hosts.
- Keep `.aes` files out of git. An encrypted file in a repository can be attacked
  offline forever, so its safety then rests only on the password strength.
- `json-from-aes-file` writes the secrets unencrypted; delete the `.json` after use.

## Development

```bash
uv run --isolated --no-project --with-editable . python -m unittest discover -s tests -v
uv build && uvx twine check dist/*
```

`CI` (`.github/workflows/ci.yml`) runs the tests on Python 3.10 to 3.14 for every
push to `main` and every pull request.

### Releasing

`Publish to PyPI` (`.github/workflows/publish.yml`) runs when a `v*` tag is pushed.
It checks that the tag matches the `pyproject.toml` version, runs the tests, builds,
and uploads to PyPI with
[Trusted Publishing](https://docs.pypi.org/trusted-publishers/), so no PyPI token is
stored in GitHub.

```bash
uv version --bump patch        # or set the version in pyproject.toml
git commit -am "Release vX.Y.Z" && git tag vX.Y.Z && git push origin main vX.Y.Z
```

One-time setup before the first release:

1. On pypi.org, go to Account settings → Publishing → Add a new pending publisher,
   and enter: PyPI project `aes-env-crypt`, owner `idanre1`, repository
   `aes_env_crypt`, workflow `publish.yml`, environment `pypi`.
2. On GitHub, go to repository Settings → Environments → New environment and create
   `pypi`. Optionally add yourself as a required reviewer, so each upload waits
   for your approval.

Formerly `azure_env_crypt`; its Azure CLI helpers moved out, so the package no
longer depends on Azure.

## License

GPL-3.0-only. See [LICENSE](https://github.com/idanre1/aes_env_crypt/blob/main/LICENSE).
