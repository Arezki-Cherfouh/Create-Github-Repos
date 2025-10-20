import os
import subprocess
import requests
GITHUB_USERNAME = input("You github username: ")
GITHUB_TOKEN = input("You github token: ")
BASE_DIR = input("Path to folder to deploy from: ")# Path to dir to deploy
PRIVATE = input("Private repo (Y/n)")
if PRIVATE.lower()=="n":
  PRIVATE=False
else:
  PRIVATE=True
def run(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running: {cmd}\n{result.stderr}")
    return result.stdout.strip()
def create_github_repo(repo_name,description):
    url = "https://api.github.com/user/repos"
    data = {"name": repo_name, "private": PRIVATE, "description": description}
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f"[+] Created GitHub repo: {repo_name}")
        return response.json()["clone_url"]
    elif response.status_code == 422:
        print(f"[!] Repo '{repo_name}' already exists.")
        return f"https://github.com/{GITHUB_USERNAME}/{repo_name}.git"
    else:
        raise Exception(f"Failed to create repo {repo_name}: {response.text}")
def get_description(folder_path):
    readme_path = os.path.join(folder_path, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            if first_line:
                return first_line[:350]
    return f"Auto-uploaded project: {os.path.basename(folder_path)}"
def push_folder(folder_path):
    repo_name = os.path.basename(folder_path)
    description = get_description(folder_path)
    clone_url = create_github_repo(repo_name,description)
    print(f"→ Pushing {repo_name} ...")
    run("git init", cwd=folder_path)
    run("git add .", cwd=folder_path)
    run('git commit -m "Initial commit"', cwd=folder_path)
    run(f"git branch -M main", cwd=folder_path)
    run(f"git remote add origin {clone_url}", cwd=folder_path)
    run("git push -u origin main", cwd=folder_path)
    print(f"[✓] {repo_name} pushed successfully.\n")
def main():
    if not os.path.exists(BASE_DIR):
        print(f"Directory does not exist: {BASE_DIR}")
        return
    for folder in os.listdir(BASE_DIR):
        full_path = os.path.join(BASE_DIR, folder)
        if os.path.isdir(full_path):
            push_folder(full_path)
main()
