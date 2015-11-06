How I would do this

`git checkout master`
`git pull origin master`
`git merge test`
`git push origin master`
If I have a local branch from a remote one, I don't feel comfortable with merging other branches than this one with the remote. Also I would not push my changes, until I'm happy with what I want to push and also I wouldn't push things at all, that are only for me and my local repository. In your description it seems, that test is only for you? So no reason to publish it.

git always tries to respect yours and others changes, and so will --rebase. I don't think, I can explain it appropriately, so have a look at the Git book - Rebasing or git-reade: Intro into rebasing for a little description. It's a quite cool feature
