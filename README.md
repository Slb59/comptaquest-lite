# SecretBox : My personnal secret manager

## Project Overview
<img src="static/images/logo_sb.png" alt="logo" width="100" height="100"/>

Secret box will allow me to manage my entire organisation. She will offer me the list of things to do as I manage it today in Excel. It will allow me to activate the pomodoro functionality for each task. There will also be links to other applications under development: comptaquest, potionrun, dictavoix and other ideas for 2026.

### Key features
- user management ( connection, change password, authenticator…)
- tasks management
- pomodoro function
- navigation for others applications

### Users
- administrator : manage all users and autorizations
- accountant : for comptaquest parameters and management
- member : all others members

### Technical stack

<div align="center">

| Database | Front End  |  Back End    | Quality                |
|-----------------|-------|-------|-------------------------|
| Sqlilte3 | Tailwind CSS | Python | Pytest, pytest-cov, pytest-html  |
|               | Wagtail | Django | Black, Isort, Flake8 |

</div>

## Getting Started

### Installation instructions
Clone the github project and activate the virtual environment.

```
git clone https://github.com/Slb59/comptaquest-lite
uv .venv
uv init
source .venv/bin/activate
```

### Prerequisites
Required tools, versions, or system requirements.

### Configuration

- Create env file .env

```
DEBUG=<<True or False>>
ALLOWED_HOSTS=<<host>>
DJANGO_SECRET_KEY=<<django key>>
DJANGO_SETTINGS_MODULE=<<config.settings.dev | config.settings.prod>>

DATABASE_URL=<<sqlite:///db.sqlite3 | postgresql://user:password@host:port/dbname>>

NPM_BIN_PATH=<<npm path>>

DEFAULT_FROM_EMAIL= <<admin email>>
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=<<superuser email>>
EMAIL_HOST_PASSWORD=<<superuser password>>
ADMIN_EMAIL=<<admin email>>

DEPLOY_PATH=<<path to deploy>>
```


## Usage

    How to run the project: 
    In frontend terminal: npm run build
    In backend terminal: make run
    Launch the project: http://127.0.0.1:8000/

## Contributing

### New release process
    Guidelines: How others can contribute (coding standards, pull request process).
    Code of conduct: use the following command: make quality for the quality checks and updates.

    - creating a branch for a new feature
```bash
    git checkout -b feature/feature_name origin/main
```
    - commit the changes
```bash
git add .
git commit -m "Detailed description of changes"
git push
```

    - check github action

    - Updating from main branch
```bash
git fetch origin
git rebase origin/main
```
    

### Version change

#### Prerequisites
    - Have access rights to the repository
    - Have Python and pip installed
    - Being on the `main` branch
    - Check that all current pull requests are merged
    - Check that the tests pass

#### Stages

##### 1. Preparation
```bash
# Create a new branch for the release
git checkout -b release/vX.Y.Z main
```

##### 2. Update the version
```bash
# Update the version in VERSION file
echo "X.Y.Z" > VERSION

# Check the version
python manage.py show_version
```

##### 3. Update the changelog file
```markdown
# CHANGELOG.md
## [X.Y.Z] - YYYY-MM-DD
### Modification type (new feature, bug fix, improvement)
- detailed description of the change
```

##### 4. Create the release commit
```bash
# Commit changes
git add VERSION CHANGELOG.md
git commit -m "Release vX.Y.Z"

# Push and create the pull request
git push origin release/vX.Y.Z
```

#### Versions types
- **MAJOR**: Major changes or compatibility break
- **MINOR**: New compatible features
- **CORRECTION**: Bug fixes and minor improvements

#### Checklist
Before merging the pull request, make sure to:
- Check that all tests pass
- Confirm that the documentation is up to date
- Validate that the changelog is complete

## Testing

All tests are located in the tests folder. To run the tests, use the following command: make tests.
You can run the tests with coverage using the following command: make tests-coverage.
You can run the tests of a specific module using the following command: make tests-module.

## Deployment
    make deploy
    Deployment instructions: How to deploy the project to production or another environment.

## Project Status and Roadmap

    Current status: in development V0.0.2
    Planned features: see the roadmap in the github project.

## Credits / Authors

    Acknowledgements: Credits for resources, libraries, or contributors.
    Maintainers: Osynia (osynia.devapps@gmail.com)

## License

    License information: What license does the project use? (MIT, GPL, etc.)

