from google.appengine.ext import ndb

class Gosti(ndb.Model):
    ime = ndb.StringProperty()
    priimek = ndb.StringProperty()
    email = ndb.StringProperty()
    sporocilo = ndb.TextProperty()
    nastanek = ndb.DateTimeProperty(auto_now_add=True)