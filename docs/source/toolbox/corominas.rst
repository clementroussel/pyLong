Modèle de Corominas
===================

.. image:: ../icones/lave.png
   :align: center
   :scale: 75%
   
|

Principe
--------

Le modèle de Corominas (1996) est basé sur l'analyse de 204 glissements de terrain majoritairement survenus dans la partie est espagnole des Pyrénées suite à des pluies très intenses survenues pendants l'hiver 1982.
Les glissements retenus ont été classifiés avec la classification de Varnes (1978) en 4 groupes dont deux concernent les laves torrentielles:

- Gr iii: "Earthflows, mudflows and mudslides" correspondent à des laves boueuses composées de matériaux fins (limons et argiles);
- Gr iv: "Debris flows, debris slides, and debris avalanches" correspondant à des laves torrentielles avec des matériaux grossiers.

L'analyse a également été conduite en prenant en compte différentes configurations d'écoulements:

- (a) "unobstructed": correspondant à des écoulements non chenalisés progressant sans obstacles ou contractions, ou écoulements progressant dans une forêt ouverte;
- (b) "channelized": écoulements dans un chenal torrentiel;
- (c) "obstructed": catégorie incluant des écoulements avec changements de direction > 60°, écoulements dans une forêt dense ou écoulement dont l'extension est limitée par la présence de la paroi de la vallée opposée qui génère une séparation de l'écoulement dans 2 directions opposée (confluences).

Les relations recherchées, qui établissent un lien entre l'angle de parcours :math:`\frac{H}{L}` et le volume de la lave :math:`V`, sont du type:

.. math::

   log \left(\frac{H}{L}\right) = b \times log(V) + a \leftrightarrow \frac{H}{L} = 10^{a} \times V^{b}

On retrouve donc comme dans la pratique des chutes de blocs et de mouvements gravitaires, le concept de ligne d'énergie, celle-ci étant ici liée au volume de lave.

Le tableau suivant récapitule les valeurs des coefficients de régression :math:`r^2` pour chaque groupe et configuration d'écoulement analysée (:math:`N` étant le nombre d'évènements dans l'échantillon).

+--------------+----+--------+--------+-----------+
| Groupe       | N  |    a   |    b   |:math:`r^2`|
+==============+====+========+========+===========+
| Debris flows |    |        |        |           |
+--------------+----+--------+--------+-----------+
| All          | 71 | -0.012 | -0.105 |   0.763   |
+--------------+----+--------+--------+-----------+
| Obstructed   | 29 | -0.049 | -0.108 |   0.849   |
+--------------+----+--------+--------+-----------+
| Channelized  | 19 | -0.077 | -0.109 |   0.690   |
+--------------+----+--------+--------+-----------+
| Unobstructed | 18 | -0.031 | -0.102 |   0.868   |
+--------------+----+--------+--------+-----------+
| Mud flows    |    |        |        |           |
+--------------+----+--------+--------+-----------+
| All          | 17 | -0.214 | -0.070 |   0.648   |
+--------------+----+--------+--------+-----------+
| Unobstructed | 8  | -0.220 | -0.138 |   0.908   |
+--------------+----+--------+--------+-----------+

Calcul d'une lave torrentielle avec le modèle de Corominas
----------------------------------------------------------

**Paramètres** à renseigner :

- un profil en long;
- l'abscisse de départ;
- le volume;
- le pas de calcul;
- un modèle d'écoulement.

Si le calcul réussi, les coordonnées du point **d'arrivée** sont mises à jour.

.. note::
   - la notion de **départ** correspond au point de plus haute altitude;
   - la notion **d'arrivée** correspond au point de plus basse altitude.
