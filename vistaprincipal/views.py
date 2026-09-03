from django.shortcuts import render


def vistaprincipal(request, perfil=None):
    perfiles = {
        "Adulto Mayor": {
            "nombre": "Adulto Mayor",
            "imagen": "",
            "descripcion": "Consejos claros para estar seguro al usar internet y el telefono móvil, y cómo proteger tu información personal.",
        },
        "Estudiante": {
            "nombre": "Estudiante",
            "imagen": "",
            "descripcion": "Consejos claros para estar seguro al usar internet y el telefono móvil, y cómo proteger tu información personal.",
        },
        "Emprendedor": {
            "nombre": "Profesional",
            "imagen": "",
            "descripcion": "Consejos claros para estar seguro al usar internet y el telefono móvil, y cómo proteger tu información personal.",
        },
    }

    if perfil is not None:
        datos = perfiles.get(perfil)
        if datos:
            return render(request, "templatePrincipal/vistaprincipal.html", {"perfil": datos})

    return render(request, "templatePrincipal/vistaprincipal.html")
