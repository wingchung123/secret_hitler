# Secret Hitler Game

Uses containers, express & AWS resources (back-end)

Game Rules: https://secrethitler.com/assets/Secret_Hitler_Rules.pdf

[Markdown Guide](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

Sublime Markdown -> Markdown Preview Package, alt-m to preview

Sample Pictures: https://medium.com/@mackenzieschubert/secret-hitler-illustration-graphic-design-435be3e3586c

(policy: 188px by 268px)


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




## Nodejs Web Dev Tutorials

[Nodejs Response Object](https://www.tutorialspoint.com/nodejs/nodejs_response_object.htm)

[Using cookies](https://www.tutorialspoint.com/expressjs/expressjs_cookies.htm)

[Bootstrap Typography](https://www.w3schools.com/bootstrap/bootstrap_typography.asp)



## Future Enhancements


| Function        | Use Case           | Sudo-code  |
| --------------- |--------------------| -----------|
| Force Player Login| When a user wants to rejoin a game (via cookie) but they enter the incorrect game ID so it overwrites the original cookie gameID| Add a button on player create the opens a new dialogue. First check to see if name exists for that game id, if it does, have the function return player id, log it in the cookie and proceed to player index |





