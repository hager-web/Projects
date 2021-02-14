#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy.sql import func
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app,db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# --------------------Venue Model------------------
class Venue(db.Model):
  __tablename__ = 'venue'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable =False, unique=True)
  city = db.Column(db.String(120), nullable =False)
  state = db.Column(db.String(120), nullable =False)
  address = db.Column(db.String(120), nullable =False)
  phone = db.Column(db.String(120), nullable =False)
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  genres = db.Column(db.ARRAY(db.String(50)), nullable =False)
  website = db.Column(db.String(120))
  seeking_talent = db.Column(db.Boolean, default=False )
  seeking_description = db.Column(db.Text())

  shows = db.relationship('Show', backref='venue', lazy=True)

  def __repr__(self):
    return "<Venue(venue id='%s', name='%s', city='%s', genres='%s')>" % (self.id, self.name, self.city,self.genres)
  

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
# --------------------Artist Model---------------------
class Artist(db.Model):
  __tablename__ = 'artist'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable =False , unique=True)
  city = db.Column(db.String(120), nullable =False)
  state = db.Column(db.String(120), nullable =False)
  phone = db.Column(db.String(120), nullable =False)
  genres = db.Column(db.ARRAY(db.String(50)), nullable =False)
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website = db.Column(db.String(120))
  seeking_venue = db.Column(db.Boolean, default=False )
  seeking_description = db.Column(db.Text())

  shows = db.relationship('Show', backref='artist', lazy=True)

  def __repr__(self):
    return "<Artist(artist id='%s', name='%s', city='%s')>" % (self.id, self.name, self.city)

