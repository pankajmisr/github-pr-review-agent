# GitHub PR Review Agent

An AI-powered GitHub Pull Request reviewer built with Google's Agent Development Kit (ADK).

## Overview

This agent helps developers by reviewing GitHub pull requests, providing feedback on code quality, identifying potential issues, and suggesting improvements. It leverages Google's Gemini models through ADK to analyze code changes and generate constructive reviews.

## Features

- Analyzes code changes in pull requests
- Identifies potential bugs, security issues, and performance problems
- Suggests improvements for code quality and readability
- Provides constructive feedback with explanations
- Submits reviews directly to GitHub pull requests

## Prerequisites

- Python 3.9 or higher
- GitHub personal access token with appropriate permissions
- Google API key for ADK/Gemini

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/github-pr-review-agent.git
   cd github-pr-review-agent
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Add your GitHub token and Google API key to the `.env` file

## Usage

Run the agent on a specific pull request:

```
python agent.py --owner <repository-owner> --repo <repository-name> --pr <pull-request-number>
```

Example:
```
python agent.py --owner google --repo adk-samples --pr 42
```

## How It Works

1. The agent fetches PR details and files changed from GitHub
2. It analyzes the code changes to identify issues and opportunities for improvement
3. It generates a detailed review with categorized feedback
4. The review is submitted to GitHub as comments on the PR

## Configuration

You can customize the agent's behavior by modifying:
- The model used (in `.env` file)
- The agent instructions (in `agent.py`)
- The code analysis criteria (in `agent.py`)

## Limitations

- The agent works best with PRs that have a reasonable number of files and changes
- Very large PRs may exceed context limits or take longer to process
- The agent doesn't have access to the full repository history or context

## License

This project is licensed under the MIT License - see the LICENSE file for details.