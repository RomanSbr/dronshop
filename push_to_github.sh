#!/bin/bash

# Script to push dronshop project to GitHub
# Make sure you have GitHub credentials configured first

echo "Pushing dronshop project to GitHub..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "Error: Not a git repository"
    exit 1
fi

# Check remote origin
echo "Current remote origin:"
git remote -v

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub!"
    echo "Repository: https://github.com/RomanSbr/dronshop"
else
    echo "❌ Failed to push to GitHub"
    echo ""
    echo "To fix authentication issues:"
    echo "1. Generate a GitHub Personal Access Token:"
    echo "   - Go to GitHub Settings > Developer settings > Personal access tokens"
    echo "   - Generate new token with 'repo' scope"
    echo "2. Use token as password when prompted"
    echo ""
    echo "Or configure credentials:"
    echo "git config --global user.name 'Your Name'"
    echo "git config --global user.email 'your.email@example.com'"
    echo "git config --global credential.helper store"
fi