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
    This view should render a listing page of all of the journal entries, where each entry displays the following
    fields:
    Title - should be a linked title, clicking it routes user to the detail page for the clicked entry.
    Date - Each entry should have a date created listed somewhere beneath the title.
    """
    entries = models.Entry.select().limit(100)
    return render_template('index.html', entries=entries)


@app.route("/new", methods=("GET", "POST"))
def add():
    """
    Allows the user to add a journal entry with the following fields: Title, Date, Time Spent, What You Learned, and
    Resources to Remember
    """
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Entry added!", "success")
        models.Entry.create_entry(
            title=form.title.data,
            date=form.date.data,
            time_spent=form.time_spent.data,
            learned=form.learned.data,
            resources=form.resources.data
        )
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


@app.route("/entries/<edit>/delete")
def delete(edit):
    """The Delete route"""
    pass


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
