# Useful Github stuff
<br>

### Pull requests
1. **Fork the Repository**: Visit the repository's page on GitHub and click on the "Fork" button in the top-right corner. This will create a copy of the repository under your GitHub account.
2. **Clone the Forked Repository**: On your GitHub account, navigate to the forked repository and click on the `Code` button. Copy the HTTPS or SSH URL of the repository. Open a terminal on your local machine and run the following command, replacing `<repository-url>` with the copied URL:
```
git clone <repository-url>
```
4. **Create a New Branch**: Change into the newly created repository's directory using the cd command. Next, create a new branch using the following command, replacing <branch-name> with a descriptive name for your branch:
```
git checkout -b <branch-name>
```
6. **Make the Desired Changes**: Use your preferred text editor or IDE to make the necessary changes to the codebase. Make sure to thoroughly test your changes before proceeding.
7. **Commit Your Changes**: Once you are satisfied with your changes, commit them by running the following command:
```
git add .
git commit -m "Your-commit-message"
```
6. **Push Changes to Your Forked Repository**: Push the changes to your forked repository by running the following command:
```
git push origin <branch-name>
```
8. **Submit the Pull Request**: After pushing the changes, visit the original repository where you forked from on GitHub. You should see a banner with an option to create a pull request from your recently pushed branch. Click on it, provide a descriptive title and comment, and then click on "Create Pull Request.
<br>

### Fetch changes from remote repository to local
1. Start by navigating to your local repository using the command line or terminal.
2. Fetch the changes from the remote repository using the following command:
```
git fetch origin
```
3. Switch to the branch that you want to merge the changes into. For example, if you want to merge the changes into the main branch, use the following command:
```
git checkout main
```
4. Merge the changes from the remote repository into your local branch using the following command:
```
git merge origin/<branch-name>
```
**Note**: `<branch-name>` represents the branch name of the remote repository that you want to merge.
5. Resolve any merge conflicts that arise. If Git is unable to automatically merge changes, it will notify you about conflicting files. Open those files and manually merge the conflicting changes.
6. After resolving the merge conflicts, add the changes to the staging area using the following command:
```
git add .
```
7. Commit the merged changes using a commit message that describes the merge operation:
```
git commit -m "Merge remote repository changes"
```
8. Push the merged changes to the remote repository using the following command:
```
git push origin <branch-name>
```
<br>


## Push changes from your local repository to a remote GitHub repository
1. **Commit Your Changes**: First, make sure you've committed the changes you want to push to the local repository. Use the following commands to commit your changes:
```
git add .
git commit -m "Your commit message here"
```
2. **Check Your Remotes**: Ensure that you have added the remote repository to your local Git configuration. You can list your remotes using the following command:
```
git remote -v
```
If your remote isn't listed, you'll need to add it. You can do this with the git remote add command:
```
git remote add origin <remote_url>
```
* Replace `<remote_url>` with the URL of your GitHub repository.
Push to the Remote: Once your changes are committed, you can push them to the remote repository. Use the following command:
```
git push origin <branch_name>
```
<br>


## Hard reset (uncommit commits)
1. **Copy the hash of the commit you want to reset to**: Go to Github → Commits → Copy the full SHA
2. **Hard reset**: Use this command to reset to your desired commit
```
git reset --hard <SHA>
```
* Replace `<SHA>` with the hash of your commit
4. **Push to Remote**: You need to force-push your branch to the remote repository to update it. The git push command with the --force or -f option is used for this purpose.
```
git push -f origin <branch_name>
```
