Modèle de Rickenmann
====================

.. image:: ../icones/lave.png
   :align: center
   :scale: 75%
   
|

Principe
--------

De nombreux travaux de recherché ont mis en évidence un lien entre la distance de parcours des laves torrentielles et le volume mobilisé (Corominas, 1996 ; Schilling et Iverson, 1997 ; Rickenmann, 1999, 2005).

Sur la base de l’analyse d’environ 160 évènements survenus en Suisse en 1987, Rickenmann (1999) a établi une un modèle de régression (:math:`r^{2} = 0.75`) liant la distance de parcours maximale de laves torrentielles :math:`L_{max}` au volume :math:`V` et à la différence d’élévation entre le point de départ et le point d’arrêt :math:`H_e`:

.. math::

   L_{max} = 1.9 \times V^{0.16} \times H_{e}^{0.83}

Les évènements sur lesquels se base la régression ont les caractéristiques suivantes:

- :math:`300\,m \le L \le 12 600\,m`;
- :math:`700\,m^3 \le V \le 106\,m^3`;
- :math:`110\,m \le H \le 1 820\,m`. 

D’après l’analyse du graphique montrant la droite de régression obtenue et la distribution du nuage de points correspondant aux laves survenues en Suisse en 1987 on déduit l’équation de type courbe enveloppe donnant la distance maximale de propagation:

.. math::

   L_{max} = 6.0 \times V^{0.16} \times H_{e}^{0.83}

Calcul d'une lave torrentielle avec le modèle de Rickenmann
-----------------------------------------------------------

**Paramètres** à renseigner:

- un profil en long;
- l'abscisse de départ;
- le volume;
- le pas de calcul.

Si le calcul réussi, les coordonnées du point **d'arrivée** sont mises à jour.

.. note::
   - la notion de **départ** correspond au point de plus haute altitude;
   - la notion **d'arrivée** correspond au point de plus basse altitude.
