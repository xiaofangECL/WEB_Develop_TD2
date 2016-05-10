# Q5-4.py

import socketserver

from datetime import datetime
from pytz import timezone
import pytz
import os

# on adhère aux conventions françaises
import locale
locale.setlocale(locale.LC_ALL, 'french')

#
# Définition du nouveau handler
#
from server import generic 

class RequestHandler(generic.RequestHandler):

  # on utilise le nom de fichier pour identifier le serveur
  server_version = os.path.basename(__file__)+'/0.1'


  #
  # On surcharge la méthode qui traite les requêtes GET
  #
  def do_GET(self):

    # on initialise nos variables d'instance
    self.init_vars()
    
    # le chemin d'accès commence par /time
    if self.path_info[0] == 'time':
      self.send_time()

    # ou pas...
    else:
      self.send_static()


  #
  # On crée la méthode qui traite les requetes POST
  #
  def do_POST(self):

    # on initialise nos variables d'instance
    self.init_vars()

    if self.path_info[0] == 'time':
      self.send_time()
    else:
      self.send_error(405)


  #
  # On envoie un document avec l'heure
  #
  def send_time(self):

    # on récupère le fuseau horaire demandé
    tz_name = '/'.join(self.path_info[1:]) if len(self.path_info) > 1 else self.params['timezone'][0]
    try:
      tz = timezone(tz_name)
    except(pytz.exceptions.UnknownTimeZoneError):
      self.send_error(400,'Unknown Time Zone')
      return

    # on récupère la date et l'heure
    time = datetime.utcnow()

    # on convertit vers le fuseau demandé
    tz_time = tz.normalize(pytz.utc.localize(time).astimezone(tz))

    # on génère le style
    style = ''
    for k in self.params:
      if k and not k == 'timezone':
        style = style + '{}:{};'.format(k,self.params[k][0])
        
    # on génère un document
    body = '<!doctype html>' + \
           '<meta charset="utf-8">' + \
           '<title>l\'heure dans le fuseau {}</title>'.format(tz_name) + \
           '<pre>Voici la date et l\'heure UTC du serveur :\n\n' + \
           '<span style="{}">{}</span>\n\n'.format(style,time.strftime('%A %d %B %Y, %H:%M:%S')) + \
           'Dans le fuseau {} il est :\n\n'.format(tz_name) + \
           '<span style="{}">{}</span></pre>'.format(style,tz_time.strftime('%A %d %B %Y, %H:%M:%S'))

    # on envoie
    self.send(body)

 
#
# Instanciation et lancement du serveur
#
httpd = socketserver.TCPServer(("", 8080), RequestHandler)
httpd.serve_forever()
