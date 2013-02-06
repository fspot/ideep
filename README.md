Service web
===========

Ce service associe l'ID d'un sensor à :
  - son eep
  - son nom (== description abrégée)
  - sa description longue
  - sa liste de types

Pour rajouter des associations possibles il suffit de modifier les deux dictionnaires contenus dans `app/ideep.py`.

Ce service tourne à l'adresse http://atom.fspot.org/ideep/.

Exemple d'utilisation :
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

Pour faire tourner le service chez vous :
```bash
$ git clone https://github.com/fspot/ideep.git
$ cd ideep
$ virtualenv venv
$ source venv/bin/activate
$ pip install flask gunicorn
$ cd app
$ gunicorn ideep:app
```

Cela le fera tourner sur le port 8000. Vous pouvez tester à `http://localhost:8000/ideep/`

Conf nginx, chez moi j'ai simplement rajouté :
```bash
location /ideep/ {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```
