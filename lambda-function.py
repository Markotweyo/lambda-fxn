import json
import requests
import os
##
def lambda_handler(event, context):
    # Extract the branch name and commit message from the event
    body = json.loads(event['body'])
    branch_name = body.get('branch_name')
    commit_message = body.get('commit_message')
    file_path = body.get('file_path')
    file_content = body.get('file_content')
    
    # GitLab project and token details
    gitlab_project_id = os.environ['GITLAB_PROJECT_ID']
    gitlab_access_token = os.environ['GITLAB_ACCESS_TOKEN']
    
    # GitLab API URL
    gitlab_api_url = f"https://gitlab.com/api/v4/projects/{gitlab_project_id}/repository/files/{file_path}"
    
    # Create/update the file in the branch
    response = requests.put(
        gitlab_api_url,
        headers={
            'PRIVATE-TOKEN': gitlab_access_token,
            'Content-Type': 'application/json'
        },
        data=json.dumps({
            'branch': branch_name,
            'content': file_content,
            'commit_message': commit_message
        })
    )
    
    # Check response status
    if response.status_code == 200:
        return {
            'statusCode': 200,
            'body': json.dumps('File updated successfully')
        }
    else:
        return {
            'statusCode': response.status_code,
            'body': response.text
        }
