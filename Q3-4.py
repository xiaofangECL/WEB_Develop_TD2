# Q3-4.py

import http.server
import socketserver

# définition du nouveau handler
class RequestHandler(http.server.SimpleHTTPRequestHandler):

  # sous-répertoire racine des documents statiques
  static_dir = '/client'

  # on surcharge la méthode qui traite les requêtes GET
  def do_GET(self):
    self.send_static()

  # on surcharge la méthode qui traite les requêtes HEAD
  def do_HEAD(self):
    self.send_static()

  # on envoie le document statique demandé
  def send_static(self):

    # on modifie le chemin d'accès en insérant un répertoire préfixe
    self.path = self.static_dir + self.path

    # on calcule le nom de la méthode parent à appeler (do_GET ou do_HEAD)
    # à partir du verbe HTTP (GET ou HEAD)
    method = 'do_{}'.format(self.command)
    
    # on traite la requête via la classe parent
    getattr(http.server.SimpleHTTPRequestHandler,method)(self)

    
# instanciation et lancement du serveur
httpd = socketserver.TCPServer(("", 8080), RequestHandler)
httpd.serve_forever()
