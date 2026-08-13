# Canevas v0.12 — Dériver une mesure P(U) sans regarder notre Univers

## Question

Le Canevas affirme, dans sa forme actuelle, qu'un ensemble très large voire infini de configurations physiques est réalisé. Pour transformer cela en prédictions, il faut une règle de pondération `P(U)`.

Cette règle ne doit **pas** être choisie parce qu'elle rend notre Univers typique. Elle doit découler d'un principe indépendant.

## Axiomes utilisés ici

On ne présuppose que les idées philosophiques déjà présentes dans le Canevas :

1. l'existence est fondamentale ;
2. le Canevas n'a pas de point de vue extérieur privilégié ;
3. aucune identité individuelle n'est fondamentale ou privilégiée ;
4. les expériences conscientes accessibles sont locales et finies ;
5. l'ensemble global peut être infini et contenir une multiplicité de réalisations.

Ces axiomes imposent des contraintes de symétrie, mais ils ne fournissent pas encore à eux seuls une métrique unique sur l'espace des lois physiques.

---

## Résultat théorique principal de v0.12

### Les axiomes actuels ne déterminent pas une mesure unique.

Dire « toutes les possibilités existent » ne dit pas combien chaque région de l'espace des possibilités doit compter.

Mathématiquement, une densité uniforme dépend du choix de coordonnée. Par exemple, si `x>0` :

- une mesure uniforme en `x` est `dμ ∝ dx` ;
- une mesure uniforme en `log x` est `dμ ∝ dx/x`.

Elles ne sont pas équivalentes.

Il faut donc un principe additionnel qui précise ce que signifie « deux variations également grandes » dans l'espace des univers.

---

## Candidat A — symétrie additive

Si un paramètre `x` possède une origine et une échelle physiquement définies et si aucune valeur additive n'est privilégiée, la mesure de Haar de la translation est

`dμ ∝ dx`.

C'est la logique d'un prior plat.

### Limite

Ce principe dépend du choix d'un paramètre qui se comporte réellement comme une coordonnée additive fondamentale.

---

## Candidat B — symétrie multiplicative / absence d'échelle

Pour un paramètre strictement positif `x`, si aucune échelle multiplicative n'est privilégiée, on exige l'invariance sous

`x -> a x`.

La mesure correspondante est

`dμ ∝ dx/x = d(log x)`.

Elle est uniforme en nombre d'ordres de grandeur plutôt qu'en unités linéaires.

### Application naturelle à zeta

`zeta = rho_CDM/rho_b` est un rapport positif et sans dimension.

Si l'espace préalable des rapports ne privilégie aucune échelle de zeta, un candidat naturel est

`P(zeta) d zeta ∝ d zeta / zeta`.

Cette mesure est également compatible avec l'inversion `zeta -> 1/zeta` : elle traite symétriquement les deux directions sur l'axe `log zeta`.

Attention : les baryons et la matière noire ne sont pas physiquement interchangeables. Cette symétrie serait une symétrie de la **coordonnée préalable des rapports**, pas une symétrie de leurs interactions.

---

## Candidat C — mesure par distinguabilité physique

Le candidat conceptuellement le plus intéressant pour le Canevas est différent.

Au lieu de demander quelle coordonnée est « uniforme », on peut demander :

> Deux univers devraient-ils compter comme deux possibilités distinctes uniquement dans la mesure où ils produisent des prédictions physiquement distinguables ?

Cela conduit naturellement à une géométrie de l'espace des modèles. Une construction standard en statistique utilise l'information de Fisher :

`dμ_J(theta) ∝ sqrt(det I(theta)) dtheta`.

Cette mesure est invariante sous un changement régulier de coordonnées des paramètres.

### Pourquoi cela peut faire écho au Canevas

Le Canevas insiste sur des expériences locales et finies plutôt que sur une étiquette extérieure absolue des univers. Une hypothèse supplémentaire possible serait donc :

> **Axiome de distinguabilité : le poids élémentaire dans l'espace des possibilités est défini par les différences observables entre configurations, et non par une coordonnée humaine arbitraire.**

Ce n'est PAS encore un axiome contenu dans le Canevas. C'est une proposition à tester.

Si on l'adopte, elle fournit une voie beaucoup plus objective vers `P(U)` que « plat » ou « log-plat » choisis à la main.

---

## Candidat D — pondération des observateurs / moments d'observation

L'absence d'identité privilégiée suggère qu'une prédiction conditionnée par l'existence d'observateurs devrait aussi spécifier une règle de localisation parmi les occurrences d'observateurs.

Une possibilité minimale est une pondération égale par occurrence d'un type défini d'« observer-moment » fini.

Mais dans un Canevas infini, cela réintroduit immédiatement un problème de régularisation : `∞/∞` ne définit pas une fréquence. De plus, la définition d'un observer-moment n'est pas actuellement fournie par les axiomes.

Conclusion : l'axiome de non-privilège de l'identité contraint la mesure, mais ne la termine pas.

---

# Falsification / règles anti-ajustement

Les règles suivantes sont verrouillées avant toute nouvelle comparaison cosmologique :

1. Aucun prior ne sera déclaré « mesure du Canevas » parce qu'il rapproche une prédiction de notre Univers.
2. Le prior log-flat sur un paramètre positif n'est admissible que si une symétrie multiplicative indépendante est défendue.
3. Le prior plat n'est admissible que si une structure additive indépendante est défendue.
4. La mesure de distinguabilité/Fisher sera testée comme **nouvelle hypothèse**, et non présentée comme conséquence déjà démontrée des axiomes.
5. Toute mesure impropre (par exemple `dx/x` sur `(0,∞)`) doit recevoir des bornes ou une régularisation dérivées indépendamment ; la sensibilité à ces bornes doit être publiée.
6. Une mesure doit être évaluée simultanément sur plusieurs paramètres (`zeta`, `Lambda`, puis d'autres) : aucune mesure ne sera retenue sur un seul succès.

---

# Conclusion de v0.12

Le résultat le plus important n'est pas encore une formule de `P(U)`.

C'est l'identification d'une lacune précise :

> **Le Canevas actuel ne possède pas encore un principe de métrique/distinguabilité sur l'espace des possibilités.**

Sans ce principe, plusieurs mesures incompatibles respectent les axiomes généraux.

Le prochain test pertinent est donc de comparer trois familles pré-déclarées :

- mesure additive ;
- mesure multiplicative ;
- mesure de distinguabilité (Fisher/Jeffreys).

On cherchera surtout à savoir si la troisième peut être définie à partir de prédictions cosmologiques calculables par CLASS sans introduire les valeurs observées dans sa construction.
