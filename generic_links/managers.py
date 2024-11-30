from django.db import models


class GenericLinkQuerySet(models.QuerySet):
    def internal(self):
        return self.exclude(is_external=True)

    def external(self):
        return self.filter(is_external=True)
