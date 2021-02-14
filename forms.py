from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField,BooleanField,TextAreaField
from wtforms.validators import DataRequired, AnyOf, URL,Regexp,length

# import enum to implement enum restriction
from enum import Enum

# Genres enum
class Genres(Enum):
    Alternative='Alternative'
    Blues='Blues'
    Classical='Classical'
    Country='Country'
    Electronic='Electronic'
    Folk='Folk'
    Funk='Funk'
    Hip_Hop='Hip-Hop'
    Heavy_Metal='Heavy Metal'
    Instrumental='Instrumental'
    Jazz='Jazz'
    Musical_Theatre = 'Musical Theatre'
    Pop='Pop'
    Punk='Punk'
    R_B='R&B'
    Reggae='Reggae'
    Rock_n_Roll='Rock n Roll'
    Soul='Soul'
    Other='Other'

    # static method to return list from enum
    @staticmethod
    def list():
        return list(map(lambda g: (g.name, g.value), Genres))
# state enum
class States(Enum):
    AL='AL'
    AK='AK'
    AZ='AZ'
    AR='AR'
    CA='CA'
    CO='CO'
    CT='CT'
    DE='DE'
    DC='DC'
    FL='FL'
    GA='GA'
    HI = 'HI'
    ID='ID'
    IL='IL'
    IN='IN'
    IA='IA'
    KS = 'KS'
    KY = 'KY'
    LA = 'LA'
    ME = 'ME'
    MT = 'MT'
    NE = 'NE'
    NV = 'NV'
    NH = 'NH'
    NJ = 'NJ'
    NM = 'NM'
    NY = 'NY'
    NC = 'NC'
    ND = 'ND'
    OH = 'OH'
    OK ='OK'
    OR ='OR'
    MD ='MD'
    MA = 'MA'
    MI = 'MI'
    MN = 'MN'
    MS = 'MS'
    MO = 'MO'
    PA ='PA'
    RI = 'RI'
    SC = 'SC'
    SD = 'SD'
    TN = 'TN'
    TX = 'TX'
    UT = 'UT'
    VT = 'VT'
    VA = 'VA'
    WA = 'WA'
    WV = 'WV'
    WI = 'WI'
    WY = 'WY'


    # static method to return list from enum
    @staticmethod
    def list():
        return list(map(lambda s: (s.name, s.value), States))


class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired(),length(max = 120)]
    )
    state = SelectField(
        'state', validators=[DataRequired(),length(max = 120)],
        choices= States.list()
    )
    address = StringField(
        'address', validators=[DataRequired(),length(max = 120)]
    )
    phone = StringField(
        'phone', validators = [ Regexp(r'^\d{3}-\d{3}-\d{4}$',flags=0, message='Invalid phone number'),DataRequired(),length(max = 120)]

    )
    image_link = StringField(
        'image_link', validators=[length(max = 500)]
    )
    # 
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=Genres.list()
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(),length(max = 120)]
    )
    website = StringField(
        'website', validators=[URL(),length(max = 120)]
    )
    seeking_talent = BooleanField(
        'seeking_talent', default=False
        )
    seeking_description = TextAreaField('seeking_description',validators= [ length(max=500)])

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=States.list()
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone', validators = [ Regexp(r'^\d{3}-\d{3}-\d{4}$',flags=0, message='Invalid phone number'),DataRequired()]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=Genres.list()
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
    )
    website = StringField(
        'website', validators=[URL(),length(max = 120)]
    )
    seeking_venue = BooleanField(
        'seeking_venue', default=False
        )
    seeking_description = TextAreaField('seeking_description',validators= [ length(max=500)])


# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
