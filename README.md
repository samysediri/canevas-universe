# Canevas Universe

Projet expérimental visant à transformer certains axiomes philosophiques du **Canevas** en hypothèses quantitatives testables en cosmologie.

## Principe de travail

On sépare strictement :

1. les axiomes philosophiques ;
2. les hypothèses physiques ajoutées ;
3. les calculs numériques ;
4. les observations utilisées pour comparer le modèle ;
5. les conclusions réellement supportées.

Le projet ne considère jamais une correspondance numérique comme une preuve du Canevas. Une connexion devient intéressante seulement si elle survit à des changements raisonnables de modèle sans être recalibrée sur la valeur observée.

## Test actuel : CLASS v0.9.2

Objectif : remplacer l'ancienne approximation du spectre de matière par **CLASS** et vérifier si l'optimum trouvé pour

`zeta = rho_CDM / rho_b`

reste du même ordre de grandeur que la valeur observée (~5.39).

Le protocole garde fixes `h`, la densité totale de matière, `A_s` et `n_s`, puis fait varier seulement la répartition baryons/CDM.

La version v0.9.2 est tolérante aux erreurs : une cosmologie refusée par CLASS est enregistrée comme telle et le scan continue.

## Exécution Windows

Prérequis déjà utilisés :

```powershell
python -m pip install numpy classy-community
```

Puis lancer :

```text
LANCER_CANEVAS_CLASS.bat
```

Les résultats sont écrits dans `results/`.

## Statut scientifique

- Énergie noire : effet sur la formation des structures cohérent, mais valeur observée non expliquée.
- Matière noire/baryons : résultat semi-analytique intéressant autour de zeta ~ quelques unités, à tester maintenant avec CLASS.
- Higgs : pas encore testé.
- Vie/conscience : pas simulées.
- Mesure P(U) du Canevas : problème théorique majeur encore ouvert.
