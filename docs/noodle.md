# API Collection (Noodle)

The project ships with a [Noodle](https://noodlerest.dev) collection that covers every `v1` endpoint: login, logout, user creation, and profile management. Noodle is a terminal-based REST client — your requests live as YAML files in the repo, versioned next to the code they exercise.

The collection lives in `api-collection/`:

```
api-collection/
├── settings.yml
├── .environments/
│   └── local.env              # base_url and dev credentials
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

Start the stack first — the collection points at `http://localhost:8000` by default:

```bash
make up
```

Then open the collection interactively:

```bash
noodle -c api-collection
```

Or run requests from the command line:

```bash
# Run every request in the collection
noodle collection run api-collection

# Run a single request
noodle request run core/ping --collection api-collection
```

## Authentication

All endpoints except `ping` require a Knox token (`Bearer`). To authenticate:

1. Send the **login** request (`auth/login`) with your credentials — the seeded admin is `admin@admin.com` / `admin` (see [Database Seeding](database_seeding.md)).
2. Copy the `token` value from the response.
3. Store it as a secret so it is never written to the collection files:

```bash
noodle secret set TOKEN --env local --collection api-collection
```

Every authenticated request reads `$token` from that secret.

## Environment Variables

Requests reference variables from `api-collection/.environments/local.env`:

| Variable      | Default                 | Used for                        |
| ------------- | ----------------------- | ------------------------------- |
| `base_url`    | `http://localhost:8000` | Prefix of every request URL     |
| `email`       | `admin@admin.com`       | Login / create / profile bodies |
| `password`    | `admin`                 | Login / create / profile bodies |
| `password2`   | `admin`                 | User creation confirmation      |
| `first_name`  | `Admin`                 | Profile update bodies           |
| `last_name`   | `User`                  | Profile update bodies           |
| `TOKEN`       | *(secret)*              | Bearer token for auth           |

Edit `local.env` freely or add new files in `.environments/` (e.g., `staging.env`) to switch environments from the Noodle UI.
