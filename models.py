from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# --------------------Venue Model------------------
class Venue(db.Model):
  __tablename__ = 'Venue'
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

  shows = db.relationship('Show', backref='Venue', lazy=True,cascade="all, delete, delete-orphan")

  def __repr__(self):
    return "<Venue(venue id='%s', name='%s', city='%s', genres='%s')>" % (self.id, self.name, self.city,self.genres)
  

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
# --------------------Artist Model---------------------
class Artist(db.Model):
  __tablename__ = 'Artist'
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

  shows = db.relationship('Show', backref='Artist', lazy=True,cascade="all, delete, delete-orphan")

  def __repr__(self):
    return "<Artist(artist id='%s', name='%s', city='%s')>" % (self.id, self.name, self.city)

# ------------------Show Model---------------------
class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
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
  
