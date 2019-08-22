from flask import Flask, g, render_template, redirect, url_for, request, make_response, flash
from peewee import *

import json
import os
import models
import forms

DEBUG = True
PORT = 8080
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = os.urandom(32)


@app.before_request
def before_request():
    """Connect to the db before each request"""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_requst(response):
    """Close the db after each request"""
    g.db.close()
    return response


@app.route("/")
@app.route("/entries")
def listing():
    """
    Renders a listing page of all of the journal entries
    """
    entries = models.Entry.select().limit(100)
    return render_template('index.html', entries=entries)


@app.route("/new", methods=("GET", "POST"))
def add():
    """
    Allows the user to add a journal entry
    """
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Entry added!", "success")
        entry = models.Entry.create_entry(
            title=form.title.data,
            date=form.date.data,
            time_spent=form.time_spent.data,
            learned=form.learned.data,
            resources=form.resources.data
        )
        return redirect(url_for("detail", slug=entry.slug))
    return render_template("new.html", form=form)


@app.route("/entries/<slug>")
def detail(slug):
    """
    Renders the detail page of a journal entry with buttons that allow the user to edit the entry
    """
    entry = models.Entry.get(models.Entry.slug == slug)
    return render_template("detail.html", entry=entry)


@app.route("/entries/<slug>/edit", methods=("GET", "PUT"))
def edit(slug):
    """
    Allows the user to edit the journal entry with a slug of the <slug> passed in.
    """
    entry = models.Entry.get(models.Entry.slug == slug)
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Entry updated!", "success")
        models.Entry.create_entry(
            title=form.title.data,
            date=form.date.data,
            time_spent=form.time_spent.data,
            learned=form.learned.data,
            resources=form.resources.data
        )
    return render_template("edit.html", form=form, entry=entry)


@app.route("/entries/<slug>/delete")
def delete(slug):
    """The Delete route"""
    entry = models.Entry.get(models.Entry.slug == slug)
    entry.delete_instance()
    return redirect("/")


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
