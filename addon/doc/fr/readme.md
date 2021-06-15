# Manuel de zUtilidades

zUtilidades vise à être un ensemble de petites applications pour NVDA.

Nous allons essayer d'ajouter des applications qui peuvent être intéressantes afin que nous puissions les consulter rapidement et que à son tour, soit faciles à gérer et clair dans son interface.

zUtilidades aura un menu dans Outils de NVDA, Dans ce menu ils seront ajoutés les différents modules.

Chaque module est préparé afin que nous puissions ajouter un raccourci allant dans le menu NVDA / Préférences /  Gestes de commandes dans la catégorie zUtilidades.

Par défaut, les modules viendront sans raccourci attribué.

Par conséquent, nous pouvons démarrer les modules en allant dans le menu Outils / zUtilidades ou en attribuant une combinaison de touches pour chaque module.

Il est actuellement composé des modules suivants:

* Lanceur d'applications.

# Module Lanceur d'applications

Ce module nous permettra rapidement et à partir de n'importe quelle partie de notre ordinateur lancer une application portable ou installé.

## Écran principal

L'écran principal consiste en une liste de catégories, une liste d'applications et un bouton Menu.

Si nous faisons Tabulation nous passerons à travers les différents zones.

### Liste des catégories

Dans cette zone, nous pouvons ajouter, modifier ou supprimer une catégorie, pouvant trier à notre goût et par catégories nos applications.

Nous pouvons accéder aux options Ajouter, Modifier ou Supprimer de deux manières.

Lorsque nous sommes dans la zone Catégories en appuyant sur la touche Application ou si nous n'avons pas la  touche Maj+F10, un menu sera affiché où nous pouvons choisir l'une des 3 options.

Les dialogues tantot pour ajouter comme pour modifier sont très simples disposant d'un seul champ de édition où nous pouvons mettre le nom de la nouvelle catégorie ou modifier la catégorie que nous avons choisie, deux boutons, OK et Annuler.

Si nous choisissons de supprimer, nous devons prendre en compte que le contenu de cette catégorie sera complètement effacée sans pouvoir refaire l'action, soyez donc prudent  car nous pourrons perdre les applications Que nous avons  dans la base de données et nous devrons re-entrez toutes les applications ou les commandes ou les accès à cette catégorie.

Nous pouvons également accéder à ces options en cliquant sur le bouton Menu, lorsque nous faisons Tabulation ou avec la combinaison Alt+M. Si nous le faisons, un menu sera affiché avec un sous-menu appelé Catégories où nous pouvons choisir l'une des 3 options précédentes.

Notez que Modifier et Supprimer seront toujours dans la catégorie qui a le focus, donnant les messages correspondants si nous n'avons pas de catégories.

Nous pouvons également utiliser les combinaisons de touches Alt + Flèche  haut et Flèche  bas pour déplacer la catégorie pour pouvoir les trier.

### Liste des applications

Dans cette zone, c'est où les applications correspondantes à la catégorie que nous avons choisies seront placées.

Nous avons 3 options qui son Ajouter une action, Modifier une action ou Supprimer une action.

Nous pouvons obtenir ces options comme dans la liste des catégories soit avec la touche Applications ou dans se cas Maj+F10 ou accédez au bouton Menu (Alt+M) et chercher le sous-menu Applications.

Dans cette liste d'applications, nous pouvons lancer l'application qui a le focus en appuyant sur la barre d'espace.

Nous pouvons également utiliser les combinaisons de touches Alt + Flèche  haut et Flèche  bas  pour déplacer  l'entrée pour pouvoir les trier.

Dans cette zone, nous pouvons rapidement naviguer dans les différentes entrées, en appuyant sur la première lettre, afin que nous puissions trouver rapidement l'application que nous souhaitons exécuter si nous en avons beaucoup dans la base de données.

#### Menu Ajouter une action

Dans ce menu, nous pouvons choisir entre les options suivantes:

* Ajouter une application:

	Si nous ajoutons une application, il existe deux champs obligatoires et c'est le nom de l'application et le répertoire dans lequel notre application est située.

Actuellement, cette extension prend en charge les applications avec les extensions exe, bat et com.

Une fois que les champs obligatoires sont remplis, nous pouvons choisir si l'application nécessite des paramètres supplémentaires ou si nous voulons exécuter l'application en mode administrateur.

Si nous voulons exécuter une application en mode administrateur, on nous demandera l'autorisation correspondante lorsque nous démarrons l'application.

