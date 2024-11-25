
git credential-manager  github login

git config --global user.name "Telmo Carmo"
git config --global user.email "telmo.carmo@gmail.com"

git config --list
git status


// create a new repository on the command line

echo "# PyApi1" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/telmo-carmo/PyApi1.git
git push -u origin main


// or push an existing repository from the command line

git remote add origin https://github.com/telmo-carmo/PyApi1.git
git branch -M main
git push -u origin main
---


remote: Permission to telmo-carmo/PyApi1.git denied to telmo-carmo_bdsogit.

---

credential.helper=manager
credential.https://dev.azure.com.usehttppath=true
credential.https://bitbucket.bdso.tech.provider=bitbucket

If you encounter issues with credential storage, try clearing your credential cache:

git config --global --unset credential.helper

and 

git config --global credential.helper manager
