from flask import Blueprint, request, render_template, redirect, url_for, flash
from models import Livro
from database.databanco import db
from sqlalchemy.exc import IntegrityError

livro_bp = Blueprint("livros", __name__)