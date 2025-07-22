class TooltipFromInstanceMixin:
    """
    Mixin qui ajoute un attribut `title` à chaque champ d'un formulaire
    en combinant le help_text et l'attribut {field_name}_description de l'instance.
    """

    def set_tooltips_from_instance(self):
        for field_name, field in self.fields.items():
            help_text = field.help_text or ""
            description_attr = f"{field_name}_description"
            description = getattr(self.instance, description_attr, "")
            combined = help_text
            if description:
                combined = f"{help_text}\n{description}" if help_text else description
            if combined:
                field.widget.attrs["title"] = combined
                field.help_text = None
