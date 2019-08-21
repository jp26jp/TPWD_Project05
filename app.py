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


@app.route("/entries/<slug>")
def detail(slug):
    """
    This view should render a detail page of a journal entry, it should display the following fields on the page:
    Title
    Date
    Time Spent
    What You Learned
    Resources to Remember.
    NOTE: This page should contain a link/button that takes the user to the Edit route for the Entry with this <id>.
    """
    entry = models.Entry.get(models.Entry.slug == slug)
    return render_template("detail.html", entry=entry)


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


@app.route("/entries/<id>/edit")
def edit(id):
    """
    Create an edit view with the route /entries/<id>/edit that allows the user to edit the journal entry with an id of the <id> passed in:
    Title - string
    Date - date
    Time Spent - integer
    What You Learned - text
    Resources to Remember - text
    Ideally, you should prepopulate each form field with the existing data on load. So the form is filled out with the existing data so the User can easily see what the value is and make edits to the form to make the update.
    NOTE: Updating an Entry should not result in a new Entry being created, this behavior would not be seen as editing this would be adding a new entry. To check this, you can simply make an edit and then reload the listing page to see if a duplicate record was created.
    """
    return render_template("edit.html")


@app.route("/entries/<id>/delete")
def delete(id):
    """The Delete route"""
    pass


if __name__ == '__main__':
    models.initialize()
    # models.Entry.create_entry(
    #     title="A cool title", date="05/09/1991", time_spent="10", learned="So many things", resources="Tons of them"
    # )
    app.run(debug=DEBUG, host=HOST, port=PORT)
