# github_tools.py

"""
GitHub API tool functions for the PR review agent.
"""

from github import Github
import os
from typing import Dict, List, Any, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_pr_details(repo_owner: str, repo_name: str, pr_number: int, github_token: str) -> Dict[str, Any]:
    """
    Gets the details of a specific pull request.
    
    Args:
        repo_owner (str): The owner of the repository
        repo_name (str): The name of the repository
        pr_number (int): The pull request number
        github_token (str): GitHub access token
        
    Returns:
        dict: Pull request details including title, description, files changed, etc.
    """
    try:
        # Initialize GitHub client
        g = Github(github_token)
        
        # Get repository and pull request
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        pr = repo.get_pull(pr_number)
        
        # Get PR details
        result = {
            "number": pr.number,
            "title": pr.title,
            "body": pr.body,
            "state": pr.state,
            "user": pr.user.login,
            "created_at": pr.created_at.isoformat(),
            "updated_at": pr.updated_at.isoformat(),
            "head_ref": pr.head.ref,
            "base_ref": pr.base.ref
        }
        
        return result
    except Exception as e:
        logger.error(f"Error getting PR details: {e}")
        return {"error": str(e)}

def get_pr_files(repo_owner: str, repo_name: str, pr_number: int, github_token: str) -> List[Dict[str, Any]]:
    """
    Gets all files changed in a pull request.
    
    Args:
        repo_owner (str): The owner of the repository
        repo_name (str): The name of the repository
        pr_number (int): The pull request number
        github_token (str): GitHub access token
        
    Returns:
        list: List of files with their content and changes
    """
    try:
        g = Github(github_token)
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        pr = repo.get_pull(pr_number)
        
        files = []
        for file in pr.get_files():
            file_info = {
                "filename": file.filename,
                "status": file.status,  # 'added', 'modified', 'removed'
                "additions": file.additions,
                "deletions": file.deletions,
                "changes": file.changes,
                "blob_url": file.blob_url,
                "raw_url": file.raw_url,
                "patch": file.patch
            }
            
            # For modified and added files, get the current content
            if file.status != "removed":
                try:
                    content = repo.get_contents(file.filename, ref=pr.head.ref)
                    file_info["content"] = content.decoded_content.decode('utf-8')
                except Exception as e:
                    file_info["content"] = f"Error getting content: {str(e)}"
            
            files.append(file_info)
        
        return files
    except Exception as e:
        logger.error(f"Error getting PR files: {e}")
        return [{"error": str(e)}]

def submit_pr_review(repo_owner: str, repo_name: str, pr_number: int, review_body: str, 
                     comments: List[Dict[str, str]], event: str, github_token: str) -> Dict[str, Any]:
    """
    Submits a review to a pull request with comments on specific files.
    
    Args:
        repo_owner (str): The owner of the repository
        repo_name (str): The name of the repository
        pr_number (int): The pull request number
        review_body (str): Overall review comment
        comments (list): List of review comments for specific files
                         Each comment is a dict with keys: path, position, body
        event (str): Review event type - 'APPROVE', 'REQUEST_CHANGES', or 'COMMENT'
        github_token (str): GitHub access token
        
    Returns:
        dict: Result of the review submission
    """
    try:
        g = Github(github_token)
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        pr = repo.get_pull(pr_number)
        
        # Create review comments
        review_comments = []
        for comment in comments:
            review_comments.append({
                "path": comment["path"],
                "position": comment["position"],
                "body": comment["body"]
            })
        
        # Submit review
        review = pr.create_review(
            body=review_body,
            event=event,
            comments=review_comments
        )
        
        return {
            "id": review.id,
            "state": review.state,
            "submitted_at": review.submitted_at.isoformat() if review.submitted_at else None
        }
    except Exception as e:
        logger.error(f"Error submitting PR review: {e}")
        return {"error": str(e)}

def add_pr_comment(repo_owner: str, repo_name: str, pr_number: int, comment: str, github_token: str) -> Dict[str, Any]:
    """
    Adds a general comment to a pull request.
    
    Args:
        repo_owner (str): The owner of the repository
        repo_name (str): The name of the repository
        pr_number (int): The pull request number
        comment (str): Comment text
        github_token (str): GitHub access token
        
    Returns:
        dict: Result of the comment submission
    """
    try:
        g = Github(github_token)
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        pr = repo.get_pull(pr_number)
        
        # Add comment
        issue_comment = pr.as_issue().create_comment(comment)
        
        return {
            "id": issue_comment.id,
            "created_at": issue_comment.created_at.isoformat()
        }
    except Exception as e:
        logger.error(f"Error adding PR comment: {e}")
        return {"error": str(e)}
