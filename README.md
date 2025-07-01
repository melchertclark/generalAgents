# generalAgents

This repository serves as a **general activities folder** for various projects, experiments, and exploratory work. It is intended as a flexible workspace where you can organize and track a variety of tasks without tying the repository to a single domain or project.

## Workspace Structure

To maintain clarity and maintainability, please adhere to the following guidelines:

```
.
├── <activity-folder-1>/
│   └── ...
├── <activity-folder-2>/
│   └── ...
└── README.md
```

- Place each distinct activity in its own subfolder at the root of the repository.
- Avoid cluttering the root with unrelated files.
- Choose clear, descriptive names for your folders.

## Documentation Guidelines

- Every activity folder should include its own `README.md` (or equivalent) describing:
  - Purpose and scope of the activity
  - Setup and installation instructions
  - Usage examples or execution steps
  - Dependencies and environment requirements
- Keep documentation up-to-date as the activity evolves.

## Environment Setup

This repository uses environment variables for sensitive configuration like API keys. To set up your environment:

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your actual API keys:
   ```
   LIMITLESS_API_KEY=your_actual_api_key_here
   ```

3. The `.env` file is already in `.gitignore` to prevent accidentally committing sensitive data.

## Clean Workspace Practices

- Commit only relevant files to version control.
- Use a `.gitignore` file to exclude temporary, build, or system-specific files.
- Regularly review and remove stale or unused artifacts.
- **Never commit API keys or sensitive credentials to version control.**

By following these guidelines, we ensure a clean, organized, and well-documented general activities repository that remains easy to navigate and maintain over time.