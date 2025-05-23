from hashlib import sha224
from random import randint
from uuid import uuid4

from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from oidc_provider.models import Client
from oidc_provider.models import Code
from oidc_provider.models import RSAKey
from oidc_provider.models import Token
from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import HelpPanel
from wagtail.admin.panels import MultiFieldPanel
from wagtail.admin.panels import ObjectList
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.snippets.views.snippets import SnippetViewSetGroup


class ClientForm(ModelForm):
    class Meta:
        model = Client
        exclude = []

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields["client_id"].required = False
        self.fields["client_id"].widget.attrs["disabled"] = "true"
        self.fields["client_secret"].required = False
        self.fields["client_secret"].widget.attrs["disabled"] = "true"

    def clean_client_id(self):
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            return instance.client_id
        else:
            return str(randint(1, 999999)).zfill(6)

    def clean_client_secret(self):
        instance = getattr(self, "instance", None)

        secret = ""

        if instance and instance.pk:
            if (self.cleaned_data["client_type"] == "confidential") and not instance.client_secret:
                secret = sha224(uuid4().hex.encode()).hexdigest()
            elif (self.cleaned_data["client_type"] == "confidential") and instance.client_secret:
                secret = instance.client_secret
        else:
            if self.cleaned_data["client_type"] == "confidential":
                secret = sha224(uuid4().hex.encode()).hexdigest()

        return secret


class ClientViewSet(SnippetViewSet):
    model = Client
    icon = "globe"

    client_panels = [
        MultiFieldPanel(
            children=[
                FieldPanel("name"),
                FieldPanel("owner"),
                FieldPanel("client_type"),
                FieldPanel("response_types"),
                FieldPanel("_redirect_uris"),
                FieldPanel("jwt_alg"),
                FieldPanel("require_consent"),
                FieldPanel("reuse_consent"),
            ],
            heading="",
        ),
        MultiFieldPanel(
            children=[
                FieldPanel("client_id"),
                FieldPanel("client_secret"),
                FieldPanel("_scope"),
            ],
            heading=_("Credentials"),
        ),
        MultiFieldPanel(
            children=[
                FieldPanel("contact_email"),
                FieldPanel("website_url"),
                FieldPanel("terms_url"),
                FieldPanel("logo"),
                FieldPanel("date_created", read_only=True),
            ],
            heading=_("Information"),
        ),
        MultiFieldPanel(
            children=[
                FieldPanel("_post_logout_redirect_uris"),
            ],
            heading=_("Session Management"),
        ),
    ]
    edit_handler = ObjectList(client_panels, base_form_class=ClientForm)

    list_display = ["name", "client_id", "response_type_descriptions", "date_created"]
    search_fields = ["name"]


class CodeViewSet(SnippetViewSet):
    model = Code
    icon = "cogs"

    inspect_view_enabled = True


class TokenViewSet(SnippetViewSet):
    model = Token
    icon = "cogs"

    inspect_view_enabled = True


class RSAKeyViewSet(SnippetViewSet):
    model = RSAKey
    icon = "key"

    panels = [
        FieldPanel("key"),
        HelpPanel(
            heading="Kid", template="wagtailadmin/wagtail_oidc_provider/panels/kid_panel.html"
        ),
    ]


class OidcProviderGroup(SnippetViewSetGroup):
    menu_label = "OpenID connect provider"
    menu_icon = "resubmit"
    menu_order = 120
    items = (ClientViewSet, CodeViewSet, TokenViewSet, RSAKeyViewSet)


register_snippet(OidcProviderGroup)