# ------------------Show Model---------------------
class Show(db.Model):
  __tablename__ = 'show'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable = False)

  def __repr__(self):
    return "<Show(artist id='%s', venue id='%s', start time='%s')>" % (self.artist_id, self.venue_id, self.start_time)
  
  @property
  def show_details(self):
    return{
        'venue_id' :self.venue_id,
        'venue_name' :self.Venue.name,
        'artist_id' :self.artist_id,
        'artist_name' :self.Artist.name,
        'artist_image_link' :self.Artist.image_link,
        'start_time' :self.start_time
    }
  

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  city_states  = Venue.query.with_entities(Venue.city, Venue.state).distinct().all()
  print(city_states)
  for city_state in city_states:
    city = city_state.city
    state = city_state.state
    venues=[]
    print(city,state)
    venueslist = Venue.query.filter_by(city=city, state=state).all()
    num_upcoming_shows= 0
    for venue in venueslist :
      try:
        upcoming_shows = venue.shows.filter(Show.start_time > datetime.now()).all()
        print(upcoming_shows)
        num_upcoming_shows=len(upcoming_shows)
      except:
        print(num_upcoming_shows)
      
      venues.append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": num_upcoming_shows})

    data.append({
      "city": city,
      "state": state,
      "venues": venues})
  print(data)
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  data = []
  try:
    stmt = db.session.query(Show.venue_id, func.count('*').\
         label('upcoming_show_count')).filter(Show.start_time > datetime.now()).\
         group_by(Show.venue_id).subquery()
    for v_id, v_name, count in db.session.query(Venue.id, Venue.name, stmt.c.upcoming_show_count).filter(Venue.name.ilike('%' + search_term + '%')).\
      outerjoin(stmt, Venue.id==stmt.c.venue_id).order_by(Venue.id):
      print(v_id,v_name, count)
      data.append({
          "id": v_id,
          "name": v_name,
          "num_upcoming_shows": count})
    
  except:
    print ("not found")
  
  count = len(data)
  response = {
    "count": count,
    "data": data
  }
  
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  data = {}
  if venue:
    # get past_shows for venue
    past_shows = []
    try:
      shows = Show.query.join(
        Venue, (Venue.id == Show.venue_id)
        ).join(Artist, (Artist.id == Show.artist_id)
        ).filter(Show.start_time<datetime.now(),venue.id == Show.venue_id
        ).with_entities(
          Artist.id.label('artist_id'), 
          Artist.name.label('artist_name'), 
          Artist.image_link, 
          Show.start_time)

      for show in shows:
        past_shows.append({
          "artist_id": show.artist_id,
          "artist_name": show.artist_name,
          "artist_image_link": show.image_link,
          "start_time": str(show.start_time)
        })
    except:
      print("no past shows")
    upcoming_shows = []
    try:
      shows = Show.query.join(
        Venue, (Venue.id == Show.venue_id)
        ).join(Artist, (Artist.id == Show.artist_id)
        ).filter(Show.start_time>datetime.now(),venue.id == Show.venue_id
        ).with_entities(
          Artist.id.label('artist_id'), 
          Artist.name.label('artist_name'), 
          Artist.image_link, 
          Show.start_time)

      for show in shows:
        upcoming_shows.append({
          "artist_id": show.artist_id,
          "artist_name": show.artist_name,
          "artist_image_link": show.image_link,
          "start_time": str(show.start_time)
        })
    except:
      print("no upcoming shows")
    print(venue.id)
    data = {
      "id": venue.id,
      "name": venue.name,
      "genres": venue.genres,
      "address": venue.address,
      "city": venue.city,
      "state": venue.state,
      "phone": venue.phone,
      "website": venue.website,
      "facebook_link": venue.facebook_link,
      "seeking_talent": venue.seeking_talent,
      "image_link": venue.image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcoming_shows)
    }
  else:
    return render_template('errors/404.html'), 404


  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead DONE
  # TODO: modify data to be the data object returned from db insertion
  # venue = request.form
  try:
    # venue = Venue(
    #   name=request.form['name'],
    #   genres=request.form.getlist('genres'),
    #   address=request.form['address'],
    #   city=request.form['city'],
    #   state=request.form['state'],
    #   phone=request.form['phone'],
    #   facebook_link=request.form['facebook_link'],    
    #   website=request.form['website'],
    #   image_link=request.form['image_link'],
    #   seeking_talent=True if request.form['seeking_talent'] in ('y', True, 't', 'True') else False,
    #   seeking_description=request.form['seeking_description'],
    # )
    # print(venue.seeking_talent)
    exists = db.session.query(db.exists().where(Venue.name == request.form['name'])).scalar()
    print(exists)
    if exists:
      flash('This venue is already exist')
      return render_template('pages/venues.html')

    venue = Venue()
    for field in request.form:
      if field == 'genres':
        setattr(venue, field, request.form.getlist(field))
      elif field == 'seeking_talent':
        setattr(venue, field, True if request.form.get(field) in ('y', True, 't', 'True') else False)
      else:
        setattr(venue, field, request.form.get(field))  
    try :
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except :
      db.session.rollback()
      flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
      return render_template('errors/500.html'), 500
    finally:
      db.session.close()

  except:
    return render_template('errors/500.html'), 500

  
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead. DONE
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  venue = Venue.query.get(venue_id)
  try:
    db.session.delete(venue)
    db.session.commit()
    flash('Venue ' + venue.name + ' was successfully deleted!')
  except :
    db.session.rollback()
    flash('An error occurred. Venue ' + venue.name + ' could not be deleted.') 
    return render_template('errors/500.html'), 500
  finally:
    db.session.close()
  return render_template('pages/home.html')
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  # return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data  = Artist.query.with_entities(Artist.id, Artist.name).all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  data = []
  try:
    stmt = db.session.query(Show.artist_id, func.count('*').\
         label('upcoming_show_count')).filter(Show.start_time > datetime.now()).\
         group_by(Show.artist_id).subquery()
    for a_id, a_name, count in db.session.query(Artist.id, Artist.name, stmt.c.upcoming_show_count).filter(Artist.name.ilike('%' + search_term + '%')).\
      outerjoin(stmt, Artist.id==stmt.c.artist_id).order_by(Artist.id):
      print(a_id,a_name, count)
      data.append({
          "id": a_id,
          "name": a_name,
          "num_upcoming_shows": count})
    
  except:
    print ("not found")
  
  count = len(data)
  response = {
    "count": count,
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.get(artist_id)
  data = {}
  if artist:
    # get past_shows for artist
    past_shows = []
    try:
      shows = Show.query.join(
        Venue, (Venue.id == Show.venue_id)
        ).join(Artist, (Artist.id == Show.artist_id)
        ).filter(Show.start_time<datetime.now(),artist.id == Show.artist_id
        ).with_entities(
          Venue.id.label('venue_id'), 
          Venue.name.label('venue_name'), 
          Venue.image_link, 
          Show.start_time)

      for show in shows:
        past_shows.append({
          "venue_id": show.venue_id,
          "venue_name": show.venue_name,
          "venue_image_link": show.image_link,
          "start_time": str(show.start_time)
        })
    except:
      print("no past shows")
    upcoming_shows = []
    try:
      shows = Show.query.join(
        Venue, (Venue.id == Show.venue_id)
        ).join(Artist, (Artist.id == Show.artist_id)
        ).filter(Show.start_time>datetime.now(),artist.id == Show.artist_id
        ).with_entities(
          Venue.id.label('venue_id'), 
          Venue.name.label('venue_name'), 
          Venue.image_link, 
          Show.start_time)

      for show in shows:
        upcoming_shows.append({
          "venue_id": show.venue_id,
          "venue_name": show.venue_name,
          "venue_image_link": show.image_link,
          "start_time": str(show.start_time)
        })
    except:
      print("no upcoming shows")
    print(artist.id)
    data = {
      "id": artist.id,
      "name": artist.name,
      "genres": artist.genres,
      "city": artist.city,
      "state": artist.state,
      "phone": artist.phone,
      "website": artist.website,
      "facebook_link": artist.facebook_link,
      "seeking_venue": artist.seeking_venue,
      "image_link": artist.image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcoming_shows)
    }
  else:
    return render_template('errors/404.html'), 404



  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

