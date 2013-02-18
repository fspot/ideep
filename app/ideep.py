#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, jsonify
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
null = None  # au cas ou un 'null' traine...

# Ici on mettra tout ce qui définit un eep.
# Ce dictionnaire est censé être figé,
# tant que de nouveaux modèles de capteurs de sortent pas.
eep_to_info = {
    '07-02-01': {
        "eep": "07-02-01",
        "name": "Capteur de température (A)",
        "description": "Capteur de température, modèle A",
        "datatypes": ["temperature", None, None, None, None, None]
    },
    '07-02-04': {
        "eep": "07-02-04",
        "name": "Capteur de température (B)",
        "description": "Capteur de température, modèle B",
        "datatypes": ["temperature", None, None, None, None, None]
    },
    '07-02-07': {
        "eep": "07-02-07",
        "name": "Capteur de température (C)",
        "description": "Capteur de température, modèle C",
        "datatypes": ["temperature", None, None, None, None, None]
    },
    '05-02-01': {
        "eep": "05-02-01",
        "name": "Interrupteur",
        "description": "Double interrupteur blanc",
        "datatypes": ["switch", "switch", None, None, None, None]
    },
    '06-00-01': {
        "eep": "06-00-01",
        "name": "Contacteur de porte/fenêtre",
        "description": "Contacteur de porte/fenêtre blanc",
        "datatypes": ["contact", None, None, None, None, None]
    },
    '07-08-02': {
        "eep": "07-08-02",
        "name": "Capteur multifonctions (A)",
        "description": "Capteur multifonctions (température, présence, luminosité), modèle A",
        "datatypes": ["temperature", "occupancy", None, None, None, None]
    },
}

# Ce dictionnaire en revanche, sera à modifier à chaque nouvel ID
# Il va sans dire que dans un cas réel, il y aurait probablement une astuce
# arithmétique pour passer d'un id à un eep.
# (sinon il y aurait beaucoup trop de données)
# Mais pour ce tp on s'en contentera.
id_to_eep = {
    '42': '05-02-01',  # <== keys must be strings !
    'test': '05-02-01',
    '2214961': '05-02-01',  # <== 0x21CC31, interrupteur blanc n°4
    '346751': '07-08-02',  # <== 0x00054A7F, capteur multifonction  n°6
    '111198': '06-00-01',  # <== 0x001B25E, Contacteur de porte/fenêtre  n°6
}


# DO NOT MODIFY BELOW
def id_to_info(idy):
    if idy in id_to_eep:
        eep = id_to_eep[idy]
        if eep in eep_to_info:
            return eep_to_info[eep]
    return None


@app.route('/ideep/')
def ideep_index():
    ''' racine '''
    return jsonify({'msg': 'It Works :)', 'status': 'success'})


@app.route('/ideep/<idy>')
def ideep_mapping(idy):
    obj = id_to_info(idy)
    if obj is None:
        obj = {'found': False}
    else:
        obj['found'] = True
    return jsonify(obj)


app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
