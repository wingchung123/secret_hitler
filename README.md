# Secret Hitler Game

Uses containers, express & AWS resources (back-end)

[Markdown Guide](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

Sublime Markdown -> Markdown Preview Package, alt-m to preview


## Useful docker commands 
[Docker Guide](https://nodejs.org/en/docs/guides/nodejs-docker-webapp/)


`docker-machine ip default` show docker-machine ip

`docker build -t wing/secret-hitler .` build image

`docker run -p 49160:8080 -d wing/secret-hitler --name test-env` run image on container; -d to run in background, -p to publish port & link to machine port

`docker ps || docker container ls`

`docker stop <container-name>`

`docker system prune`




## Useful node commands

`npm start`

`npm install <package-name> --save` (replace --save with --save-dev for dev packages)

Nodemon has been installed for dev. Code changes automatically applied