# Canevas v0.16 — tentative de dérivation de la mesure

## But

Tester si la mesure de distinguabilité utilisée en v0.13–v0.15 peut être motivée à partir des axiomes du Canevas, sans utiliser les valeurs observées de zeta ou Lambda.

## Axiomes de départ (version minimale)

A1. L'existence est nécessaire; le néant absolu n'est pas un état physique privilégié.

A2. Le Canevas ne possède pas d'observateur extérieur ni de point de vue absolu privilégié.

A3. Les univers/états possibles doivent être décrits intrinsèquement; changer seulement les coordonnées utilisées pour les nommer ne doit pas changer leur poids physique.

A4. Les observateurs sont des structures locales internes au Canevas; aucune occurrence particulière de "moi" n'est fondamentale.

A5. Les expériences physiques sont finies et locales: deux univers qui ne produisent aucune différence physique accessible dans un ensemble donné de relations/observables ne doivent pas être distingués simplement parce que leurs paramètres ont des étiquettes numériques différentes.

A6. La mesure n'est pas autorisée à contenir explicitement les valeurs observées dans notre univers.

## Ce qui découle réellement

### 1. Invariance de reparamétrisation

Si theta et phi=f(theta) décrivent les mêmes univers, la probabilité d'une même région physique doit être la même. Donc une densité p(theta) dtheta n'a pas de sens absolu si elle n'est pas accompagnée d'une règle de transformation.

Cela élimine l'idée qu'une densité "plate" dans une coordonnée choisie arbitrairement soit fondamentale.

### 2. Une distance doit être relationnelle

A2–A5 suggèrent que la distance entre univers doit dépendre de différences physiques prédites, non de la distance euclidienne entre leurs paramètres.

Soit un vecteur de prédictions intrinsèques O(theta). Pour un petit déplacement dtheta,

    dO = J dtheta

avec J le Jacobien des prédictions. La forme quadratique minimale construite localement à partir de ces changements est

    ds^2 = dtheta^T J^T W J dtheta,

avec W une métrique positive sur l'espace des observables.

La densité de volume associée est

    dmu(theta) ∝ sqrt(det(J^T W J)) d^n theta.

Cette densité est invariante sous changement régulier de coordonnées dans l'espace des paramètres, car le déterminant et l'élément de volume se compensent.

## Ce qui NE découle PAS encore

Le Canevas minimal ne détermine pas W.

Autrement dit, les axiomes suggèrent une famille de mesures de distinguabilité, mais pas encore une mesure unique. Choisir W=I, comme dans les premiers tests numériques, est une hypothèse supplémentaire.

Cela est crucial: le résultat numérique de v0.15 ne peut pas être présenté comme une prédiction dérivée tant que W n'est pas fixé indépendamment.

## Tentative de fermeture de W

Trois principes supplémentaires possibles, à tester séparément:

P1. **Isotropie informationnelle** — aucune direction d'observable intrinsèque n'est privilégiée. Dans des coordonnées observationnelles orthonormales, W ∝ I.

P2. **Bruit opérationnel** — W doit être l'inverse de la covariance d'une expérience/observation idéale, menant à une métrique de type Fisher.

P3. **Compression minimale** — W est défini par une représentation minimale/suffisante des prédictions, afin d'éviter le double comptage d'observables corrélées.

Aucun de ces principes n'est actuellement un axiome du Canevas. Ils représentent des extensions falsifiables.

## Conclusion v0.16

Résultat théorique provisoire:

- Les axiomes du Canevas donnent un argument non trivial en faveur de l'invariance de reparamétrisation et d'une notion relationnelle de distance entre univers.
- Sous l'hypothèse supplémentaire qu'une mesure locale est construite uniquement à partir des variations infinitésimales d'un vecteur de prédictions physiques, la forme naturelle est une métrique de pullback J^T W J.
- La mesure testée numériquement en v0.15 correspond au cas particulier W=I.
- W=I n'est PAS encore dérivé.

Le prochain test décisif ne consiste donc pas à ajouter d'autres paramètres cosmologiques, mais à vérifier si la typicalité observée survit à des choix de W définis indépendamment: identité, whitening/covariance, sous-espaces de prédictions, et compression des observables.

Si le résultat disparaît sous ces choix raisonnables, la mesure de distinguabilité est fragile. S'il reste stable, on obtient une classe de mesures plus robuste, mais toujours pas une preuve des axiomes philosophiques.
