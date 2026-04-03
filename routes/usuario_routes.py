from flask import Blueprint, request, redirect, url_for, render_template, flash
from models import Usuario
from database.databanco import db
from sqlalchemy.exc import IntegrityError

usuario_bp = Blueprint("usuarios", __name__)
