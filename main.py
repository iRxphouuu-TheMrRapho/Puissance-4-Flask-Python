import flask
import game
from flask import Flask
from flask_socketio import SocketIO, send, emit

games = game.Games()
app = Flask(__name__)
socket = SocketIO(app)


# Handler d'api rest pour la page par défaut du site
@app.route('/')
def home():
    return flask.render_template('home.html')


# Handler d'api rest, la page play est le hub du jeu
# Soit le joueur attend son adversaire
# Soit l'adversaire fait la requete depuis la page
@app.route('/play')
def play():
    game_ = game.get_game(flask.request.args.get("id"), games)

    if game_ is None or game_.is_pending:
        return flask.render_template('play.html')

    return flask.render_template('playing.html')


# Handler d'api rest utilisé lorsque un utilisateur fait une demande de duel
@app.route('/create_game')
def create_game():
    game_ = game.Game()
    game_.print_info()
    games.list_.append(game_)
    return str(game_.id01)


clients = {}


# Objet qui stoque les donnés d'un navigateur ( id du joueur, l'id de sa partie et si il est en jeu)
class Client:
    def __init__(self, user_sid, in_game):
        self.game_id = None
        self.user_sid = user_sid
        self.in_game = in_game


# Fonction utile pour recuperer un joueur par son id du jeu
def get_client_by_game_id(game_id):
    for key, value in clients.items():
        if value.game_id == game_id:
            return value
    return None


# Fonction utile pour recuperer un joueur par son id du jeu qui fonctionne que si la partie est lancé
def get_client_by_game_id_in_game(game_id):
    for user_id, client in clients.items():
        if client.game_id == game_id and client.in_game:
            return client
    return None


# Socket reçu lorsque le joueur accepte l'invitation de duel
@socket.on('connect')
def handle_connect(auth):
    user_id = flask.request.remote_addr + ":" + str(
        flask.request.environ.get('REMOTE_PORT'))
    clients[user_id] = Client(flask.request.sid, False)


# Socket envoyé par le navigateur lorsque l'un des deux joueurs se déconnecte
@socket.on('disconnect')
def handle_disconnect():
    user_id = flask.request.remote_addr + ":" + str(
        flask.request.environ.get('REMOTE_PORT'))
    clients.pop(user_id, None)


# Socket envoyés au 2 joueurs pour lancer la partie
@socket.on('play')
def handle_play(id_):
    user_id = flask.request.remote_addr + ":" + str(
        flask.request.environ.get('REMOTE_PORT'))
    game_ = game.get_game(id_, games)

    if game_ is None:
        emit("play", "state=0")
    elif game_.is_pending and game_.id01 == id_:
        clients[user_id].game_id = id_
        emit("play", "state=1")
        emit("play", "shared_id=" + str(game_.id02))
    elif game_.is_pending and game_.id02 == id_:
        clients[user_id].game_id = id_
        emit('play', "reload", to=get_client_by_game_id(game_.id01).user_sid)
        emit('play', "reload")
        game_.is_pending = False


## Playing est le socket reçu lorsque le joueur clique sur une case
## Il y a donc un test pour savoir si tout est valide
@socket.on('playing')
def handle_playing(id_):
    user_id = flask.request.remote_addr + ":" + str(
        flask.request.environ.get('REMOTE_PORT'))
    game_ = game.get_game(id_, games)

    if game_ is None:
        emit("playing", "state=0")
    elif not game_.is_pending and game_.id01 == id_:
        clients[user_id].game_id = id_
        emit("playing", "state=1")
        emit("playing", "map=" + game_.map_)
        emit("playing", "player=" + str(1))
        emit("playing", "turn=" + str(game_.turn))
        clients[user_id].in_game = True
    elif not game_.is_pending and game_.id02 == id_:
        clients[user_id].game_id = id_
        emit("playing", "state=1")
        emit("playing", "map=" + game_.map_)
        emit("playing", "player=" + str(2))
        emit("playing", "turn=" + str(game_.turn))
        clients[user_id].in_game = True


## Socket renvoyé au 2 joueurs a chaque fois qu'un des deux joue pour actualiser leurs tableau et checker la victoire
@socket.on('playing2')
def handle_playing2(data_):
    splited = str(data_).split("=")
    game_ = game.get_game(splited[0], games)
    player = 0

    if game_.id01 == splited[0]:
        player = 1
    elif game_.id02 == splited[0]:
        player = 2

    if game_.add_column(int(splited[1]), player):
        game_.print_info()
        print("player ", player, " places to ", splited[1])
        print(
            emit('playing2',
                 "player=" + str(player) + "=" + splited[1],
                 to=get_client_by_game_id_in_game(game_.id01).user_sid))
        print(
            emit('playing2',
                 "player=" + str(player) + "=" + splited[1],
                 to=get_client_by_game_id_in_game(game_.id02).user_sid))

        print("win1: ", game_.verify_win(1))
        print("win2: ", game_.verify_win(2))

        if game_.verify_win(1):
            emit('playing2',
                 "win=" + str(1),
                 to=get_client_by_game_id_in_game(game_.id01).user_sid)
            emit('playing2',
                 "win=" + str(1),
                 to=get_client_by_game_id_in_game(game_.id02).user_sid)
            return
        elif game_.verify_win(2):
            emit('playing2',
                 "win=" + str(2),
                 to=get_client_by_game_id_in_game(game_.id01).user_sid)
            emit('playing2',
                 "win=" + str(2),
                 to=get_client_by_game_id_in_game(game_.id02).user_sid)
            return

        game_.switch_turn()
        emit("playing2",
             "turn=" + str(game_.turn),
             to=get_client_by_game_id_in_game(game_.id01).user_sid)
        emit("playing2",
             "turn=" + str(game_.turn),
             to=get_client_by_game_id_in_game(game_.id02).user_sid)
    else:
        print("player ", player, " can't place to ", splited[1])


# Run l'application flask
if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port=11111)
