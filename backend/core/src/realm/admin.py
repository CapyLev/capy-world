from django.contrib import admin

from .models import Server, ServerMember


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "admin",
        "name",
        "description",
        "created_at",
    )
    search_fields = (
        "id",
        "name",
    )
    date_hierarchy = "created_at"
    readonly_fields = (
        "id",
        "created_at",
    )


@admin.register(ServerMember)
class ServerMemberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "server",
        "user",
        "created_at",
    )
