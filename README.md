Ce projet est un Puissance4 créé par Gabriel et Raphaël.

Ce puissance 4 est jouable en un contre un a distance via un site web, codé en JavaScript, en Python et en Html/Css.

Le principe est simple, le joueur 1 créer un lien en se connectant sur le site web. Il l'envoie au joueur 2 qui en se connectant, lance la partie. Le premier joueur a aligner 4 jetons de sa couleur gagne la partie.

La partie serveur, fait en python grâce a flask, s'occupe de la gestion des parties, vérifie si les joueurs gagnent et represente le relais entre les deux clients. La partie client, fait en html, en css et en javascript avec axios, gère l'ui du projet ainsi que la communication avec le serveur.

Le seul fichier externe utilisé est le fichier html de ce puissance 4 que nous avons en plus modifié par la suite : https://codepen.io/defeo/pen/emPevV

Répartition des Taches
Nous avons réfléchis au fonctionnement du jeu ensemble, mais Raphael s'est ensuite occupé du moteur de calcul de la victoire, ainsi que de l'ui. Gabriel s'est occupé quant a lui de la connection serveur-client en socket, de la rest api avec flask et de la partie en javascript.

Etapes de Réalisations
Nous avons commencer par la partie html, afin de pouvoir nous representer le projet a faire par la suite, que ce soit les boutons ou les textes et leurs couleurs. Gabriel a fait des fonctions basique representant ce qu'il fallait remplir pour envoyer au client suivi de pass. Ensuite, Raphael a développé l'ensemble du systeme de victoire et Gabriel s'est occupé du cache des parties. Après ça, nous avons fait la partie JS qui permet de rendre la page web dynamique. Cette partie envoie au serveur les informations lorsque le joueur clique par exemple. Pour rendre cette partie esthétique mais aussi efficace, nous avons terminé par l'écriture du css avec TailwindCSS, en choisissant un thème orienté autour du bleu. Enfin, nous avons fait une partie de test ou nous avons réglé les derniers bugs d'affichage et procédé au derniers ajouts afin de parfaire le jeu.

Fonctionnement du serveur web
Tout les utilisateurs arrivent par défaut sur la page / nommé home. L'utilisateur peut faire une requete pour créer une partie et recevoir un lien. Ce lien est l'id unique de son adversaire. Le joueur est redirigé vers une page d'attente nommé play, le temps qu'il envoie a son adversaire le lien. Lorsque celui ci clique dessus, une requete socket est envoyé au serveur nommé play ou il y est indiqué l'id du joueur. La partie se lance alors. Lorsqu'un joueur clique, il envoie une requete playing qui défini ou il clique. Les deux joueurs reçoivent en échange un socket playing2 ou il y est indiqué si le coup est validé ainsi que le coup en question. La page affiche alors le coup. En cas de victoire, tout s'arrete, la victoire est aussi indiqué dans ce packet.

Fonctions notables
En plus des descriptions directements implémentés dans pythons, voici quelques fonctions notables :

game.py#verify_win(self, player) Qui prend en paramètre le joueur qui a posé le dernier jeton, et qui renvoie un boolean : si il a gagné ou non. app.py#handle_playing(data_) Qui prend en paramètre les donnée reçu du client, cette fonction s'execute lorsque le joueur clique sur une case depuis son navigateur. app.py#home() Fonction initial, elle est executé lorsque un joueur se connecte sur la page web principale

Installation
Le projet requière Python en version 3.10.2 Le projet requiere les différentes dépendencies suivantes :

simple-web-socket (version 0.5.1)
flask (version 2.0.3)
flask-socketio (version 5.1.1)
markupsafe (version 2.1.0)
random (version compatible avec Python 3.10.2)
Après avoir executé le fichier nommé app.py, suivez les instructions et cliquer sur le lien affiché sur la console.
