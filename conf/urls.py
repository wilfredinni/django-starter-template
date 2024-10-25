from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path


# TODO 👇 Delete the index view, route and template.
def index(request):
    base_url = (
        "https://github.com/wilfredinni/django-starter-template?tab=readme-ov-file"
    )
    context = {}
    context["version"] = "0.1.2"
    context["buttons"] = [
        {"title": "🚀 Features", "url": f"{base_url}#key-features"},
        {"title": "📋 Requirements", "url": f"{base_url}#requirements"},
        {"title": "🛠️ How to use it", "url": f"{base_url}#how-to-use"},
    ]
    return render(request, "index.html", context)


urlpatterns = [
    #
    #  TODO⚡ Change the admin url to one of your choice.
    # Please avoid using the default 'admin/' or 'admin-panel/'
    path("admin-panel/", admin.site.urls, name="admin"),
    #
    # TODO ⚡ Disable the auth endpoints you don't need.
    # Enabled: create, profile, login, logout, logoutall
    path("auth/", include("apps.users.urls")),
    path("core/", include("apps.core.urls")),
    path("", index),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