* Ajouter une commande CMD

Dans ce dialogue, nous pouvons ajouter des commandes de console.

Les champs nom pour identifier la commande et le champ commandes sont obligatoires.

Dans ce cas, en plus de lancer des commandes CMD, si nous maîtrisons Windows PowerShell, si nous mettons PowerShell en ligne de commande et suivi de ce que nous voulons, nous allons également exécuter des commandes PowerShell.

De même, si son des commandes CMD j'ajoute que nous pouvons exécuter plusieurs lignes de commande qui doivent être séparées par le symbole (et commercial) pouvant être effectuées avec  Maj+6, ceci avec un clavier QWERTY espagnol. Si un clavier QWERTY anglais est utilisé, Cela sera effectué avec Maj+7.

Par exemple, j'ai mis une ligne de commande pour redémarrer Windows Explorer, vous vérifierez que j'utilise le symbole (et commercial) pour séparer une ligne de commande de l'autre.

`taskkill /f /im explorer.exe & start explorer`

En outre, dans ce dialogue, nous pouvons mettre une pause de sorte que la console ne se ferme pas et nous pouvons voir les résultats.

Nous pouvons également exécuter en tant qu'administrateur.

* Ajouter des accès aux dossiers

Dans ce dialogue, nous devrons choisir un nom pour identifier l'accès au dossier et choisir un dossier.

Cela nous permettra d'ouvrir rapidement des dossiers de notre système de n'importe où.

* Ajouter Exécuter des raccourcis de Windows

Dans ce dialogue, nous pouvons choisir un raccourci pour le démarrer. Nous pouvons également choisir si nous voulons le démarrer en tant qu'administrateur.

Les champs pour identifier le nom du raccourci et le chemin sont obligatoires.

* Ajouter une application installée

Dans ce dialogue, toutes les applications installées sur notre ordinateur seront obtenues par l'utilisateur ou sont des applications qui sont déjà livrées avec Windows.

Également sur cet écran, nous pouvons choisir les applications installées à partir du Microsoft Store de Windows.

AVERTISSEMENT ceci n'est pas valide pour Windows 7.

Une fois qu'une application est ajoutée à partir de ce dialogue, notez qu'il ne peut pas être modifié, alors nous devrons supprimer l'entrée si nous voulons l'ajouter à nouveau.

L'option Exécuter en tant qu’administrateur dans ce dialogue ne fonctionnera pas pour toutes les applications. Fonctionnant uniquement pour celle qui vous permettent d'utiliser des privilèges d'administrateur.

Notez également que dans ce dialogue, les accès installés par les applications apparaissent également dans la zone de liste déroulante, nous pouvons les sélectionner, mais certains ne sont pas autorisés d'être ouvert, donnant une erreur.

Notez également que vous devez faire attention car dans cette liste, apparaîtront des applications qui peut être pour administrer ou des applications pour la gestion Que si nous ne savons pas à quoi servent il vaut mieux ne pas les toucher.

#### Modifier une action

Le dialogue Modifier est exactement le même que le dialogue Ajouter une action Mais cela nous permettra de modifier l'entrée que nous choisissons.

Cela nous permettra de modifier tous les éléments, à l'exception de ceux qui ont été ajoutés par l'option  Ajouter une application installée, Les dialogue seront identiques que dans les options pour ajouter.

#### Supprimer une action

Si nous supprimons une entrée, nous devons garder à l'esprit que l'action ne sera pas réversible.

### Bouton Menu

Ce bouton sera accessible depuis n'importe quelle partie de l'interface en appuyant sur la combinaison  Alt+M.

Dans ce menu, nous trouverons quatre sous-menus qui sont  Catégories, Actions, Faire ou restaurer une sauvegarde et Options, dans ce menu nous trouvons aussi l'option Quitter.

Eh bien,  Catégories et Actions que j'ai expliquées auparavant, je n'expliquerai que le sous-menu Faire ou restaurer une sauvegarde et Options.

Eh bien, si nous choisissons Faire  une sauvegarde, une fenêtre d'enregistrement de Windows s'ouvre où nous devrons choisir où enregistrer notre sauvegarde de la base de données.

Par défaut, le nom du fichier est plus ou moins comme ceci:

`Backup-03052021230645.zut-zl`

Eh bien, l'extension est configurée par défaut et le nom correspond au module et contient la date à laquelle il a été créé, mais nous pouvons mettre le nom que nous souhaitons.

