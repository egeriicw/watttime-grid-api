from django.db import models
from django.db.models.query import QuerySet


class ProvenanceQuerySet(QuerySet):
    def best(self, dp, alg_name):
        """
        Best provenance is determined by balancing authority and timestamp.
        """
        # filter for balancing authority
        qset = self.filter(ba=dp.ba)
        if not qset.exists():
            raise ValueError("No model found for dp %s, nothing matches for ba %s" % (dp, dp.ba.abbrev))

        # filter for algorithm
        qset = self.filter(algorithm__name=alg_name)
        if not qset.exists():
            raise ValueError("No model found for dp %s, nothing matches for algorithm %s" % (dp, alg_name))

        # filter for valid_after
        qset = qset.filter(valid_after__lte=dp.timestamp)
        if not qset.exists():
            raise ValueError("No model found for dp %s valid after timestamp" % (dp))

        # get latest modelset
        row = qset.latest()

        # should have only one value now
        return row


class ProvenanceManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return ProvenanceQuerySet(self.model, using=self._db).all()
