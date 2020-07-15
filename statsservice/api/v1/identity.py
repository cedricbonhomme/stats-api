#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, current_app
from datetime import datetime
from flask_login import LoginManager, login_user, current_user
from flask_principal import (
    Principal,
    Identity,
    Permission,
    UserNeed,
    RoleNeed,
    session_identity_loader,
    identity_changed,
    identity_loaded
)

from statsservice.models.client import ROLE_USER, ROLE_ADMIN
from statsservice.bootstrap import application
from statsservice.models import Client


Principal(current_app)
login_manager = LoginManager()
login_manager.init_app(current_app)

user_role = RoleNeed(ROLE_USER)
admin_role = RoleNeed(ROLE_ADMIN)

user_permission = Permission(user_role)
admin_permission = Permission(admin_role)


@login_manager.user_loader
def load_user(client_id):
    return Client.query.filter(Client.id == client_id).first()


@application.before_request
def before_request():
    print('before_request')
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


def login_user_bundle(client):
    login_user(client)
    identity_changed.send(current_app, identity=Identity(client.id))
    session_identity_loader()


@identity_loaded.connect_via(application)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if current_user.is_authenticated:
        identity.provides.add(UserNeed(current_user.id))
        if current_user.role == ROLE_USER:
            identity.provides.add(user_role)
        if current_user.role == ROLE_ADMIN:
            identity.provides.add(admin_role)
