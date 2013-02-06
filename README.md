Service web
===========

Ce service associe l'ID d'un sensor à :
  - son eep
  - son nom (== description abrégée)
  - sa description longue
  - sa liste de types

Pour rajouter des associations possibles il suffit de modifier les deux dictionnaires contenus dans `app/ideep.py`.

Ce service tourne à l'adresse http://atom.fspot.org/ideep/.

Exemple d'utilisation
---------------------

  - Requête http GET sur `http://atom.fspot.org/ideep/42`
  - Réponse (format JSON) =

```javascript
{
	"found": true, 
	"eep": "05-02-01"
	"name": "Interrupteur", 
	"description": "Double interrupteur blanc", 
	"datatypes": [
		"switch", 
		"switch", 
		null, 
		null, 
		null, 
		null
	], 
}
```

Attention, dans l'url, 42 est passé en tant que **chaîne**.
C'est pourquoi dans le dictionnaire d'association `id => eep`, l'id est également une **chaîne**.

Si l'ID est inconnu, la réponse sera toujours `{"found": false}`

Mise en place
-------------

*Requiert python2.7, virtualenv et pip :*
```bash
# ubuntu :
$ sudo apt-get install python-pip
$ sudo pip install virtualenv
```

Pour installer le nécessaire :
```bash
$ git clone https://github.com/fspot/ideep.git
$ cd ideep
$ ./setupvenv.sh
```
Puis, pour lancer le service :
```bash
$ cd ideep
$ source venv/bin/activate
$ cd app
$ gunicorn ideep:app -b :8000
```
=> ça fait tourner le service sur le port 8000. Vous pouvez tester à `http://localhost:8000/ideep/`

Conf nginx
----------

Chez moi j'ai simplement rajouté une section :
```bash
location /ideep/ {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```
