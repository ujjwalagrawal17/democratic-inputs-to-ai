from django import forms
from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.urls import reverse, NoReverseMatch
from django.utils.html import escape
from django.utils.safestring import mark_safe

from account.models import User, UserProfile


class UserCreationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone', 'name')


class AdminUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = ('phone', 'password', 'is_active', 'name')


class UserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = AdminUserChangeForm
    add_form = UserCreationForm
    date_hierarchy = 'date_joined'

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('phone', 'name', 'is_verified')

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (('Personal info'), {'fields': ('name', 'email')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions', 'is_verified')}),

    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'name', 'password1', 'password2'),
        }),
    )
    search_fields = ('phone',)
    ordering = ('phone',)
    filter_horizontal = ()


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = "action_time"
    readonly_fields = ("action_time",)
    list_filter = ["user", "content_type"]
    search_fields = ["object_repr", "change_message"]
    list_display = ["content_type", "action_time", "user", "object_link"]

    # keep only view permission
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     if obj is None or obj.content_type == "user":
    #         return True
    #     return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = obj.object_repr
        else:
            ct = obj.content_type
            try:
                link = mark_safe(
                    '<a href="%s">%s</a>'
                    % (
                        reverse(
                            "admin:%s_%s_change" % (ct.app_label, ct.model),
                            args=[obj.object_id],
                        ),
                        escape(obj.object_repr),
                    )
                )
            except NoReverseMatch:
                link = obj.object_repr
        return link

    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"

    def queryset(self, request):
        return (
            super(LogEntryAdmin, self)
            .queryset(request)
            .prefetch_related("content_type")
        )


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)

admin.site.unregister(Group)


class ProfileAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('id', 'user', 'flag_aadhar_card_verified')


admin.site.register(UserProfile, ProfileAdmin)
