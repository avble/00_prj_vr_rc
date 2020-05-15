import os, sys 
import string
import random
import hashlib

from time import gmtime, strftime
from random import random


from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import Blueprint

from .db import db_get
from .auth import login_required


bp = Blueprint("peer", __name__)

################################################
### Utility
################################################
def key_generate(user):
    time_now = strftime(user + "%a, %d %b %Y %H:%M:%S +0000", gmtime())
    time_now = "%s-%f" % (time_now, random())
    md = hashlib.md5(time_now.encode())
    md_digest = md.hexdigest()
    return md_digest[-6:]

################################################
##### peer service #################
@bp.route('/peer/register', methods = ['POST'])
def peer_register():
    #print ("Register >> peer_register >>>ENTER ")
    db = db_get()
    code = key_generate('user')
    shareinfo = 'mqtt/mac012'
    db.execute(
        "INSERT INTO invitation (code, shareinfo) VALUES (?, ?)",
        (code, shareinfo),
    )
    db.commit()

    return code, 200

@bp.route('/peer/get/<string:peer_id>', methods = ['GET'])
def peer_get(peer_id):
    db = db_get()
    share_info = db.execute(
        'SELECT shareinfo FROM invitation WHERE code = "%s"' % (peer_id)
        ).fetchone()

    if share_info:
        return share_info['shareinfo'], 200
    else:
        return "NONE", 200
        

################################################
### view page 
@bp.route('/')
@login_required
def index():
    db = db_get()
    invitations = db.execute(
        "SELECT code, shareinfo, created"
        " FROM invitation"
        " ORDER BY created DESC"
    ).fetchall()

    return render_template('invite/index.html', invitations=invitations)

@bp.route('/peer/delete/<string:peer_id>', methods = ('POST', 'GET'))
def peer_delete(peer_id):
    # Get formdate
    db = db_get()
    sql_string =  "DELETE FROM invitation WHERE code = \"%s\"" % (peer_id)
    #print ( "peer_delete >>> " + sql_string + " peer_delete >>>")
    db.execute(sql_string)
    db.commit()

    return redirect(url_for("peer.index"))
