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


