import os

import requests
from dotenv import load_dotenv

from src.error.forbidden import ForbiddenErr
from src.error.not_found import NotFoundErr
from src.error.permission import PermissionErr

load_dotenv()


def fetch_pr_diff(owner: str, repo: str, pr_number: int) -> str:
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN is not set in the environment variables.")

    headers = {
        "Accept": "application/vnd.github.diff",
        "Authorization": f"Bearer {github_token}",
    }

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.HTTPError as e:
        status = e.response.status_code
        if status == 404:
            raise NotFoundErr("Pull request not found") from e
        if status == 403:
            raise ForbiddenErr(
                "Access forbidden. Check your GitHub token and permissions."
            ) from e
        if status == 401:
            raise PermissionErr("Unauthorized access. Check your GitHub token.") from e
        raise
    except requests.RequestException as e:
        raise requests.RequestException(
            "An error occurred while fetching the pull request diff."
        ) from e

    return response.text
