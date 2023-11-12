# Useful Github stuff

## Hard reset (uncommit commits)
- Copy the hash of the commit you want to reset to: Go to Github → Commits → Copy the full SHA
- Hard reset: Use this command to reset to your desired commit
 - 'git reset --hard <SHA>'
   - Replace <SHA> with the hash of your commit
- Push to Remote: You need to force-push your branch to the remote repository to update it. The git push command with the --force or -f option is used for this purpose.
 - 'git push -f origin <branch_name>'
