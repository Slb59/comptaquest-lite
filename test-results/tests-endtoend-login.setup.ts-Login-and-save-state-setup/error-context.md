# Page snapshot

```yaml
- main:
  - img "App logo"
  - heading "Connexion" [level=1]
  - paragraph: Vous n'avez pas encore de compte ?
  - paragraph: Veuillez contacter l'administrateur du site
  - text: Identifiant*
  - textbox "Identifiant*": test.user@test.com
  - text: Mot de passe*
  - textbox "Mot de passe*"
  - button "Se connecter"
  - link "Mot de passe oublié ?":
    - /url: /account/password-reset/
  - text: © 2025 Osynia
  - navigation:
    - link "contact":
      - /url: /contact/
```