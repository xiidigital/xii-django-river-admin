#!/usr/bin/env sh

# abort on errors
set -e

# build
npm run build

# navigate into the build output directory
cd dist

# NOTE: this fork does not have a custom domain configured yet.
# If/when one is chosen, uncomment and set it below:
# echo 'www.example.com' > CNAME

git init
git add -A
git commit -m 'deploy'

# if you are deploying to https://<USERNAME>.github.io/<REPO>
git push -f git@github.com:xiidigital/xii-django-river-admin.git master:gh-pages

cd -
