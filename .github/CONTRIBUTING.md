# Contribution Guidelines

We would appreciate your contributions:

- [Feature requests and bug reports](https://github.com/makukha/questionary-cli/issues)
- [Security vulnerability reports](https://github.com/makukha/questionary-cli/blob/main/.github/SECURITY.md)
- Pull requests

## Pull requests

If the change proposed is not trivial, like typo in docs, please create an issue first.

### Prerequisites

You will need:

- [GNU make](https://www.gnu.org/software/make/make.html)
- [Git](https://git-scm.com)
- [GitHib CLI](https://cli.github.com)
- [Lefthook](https://lefthook.dev)
- [Podman](https://podman.io) or [Docker](https://www.docker.com)
- [uv](https://docs.astral.sh/uv/)
- [yq](https://mikefarah.gitbook.io/yq)

If your OS is macOS or Linux, some of them will be installed by `make init`.

### Initialize dev environment

- Fork project repository [makukha/questionary-cli](https://github.com/makukha/questionary-cli) under your account.
- Create feature branch in your fork.
- Clone and install Python packages:

    ```shell
    git clone https://github.com/<YOUR_USER_NAME>/questionary-cli.git
    make init
    make pre-commit
    ```

### Write code

It is convenient to start from adding tests reproducing the bug or shaping the new
feature. All added code must be covered with tests.

The code will be checked with [Ruff](https://github.com/astral-sh/ruff) and
[mypy](https://mypy.readthedocs.io). See `pyproject.toml` for details.

### Run lint and format checks

```shell
make lint
```

There must be no errors.

### Run tests

* Fast, the "main" configuration only:

    ```shell
    make test TOXARGS="-m main"
    ```

    Coverage report is generated as part of "main" configuration.
    Every new PR must not decrease the code coverage.

* The whole test matrix (may take some time):

    ```shell
    make test
    ```
* Debug single failing tox environment other than "main":

    ```shell
    make test TOXARGS="-e <tox-env-name>"
    ```

    See `tox.ini` for details.

### Build docs and python package

```shell
make build
```

There must be no errors.

### Add changelog entry

```shell
make news
```

Edit the new `*.md` file added under `NEWS.d/`: uncomment the appropriate
section and describe what was done in your pull request.

### Create pull request

The project maintainers will get back to review your PR.

Thank you for your valuable contribution!
