# Rapport Application BI

## Préparation des données

### Exploration

### Nettoyage

### Fusion

### Recodage

### Prétraitement

### Découpage

## Méthodes de classification

### Sélection

### Apprentissage

### Comparaison

### Raffinage

### Évaluation

### Interprétation

## Implémentation

### Le conflit sociétaire -> démissionnaire VS démissionnaire -> sociétaire

#### La source :

Les données sociétaires et démissionnaires n'ont pas les mêmes colonnes, démissionnaire en a plus, dont certaines qui sont sous des formats assez spéciaux.

- Yacine a dit:
  - on cherche a voir si des sociétaires risquent de devenir démissionnaires, donc on fait l'analyse sur des sociétaires donc on traite les démissionnaires comme des sociétaires.
- Jérémie a dit:
  - on cherche a voir si des sociétaires risquent de devenir démissionnaires, donc on transforme les sociétaires en démissionnaires et on voit si leur situation fait sens par rapport aux démissionnaires déjà existants.

#### Arguments pour démissionnaire -> sociétaire

- Pcq yacine a dit qu'il avait raison et que moi je dis de la merde.

#### Arguments pour sociétaire -> démissionnaire

- Les démissionnaires possèdent plus de donnés catégorielles, pouvant nous permettre de faire des clusterings avec les catégories proposées.
- Il est facile de transformer un sociétaire en démissionnaire grâce aux données de sociétaire.

### 