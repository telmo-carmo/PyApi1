
git credential-manager  github login
(in popup prompt choose 'telmo-carmo' )

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

or add:

git config --global http.sslBackend schannel

---

credential.helper=manager
credential.https://dev.azure.com.usehttppath=true
credential.https://bitbucket.bdso.tech.provider=bitbucket

If you encounter issues with credential storage, try clearing your credential cache:

git config --global --unset credential.helper

and 

git config --global credential.helper manager

AND for VS 2022 17.13 can do Git push must do this:


git config --global  http.https://github.com.proxy http://proxy-vpn.glb.besp.dsp.gbes:8080

---

// Force-Push to the Remote Main Branch:

git commit -m "Force-pushing <filename>"
git push -f origin main

also for using NB git account do:
git clone https://telmo-carmo_bdsogit@github.com/telmo-carmo_bdsogit/reactweb1.git


