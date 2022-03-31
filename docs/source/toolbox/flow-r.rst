Modèle Flow-R
=============

.. image:: ../icones/lave.png
   :align: center
   :scale: 75%
   
|

Principe
--------

FLOW-R est un modèle SIG développé par l’université de Lausanne (Horton. Et al., 2013) permettant la modélisation à large échelle de la propagation de laves torrentielles. FLOW-R couple un algorithme d'étalement avec un algorithme de propagation. On décrit ici le modèle de propagation qui fait l'hypothèse, comme pour les mouvements de masse (écroulements, chutes de blocs), que la distance peut être approchée par une modélisation de la ligne d'énergie. L'originalité réside ici dans le fait que l'angle de la ligne est modulé en faisant l'hypothèse d'une vitesse maximale possible des laves torrentielles (cf. figure suivante).
La conservation de l'énergie s'écrit entre deux points 1 et 2 le long du profil en long:

.. math::

   \Delta E_{TOT} = \left( E_{cin,1} + E_{pot,1} \right) - \left( E_{cin,2} + E_{pot,2} \right) = j

où :math:`\Delta E_{TOT}` représente la variation d'énergie totale, :math:`E_{cin}` la composante d'énergie cinétique, :math:`E_{pot}` la composante d'énergie potentielle et :math:`j` les pertes de charges liées aux frottements.

La distance maximale de propagation est déterminée par intersection de la ligne d’énergie avec le terrain naturel. En fixant de manière arbitraire la vitesse au niveau de la zone de départ, la vitesse peut être déterminée en chaque point du profil en long avec l’équation suivante:

.. math::

   V_{i} = min \left\{ \sqrt{ V_{i-1}^2 + 2.g.\Delta z - 2.g.\Delta x.tan{\varphi}}, V_{max} \right\}

Avec: :math:`V_i` la vitesse au nœud de calcul :math:`i`, :math:`V_{i-1}` la vitesse au nœud de calcul :math:`i-1`, :math:`\Delta x` la distance séparant les nœuds calcul :math:`i` et :math:`i-1`, :math:`\Delta z` la différence d’altitude  entre les nœuds :math:`i-1` et :math:`i` et  :math:`\tan \varphi` la pente de la ligne d’énergie, et :math:`V_{max}` la vitesse maximale des laves.

L’originalité de cette méthode est la limitation du terme d’énergie cinétique obtenue sur la base d’une vitesse maximale admissible de laves torrentielles.

Pour des laves torrentielles, en s’appuyant sur des travaux Rickenmann et Zimmermann (1993), Bathurst(1997) et Huggel (2002), les auteurs indiquent un angle de ligne d’énergie :math:`\varphi` minium de 11°. Cette valeur semble adaptée pour des laves à forte proportion de matériaux grossiers (coarse and medium-grained debris flows). D’après Zimmermann, cet angle est susceptible de chuter à 7° pour des matériaux plus fins (matrice argileuse prépondérante) et où les matériaux grossiers dans le front sont moins nombreux. 

On retrouve donc des valeurs d’angles de ligne d’énergie égaux ou inférieurs à ceux observés sur des débâcles glaciaires. L’utilisation d’une limitation de la vitesse maximale a pour effet de réduire la distance de parcours.


On notera que le modèle de propagation ne dépend pas du volume de l’évènement.

.. image:: ../images/flowr.png
   :align: center
   :scale: 100%

Calcul d'une lave torrentielle avec un modèle de type Flow-r
------------------------------------------------------------

**Paramètres** à renseigner:

- un profil en long;
- l'abscisse de départ;
- l'angle d'énergie;
- la vitesse initiale;
- la vitesse maximale;
- le pas de calcul.

Si le calcul réussi, les coordonnées du point **d'arrivée** sont mises à jour.

.. note::
   - la notion de **départ** correspond au point de plus haute altitude;
   - la notion **d'arrivée** correspond au point de plus basse altitude.
