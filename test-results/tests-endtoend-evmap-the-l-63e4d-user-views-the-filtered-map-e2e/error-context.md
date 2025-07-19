# Page snapshot

```yaml
- main:
  - link "Profile":
    - /url: /account/profile/
    - img "Profile"
  - link "Tableau de bord":
    - /url: /
    - img "Tableau de bord"
  - link "EscapeVault":
    - /url: /escapevault/map/
    - img "EscapeVault"
  - img "App logo"
  - heading "EscapeVault Map" [level=1]
  - link "Liste des positions":
    - /url: /escapevault/list/
    - img "Liste des positions"
  - link "Nouvelle position":
    - /url: /escapevault/add/
    - img "Nouvelle position"
  - link "Paramètres":
    - /url: /escapevault/parameters/
    - img "Paramètres"
  - text: Catégorie
  - combobox "Catégorie":
    - option "Toutes"
    - option "Maison" [selected]
    - option "Nomade"
    - option "Coup de coeur"
    - option "Ordinaire"
    - option "À bannir"
  - img
  - text: "Make this Notebook Trusted to load map: File -> Trust Notebook"
  - iframe
  - text: © 2025 Osynia
  - navigation:
    - link "contact":
      - /url: /contact/
```