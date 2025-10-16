Quick complete example (setuptools/pyproject + build + twine):
- Bump version and tag:
  # edit version in package
  git add .
  git commit -m "Bump version to 1.2.3"
  git tag v1.2.3
  git push && git push --tags

- Build:
  pip install build twine
  python -m build

- Test upload:
  twine upload --repository testpypi dist/*

- Final upload:
  export PYPI_TOKEN="pypi-...."
  twine upload -u __token__ -p "$PYPI_TOKEN" dist/*

Poetry minimal flow:
- poetry version patch
- poetry build
- poetry publish -u __token__ -p $PYPI_TOKEN

update the package version (where you keep it), build a new sdist/wheel from pyproject, then upload to PyPI (preferably test first). Below are the common, step-by-step options and commands.

1) Decide where the canonical version lives
- pyproject-managed backends vary:
  - Poetry: version is in pyproject.toml under . Use poetry commands to bump.
  - Flit: version in pyproject.toml.
  - Setuptools/PEP 621: you may have version in pyproject.toml  or use a dynamic approach (package __init__.py, setuptools_scm, etc.).
Make sure you know how your project supplies the version so you update the right place.

2) Update the version
- Poetry:
  - poetry version 1.2.3
  (This updates pyproject.toml and the lockfile.)
- Manual (pyproject / package __init__):
  - Edit pyproject.toml (or package/__init__.py) and change version = "1.2.3".
- Automatic tools:
  - bump2version or setuptools_scm – use their workflows.

3) Commit and tag
- git add -A
- git commit -m "Bump version to 1.2.3"
- git tag v1.2.3
- git push && git push --tags

Tagging is optional for PyPI itself but recommended for releases.

4) Build distributions
Install the modern build tool if you don’
Flit alternative:
- flit build

5) Test upload to TestPyPI (recommended)
Create a TestPyPI account and API token (or use username/password).
- python -m pip install --upgrade twine
- twine upload --repository testpypi dist/*
or explicitly:
- twine upload --repository-url https://test.pypi.org/legacy/ dist/*

To install from TestPyPI for verification:
- pip install --index-url https://test.pypi.org/simple/ --no-deps your-package==1.2.3

6) Upload to PyPI
Get an API token from https://pypi.org/manage/account/#api-tokens and use it (recommended).
- Export credentials (recommended for tokens):
  - export TWINE_USERNAME="__token__"
  - export TWINE_PASSWORD="pypi-xxxxx..."
Then:
- twine upload dist/*

You can also use ~/.pypirc to store credentials:
~/.pypirc example:

index-servers =
    pypi
    testpypi


  username = __token__
  password = pypi-<token>


  repository: https://test.pypi.org/legacy/
  username = __token__
  password = pypi-<token>

7) (Optional) GPG-sign your distributions
- twine upload --sign dist/*

8) Verify
- pip install your-package==1.2.3
Or check https://pypi.org/project/your-package/1.2.3

Common variations and tips
- Poetry publish: poetry publish --build --username __token__ --password <token> (or configure via poetry config pypi-token.pypi <token>)
- If using setuptools_scm you don’t manually edit a version—tag your git commit and setuptools_scm will derive the version.
- If build fails, check pyproject.toml for correct  requires and build-backend.
- CI: automate build + twine upload in CI (use encrypted token / secret) on push/tag.

Minimal command sequence (setuptools/PEP 621 or build-based):
- Edit version
- git commit && git tag vX.Y.Z && git push --tags
- python -m build
- TWINE_USERNAME="__token__" TWINE_PASSWORD="pypi-..." twine upload dist/*
