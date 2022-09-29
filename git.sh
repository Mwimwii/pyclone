git stash
git checkout master
git pull
branch=$RANDOM
file=$RANDOM
git checkout -b $branch
mkdir files
touch files/$file
git add files/$file
git commit -m 'Message


Co-authored-by: Bryan Allen <Dr.Frankenmiller@gmail.com>
Co-authored-by: gooby <mpnyirongo@gmail.com>'
# git push --set-upstream origin $branch