Une fois enregistré, nous pouvons la restaurer si notre base de données est corrompue ou tout simplement si celle-ci est supprimée par erreur ou nous souhaitons revenir à une version que nous avons précédemment enregistrée.

Si nous choisissons Restaurer une sauvegarde, une fenêtre Windows classique s'ouvrira, pour nous permettre d'ouvrir les fichiers respectifs.

Nous devons choisir la copiie que nous avons enregistrée qui aura l'extension *.zut-zl , veillez à ne pas modifier l'extension car sinon vous ne trouverez pas le fichier.

Une fois que vous avez choisi, la sauvegarde sera restaurée et lorsque nous  avons appuyer sur  OK l'extension sera fermé  et la prochaine fois que nous l'ouvrons, il aura notre copie restaurée.

Notez que les fichiers *.zut-zl sont en réalité des fichiers compressés, mais faites attention lorsque vous les modifiez, si elles sont modifiées, la signature ne correspondra pas et ne leur permettra pas d'être restaurer.

Avec cela, je tiens à dire que ces fichiers apportent une signature qui ne correspond pas au moment de la restauration, cela donnera une erreur et chaque signature est différente pour chaque fichier.

Dans le sous-menu Options maintenant il n'y a que l'option Réinitialiser le lanceur d'applications aux valeurs par défaut.

Si nous choisissons cette option, toute la base de données sera supprimée, laissant  l'extension comme s'il était nouvellement installé.

## Raccourcis clavier

Dans les deux zones, Catégories et Applications, nous pouvons trier les entrées avec:

* Alt + Flèche  haut ou Flèche bas

Lorsqu'une catégorie ou une application atteint le début ou la fin de la liste, cela sera annoncé avec un son distinct pour savoir que nous ne pouvons pas ni monter ni descendre plus.

* Alt + C: Ça va nous amener rapidement à la zone des catégories.

* Alt + L: Ça va nous amener rapidement à la liste des applications.

* Alt + M: Cela nous ouvrira le menu.

* Touche Applications ou Maj + F10: Dans les zones des catégories et applications nous déploierons le menu contextuel avec des options.

* Espace: Dans la zone liste des applications s'exécutera l'application qui a le focus.

* Echap: Ferme tous les dialogues que l'application peut ouvrir même l'écran principal du lanceur d'applications, laissant le focus depuis l'endroit où elle a été appelée.

## Observations de l'auteur

Prenez garde sur diverses choses, la première que le lanceur d'applications se fermera lorsque nous exécuterons une application, devant l'appeler à nouveau lorsque nous voulons exécuter une  autre.

Il a également été implémenté une fonction qui sauvegardera la position de la catégorie et les dernières applications visitées, alors lorsque nous ouvrons le lanceur d'applications, la dernière catégorie et la dernière application de cette catégorie seront toujours choisies.

Aussi il a été implémenté la sauvegarde du focus, alors lorsque nous appelons le lanceur d'applications, il nous laissera toujours dans la dernière position où le focus a était mis  avant de fermer.

Par exemple,  si le focus est mis sur le bouton  Menu et nous fermons le lanceur d'applications, la prochaine fois que nous l'ouvrons, le focus sera mis sur le bouton Menu.

Ces caractéristiques ne sont valables que lors de la session de NVDA, cela signifie que si nous redémarrons NVDA on va démarrer avec le focus mis dans la zone catégories.

Cette extension a été faite pour être utilisée avec Windows 10, de sorte que si vous utilisez des versions antérieures et que vous avez  un problème quelconque vous pouvez me le dire, mais je ne peux sûrement rien faire car certaines fonctionnalités ne sont trouvées que dans Windows 10.

## Traducteurs et contributeurs:

* Français: Rémy Ruiz
* Portugais: Ângelo Miguel Abrantes

# Journal des changements.
## Version 0.1.6.

* Ajout de la traduction française et Portugaise (Portugal / Brésil).

## Version 0.1.5.

* Menus restructurés.

Ajoutez la possibilité d'ajouter:

* Ajouter une commande CMD

* Ajouter des accès aux dossiers

* Ajouter Exécuter des raccourcis de Windows

* Ajouter une application installée

* Ajouté dans le bouton Menu la possibilité  dans Options Réinitialiser le lanceur d'applications aux valeurs par défaut

* Différentes erreurs ont été corrigées avec la base de données.

* Des erreurs internes ont été corrigées.

* L'extension a été préparée afin  d'être traduite.

## Version 0.1.

* Module Lanceur d'applications ajouté.

* Version initiale.

