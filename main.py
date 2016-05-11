#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import jinja2
import webapp2



from models import Gosti

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")


class RezultatHandler(BaseHandler):
    def post(self):
        ime_osebe = self.request.get("polje_ime")
        priimek_osebe = self.request.get("polje_priimek")
        email_osebe = self.request.get("polje_email")
        sporocilo_osebe = self.request.get("polje_sporocilo")


        if ime_osebe == "":
            ime_osebe == "neznanec"

        if priimek_osebe == "":
            priimek_osebe == "neznanec"

        if sporocilo_osebe =="":
            sporocilo_osebe = self.request.get("polje_sporocilo")


        sporocilo = Gosti(ime=ime_osebe, priimek=priimek_osebe, email=email_osebe, sporocilo=sporocilo_osebe)
        sporocilo.put()



class SeznamSporocilHandler(BaseHandler):
    def get(self):
        seznam = Gosti.query().fetch()
        izhodni_podatki = {"trenutni_vnosi": seznam}
        return self.render_template("seznam_sporocil.html", params=izhodni_podatki)

class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Gosti.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        return self.render_template("posamezno_sporocilo.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/seznam-sporocil', SeznamSporocilHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>', PosameznoSporociloHandler)
], debug=True)