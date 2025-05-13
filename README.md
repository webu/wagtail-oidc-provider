# wagtail-oidc-provider

Pairs with [django-oidc-provider](https://github.com/juanifioren/django-oidc-provider/), with wagtail support.

## Install

```
pip install wagtail-oidc-provider
```

Add `wagtail_oidc_provider` to your `INSTALLED_APP`:

```py
INSTALLED_APP = [
    ...
    "oidc_provider",
    "wagtail_oidc_provider",
    ...
]
```

and configuration snippet will popup in the admin navbar of wagtail!
