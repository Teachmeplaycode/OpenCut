#!/bin/bash
# GitHub setup and push script for OpenCut
# Run this script to push OpenCut to GitHub and invite collaborators

echo "OpenCut GitHub Setup"
echo "===================="
echo ""

# Check if git remote already exists
if git remote -v > /dev/null 2>&1; then
    echo "Git remote already configured"
    git remote -v
else
    echo "Please enter your GitHub username:"
    read github_user
    
    echo "Please enter your desired repository name (default: OpenCut):"
    read repo_name
    repo_name=${repo_name:-OpenCut}
    
    # Add remote
    git remote add origin "https://github.com/$github_user/$repo_name.git"
    echo "Added remote: https://github.com/$github_user/$repo_name.git"
fi

echo ""
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "To invite 'Teachmeplaycode' as a collaborator, run:"
echo "  gh repo invite Teachmeplaycode --role push"
echo ""
echo "Or manually:"
echo "1. Go to https://github.com/yourusername/OpenCut/settings/access"
echo "2. Click 'Invite a collaborator'"
echo "3. Enter username: Teachmeplaycode"
echo "4. Select role (Write recommended)"
echo "5. Click 'Add'"
