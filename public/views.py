import os
from flask import Flask, request, abort, Response, redirect, url_for, flash, Blueprint, send_from_directory, jsonify
from flask.templating import render_template
from flask.ext.security.utils import verify_password
from user.models import User
from public.models import Message

import datetime
import json

from werkzeug.utils import secure_filename

bp_public = Blueprint('public', __name__, static_folder='../static')

ERR_RESPONSE = {
    "_status": "ERR",
    "_error": {
        "message": "Please provide proper credentials",
        "code": 401
    }
}


@bp_public.route('/robots.txt')
def static_from_root():
    return send_from_directory(bp_public.static_folder, request.path[1:])


@bp_public.route('/enter', methods=['POST'])
def enter_site():
    # Message.objects().delete()
    userd = User.objects(email=str(request.json['username'])).first()
    pwd = userd.password
    if verify_password(str(request.json['password']), pwd):
        return jsonify({'authenticated': verify_password(str(request.authorization['password']), pwd),
                        'username': userd,
                        'first_name': userd.first_name,
                        'last_name': userd.last_name,
                        "_status": "OK"
                        })
    else:
        return jsonify(ERR_RESPONSE)


@bp_public.route('/regis', methods=['POST'])
def reg_user():
    userd = User.objects(email=str(request.json['username'])).first()
    pwd = userd.password
    if verify_password(str(request.json['password']), pwd):
        return jsonify({'authenticated': verify_password(str(request.authorization['password']), pwd),
                        'user': userd,
                        "_status": "OK",
                        })
    else:
        return jsonify(ERR_RESPONSE)


@bp_public.route('/uploader', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            now = datetime.datetime.now()
            filename = secure_filename(file.filename)
            file.save(os.path.join('/Users/Omkareshwar/PycharmProjects/roust/static/img/', 'item' + str(now) + '.jpeg'))
            return jsonify({"filepath": 'static/img/' + filename})
