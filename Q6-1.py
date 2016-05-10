# Q6-1.py

# pour le serveur web
import socketserver

# pour la gestion des noms de fichiers
import os

# pour l'accès base de données
import sqlite3


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

    # le chemin d'accès commence par /lignes
    if self.path_info[0] == 'lignes':
      self.send_trains()
    
    # ou pas...
    else:
      self.send_static()
    

  #
  # On envoie un document avec la liste des lignes
  #
  def send_trains(self):

    conn = sqlite3.connect('sncf.sqlite')
    c = conn.cursor()
    c.execute("SELECT DISTINCT c.hexadecimal, p.code_ligne, p.nom_ligne " +\
              "FROM ponctualite_transilien AS p, couleur_transilien as c " +\
              "WHERE c.code_ligne = p.code_ligne " +\
              "ORDER BY p.code_ligne")
    r = c.fetchall()

    header = '<tr><td colspan=2>code</td><td>ligne</td><tr>'
    rows = ['<tr><td style="background-color: {}">&nbsp;</td><td>{}</td><td>{}</td></tr>'.format(*a) for a in r]
    html = '<table>{}\n{}</table>'.format(header,'\n'.join(rows))

    self.send(html)


#
# Instanciation et lancement du serveur
#
httpd = socketserver.TCPServer(("", 8080), RequestHandler)
httpd.serve_forever()
