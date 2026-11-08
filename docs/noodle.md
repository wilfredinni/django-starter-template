# API Collection (Noodle)

The project ships with a [Noodle](https://noodlerest.dev) collection that covers every `v1` endpoint: login, logout, user creation, and profile management. Noodle is a terminal-based REST client — your requests live as YAML files in the repo, versioned next to the code they exercise.

The collection lives in `api-collection/`:

```
api-collection/
├── settings.yml
├── .environments/
│   ├── local.env              # local API and credential declarations
│   └── ci.env                 # disposable CI API and credential declarations
├── auth/
│   ├── create-user.yml
│   ├── login.yml
│   ├── logout.yml
│   └── logout-all.yml
├── core/
│   └── ping.yml
└── profile/
    ├── get-profile.yml
    ├── patch-profile.yml
    └── update-profile.yml
```

## Installation

macOS (Homebrew):

```bash
brew tap wilfredinni/noodle
brew trust wilfredinni/noodle
brew install noodle
```

Linux/macOS (install script):

```bash
curl -LsSf https://noodlerest.dev/install.sh | sh
```

Verify the installation:

```bash
noodle --version
```

## Usage

Start the stack and create your administrator — the local collection points at `http://localhost:8000`:

```bash
make up
# In another terminal, once the API is ready:
make superuser
```

`make seed` creates sample users with random passwords; it does not create an administrator with predefined credentials. Configure your administrator's credentials as described below before running authentication checks.

Open the collection interactively:

```bash
noodle -c api-collection
```

Or run all eight saved requests from the command line in three runs:

```bash
noodle collection run api-collection auth/create-user core/ profile/ --env local --fail-fast
noodle collection run api-collection auth/logout --env local --fail-fast
noodle collection run api-collection auth/logout-all --env local --fail-fast
```

Each run starts with the saved `auth/login` setup hook and captures a fresh token. Run the logout endpoints separately: they revoke tokens and would break later requests in an unfiltered collection run.

These checks create a user and update the administrator's profile. Use a disposable development database and choose an unused `new_user_email` each time you repeat the user-creation checks.

## Authentication

Protected endpoints use Knox tokens (`Bearer`); login and ping accept unauthenticated requests. For local use:

1. Create an administrator with `make superuser` and set its email in `api-collection/.environments/local.env`.
2. Set `new_user_email` to a different, unused email for the account created by `auth/create-user`.
3. Save your administrator's password as both `password` and `password2` using the prompts:

```bash
noodle secret set password --env local --collection api-collection
noodle secret set password2 --env local --collection api-collection
```

The collection shares these password variables between login, user creation, and profile updates. The two values must match. Local secret storage requires a working OS keyring; CI supplies passwords through process environment variables instead.

`auth/login` captures `body.token` as the lowercase variable `token` with `persist: secret`. Collection runs keep that capture in memory for subsequent requests and do not write it to the keyring. Sending login individually saves the token securely for later manual requests; no copying is needed.

`request run` and manual sends do not execute collection setup hooks. Send login first when using individual requests:

```bash
noodle request run auth/login --collection api-collection --env local
noodle request run profile/get-profile --collection api-collection --env local
```

## Environment Variables

Requests reference variables from `api-collection/.environments/local.env`:

| Variable | Local default | Used for |
| --- | --- | --- |
| `base_url` | `http://localhost:8000` | Prefix of every request URL |
| `email` | *(set your administrator's email)* | Login and profile bodies/assertions |
| `new_user_email` | *(set an unused email)* | User creation |
| `password` | *(secret; set before running)* | Login, user creation, and profile updates |
| `password2` | *(secret; match `password`)* | User creation confirmation |
| `first_name` | `Admin` | Profile update bodies/assertions |
| `last_name` | `User` | Profile update bodies/assertions |
| `token` | *(secret; captured by login)* | Bearer token for authenticated requests |

Edit `local.env` freely or add new files in `.environments/` (e.g., `staging.env`) to switch environments from the Noodle UI.

## GitHub Actions

The [Test workflow](https://github.com/wilfredinni/django-starter-template/blob/main/.github/workflows/test.yml) runs a **Noodle API collections** job alongside the Python tests on pushes and pull requests to `main`. It installs Noodle v0.10.4 with the pinned [setup-noodle action](https://github.com/wilfredinni/setup-noodle):

```yaml
- uses: wilfredinni/setup-noodle@a964e8bf15b3e18ac4ed85480d01c2d3b6744a39 # v1.0.0
  with:
    version: v0.10.4
```

The job starts the API, Postgres, and Redis with Docker Compose, waits for health checks, and creates a disposable administrator. The backend runs migrations during startup. `ci.env` selects the API at `http://127.0.0.1:8000` and the CI account emails; the workflow supplies the declared `password` and `password2` secrets from `DJANGO_SUPERUSER_PASSWORD` through process environment variables.

**Do not declare `token` in `ci.env`.** Noodle resolves declared secrets before sending requests. An empty token secret would trigger a lookup in the unavailable Linux keyring, failing before login. The setup hook captures the token in memory instead.

With that disposable stack and its credentials ready, the workflow runs:

```bash
noodle collection run api-collection auth/create-user core/ profile/ \
  --env ci --fail-fast --reporter junit --output noodle-api.xml
noodle collection run api-collection auth/logout \
  --env ci --fail-fast --reporter junit --output noodle-logout.xml
noodle collection run api-collection auth/logout-all \
  --env ci --fail-fast --reporter junit --output noodle-logout-all.xml
```

HTTP failures, failed captures, or failed response assertions make the check fail. Each command writes a JUnit report, and the workflow uploads available `noodle-*.xml` files as the **noodle-api-results** artifact even when a check fails. Find it on the workflow run's summary page. Later commands are skipped if an earlier command fails.

Noodle refuses to overwrite reports. Choose new output filenames when repeating these commands outside a fresh CI checkout. The job prints Docker logs on failure and removes its containers and database volume after the run.
