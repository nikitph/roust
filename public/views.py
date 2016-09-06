from flask import Flask, request, abort, Response, redirect, url_for, flash, Blueprint, send_from_directory
from flask.templating import render_template
from flask_security.decorators import roles_required, login_required

bp_public = Blueprint('public',__name__, static_folder='../static')




@bp_public.route('/robots.txt')
def static_from_root():
    return send_from_directory(bp_public.static_folder, request.path[1:])


