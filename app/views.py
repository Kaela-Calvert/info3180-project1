"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""
import os
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory
from werkzeug.utils import secure_filename
from app import app, db
from app.models import Property
from app.forms import PropertyForm

###
# Routing for your application.
###

# def get_uploaded_images():
#     rootdir = os.getcwd() + '/uploads'
#     image_files = []
#     for subdir, dirs, files in os.walk(rootdir):
#         for file in files:
#             if file.endswith(('.jpg', '.png','.jpeg')):
#                 image_files.append(file)
#     return image_files


@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'uploads'), filename)


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

app.config['UPLOAD_FOLDER'] = './uploads'
@app.route('/properties/create', methods=['GET', 'POST'])
def create_property():
    form = PropertyForm()
    if form.validate_on_submit():
        # Save the uploaded file
        file = request.files['photo']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Save the form data to the database
        property = Property(
            title=form.title.data,
            bedrooms=form.bedrooms.data,
            bathrooms=form.bathrooms.data,
            location=form.location.data,
            price=form.price.data,
            type=form.type.data,
            description=form.description.data,
            photo=filename  
        )
        db.session.add(property)
        db.session.commit()
        
        flash('Property added successfully!', 'success')
        return redirect(url_for('properties'))
        #return render_template('properties.html')
    return render_template('create_property.html', form=form)


# # Route to display a list of all properties in the database
# @app.route('/properties')
# def properties():
#     properties = Property.query.all()
#     for property in properties:
#         property.photo = os.path.join(app.config['UPLOAD_FOLDER'], property.photo)
#         # print(property.photo)
#     return render_template('properties.html', properties=properties)

@app.route('/properties')
def properties():
    properties = Property.query.all()
    # image_files = get_uploaded_images()  # Get a list of uploaded image filenames
    for property in properties:
        # if property.photo in image_files:
        #     property.photo = url_for('get_image', filename=property.photo)
        
        return render_template('properties.html', properties=properties)

# Route to view an individual property by its ID
@app.route('/properties/<int:propertyid>')
def view_property(propertyid):
    property = Property.query.get_or_404(propertyid)    
    return render_template('property.html', property=property)

###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
