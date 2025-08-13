from django.utils.translation import gettext_lazy as _

SAMI_DESCRIPTIONS = {
    "bedtime": _("Heure du coucher (0: > 23h, 3: 22h-23h, 2: 21h-22h, 1: <21h)"),
    "wakeup": _(
        "Heure de réveil (0: < 5h30, 3: 5h30-7h30, 2: 7h30-8h00, 1: 8h00-9h00, 0: >9h00)"
    ),
    "nonstop": _("Temps non stop (0: < 4h00, 1: 4h00-5h00,")
    + _("2: 5h00-6h00, 3: 6h00-7h00,")
    + _("5: 7h00-8h00, 2: 8h00-10h00, 0: >10h00)"),
    "energy": _("Forme (5: je fais plein de chose, je ne suis pas fatiguée,")
    + _(
        "1:je ne pleure pas mais je me lutte contre la fatigue toute la journée, 0:dépression)"
    ),
    "naptime": _("Sieste (4: 15-20 mn, 2: < 15mn, 2: 20mn-1h, 0: > 1h)"),
    "phone": _("Telephone (2: absence, 1: Présence, 0: présence et usage)"),
    "reading": _(
        "Lecture (3: > 30mn,2: <30mn concentrée, 1: <30mn non concentrée, 0: si absence)"
    ),
    "total_sleep": _("Total Sommeil : maxi 25"),
    "fruits": _("1 par fruit, maxi 3"),
    "vegetables": _("1 par légume, maxi 2"),
    "meals": _(
        "selon la qualité du plat, +1 s'il y a au moins 3 ingrédients différents,"
    )
    + _("+1 s'il y a des légumes, -3 s'il y a des pâtes ou du pain"),
    "desserts": _("0 si le dessert est trop calorique (chocolat ou gâteau),")
    + _("+2 ou +3 s'il est fait maison, +1 s'il est léger (yaourt)"),
    "sugardrinks": _("0 si il est trop calorique (coca),")
    + _(
        "-2 si c'est du sirop, -2 si sucre ajouté (dans le thé ou le café par exemple)"
    ),
    "nosugardrinks": _("+1 par verre"),
    "total_food": _("Total Alimentation : maxi 25"),
    "homework": _("5 si > 2h, 4 si entre 1h et 2h, 3 si 30mn-1h, 2 si < 30mn"),
    "garden": _(
        "5 si > 2h,  4 si entre 1h et 2h, 3 si 30mn-1h, 2 si < 30mn,   0 sinon"
    ),
    "outsidetime": _("5 si > 3h ,4 si entre 2 et 3h, 3 entre 1 et 2h, 0 sinon"),
    "endurancesport": _(
        "Natation-course-velo: 5 si > 1h ,4 si entre 30mn et 1h ,2 si <30mn, 0 si rien"
    ),
    "yogasport": _("Yoga-musculation,5 si >1h ,4 si >30mn ,2 si < 30mn ,0 sinon"),
    "total_move": _("Total Mouvement : maxi 25"),
    "videogames": _("5 >1h30, 3: entre 1h30 et 2h, 2 si 0, 0 sinon"),
    "papergames": _(
        "5 si entre 2 et 3h ,4 si entre 1 et 2h ou > 3h ,3 si < 1h, 0 si > 3h"
    ),
    "administrative": _(
        "5 si entre 2 et 3h ,4 si entre 1 et 2h ou > 3h ,3 si < 1h, 0 si > 3h"
    ),
    "computer": _("5 si entre 4 et 5h ,3 si > 5 ,4 si entre 2 et 4h ,3 si 1 à 2h"),
    "youtube": _("5 si < 1h ,3 si entre 1h et 2h ,0 si > 2h"),
    "total_idea": _("Total idées : maxi 25"),
    "total_sami": _("Total Sami : maxi 100"),
}