# --------------------------------------
# ---------------delete artist----------

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  artist = Artist.query.get(artist_id)
  try:
    db.session.delete(artist)
    db.session.commit()
    flash('Artist ' + artist.name + ' was successfully deleted!')
  except :
    db.session.rollback()
    flash('An error occurred. Artist ' + artist.name + ' could not be deleted.') 
    return render_template('errors/500.html'), 500
  finally:
    db.session.close()
  return render_template('pages/home.html')
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  try:
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)
  except:
    return render_template('errors/500.html'), 500
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  # get artist by id and edit it
  try:
    artist = Artist.query.get(artist_id)
    for field in request.form:
      if field == 'genres':
        setattr(artist, field, request.form.getlist(field))
      elif field == 'seeking_venue':
        setattr(artist, field, True if request.form.get(field) in ('y', True, 't', 'True') else False)
      else:
        setattr(artist, field, request.form.get(field))  
    try :
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully modified!')
    except :
      db.session.rollback()
      flash('An error occurred. Artist ' + artist.name + ' could not be modified.')
      
      return render_template('errors/500.html'), 500
    finally:
      db.session.close()
  except:
    return render_template('errors/500.html'), 500

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
  except:
    return render_template('errors/500.html'), 500
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    venue = Venue.query.get(venue_id)
    for field in request.form:
      if field == 'genres':
        setattr(venue, field, request.form.getlist(field))
      elif field == 'seeking_talent':
        setattr(venue, field, True if request.form.get(field) in ('y', True, 't', 'True') else False)
      else:
        setattr(venue, field, request.form.get(field))  
      try :
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully modified!')
      except :
        db.session.rollback()
        flash('An error occurred. Venue ' + venue.name + ' could not be modified.')
        
        return render_template('errors/500.html'), 500
      finally:
        db.session.close()
  except:
    return render_template('errors/500.html'), 500

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
    exists = db.session.query(db.exists().where(Artist.name == request.form['name'])).scalar()
    print(exists)
    if exists:
      flash('This artist is already exist')
      return render_template('pages/artists.html')
    artist = Artist()
    for field in request.form:
      if field == 'genres':
        setattr(artist, field, request.form.getlist(field))
      elif field == 'seeking_venue':
        setattr(artist, field, True if request.form.get(field) in ('y', True, 't', 'True') else False)
      else:
        setattr(artist, field, request.form.get(field))  
    try :
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except :
      db.session.rollback()
      flash('An error occurred. Artist ' + artist.name + ' could not be listed.')
      
      return render_template('errors/500.html'), 500
    finally:
      db.session.close()

  except:
    return render_template('errors/500.html'), 500

  # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  try:
    data=[]
    shows_details = Show.query.join(
        Venue, (Venue.id == Show.venue_id)
        ).join(Artist, (Artist.id == Show.artist_id)
        ).with_entities(
          Show.venue_id, 
          Venue.name.label('venue_name'),
          Show.artist_id, 
          Artist.name.label('artist_name'), 
          Artist.image_link, 
          Show.start_time)

    for show in shows_details:
      data.append({
        "venue_id": show.venue_id,
        "venue_name": show.venue_name,
        "artist_id": show.artist_id,
        "artist_name": show.artist_name,
        "artist_image_link": show.image_link,
        "start_time": str(show.start_time)
      })
  except:
    return render_template('errors/400.html'), 400
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    show = Show()
    for field in request.form:
        setattr(show, field, request.form.get(field))  
    try :
      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!')
    except :
      db.session.rollback()
      flash('An error occurred. Show could not be listed.')
      return render_template('errors/500.html'), 500
    finally:
      db.session.close()

  except:
    return render_template('errors/500.html'), 500

  # # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
