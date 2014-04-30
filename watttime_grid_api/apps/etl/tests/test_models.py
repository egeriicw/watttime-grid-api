from django.test import TestCase
from apps.etl.models import ETLJob
from django.core import mail


class TestJob(TestCase):
    def test_minimal_create(self):
        ETLJob.objects.create()

    def test_dates(self):
        job = ETLJob.objects.create()

        # created and updated are same up to microseconds
        self.assertIsNotNone(job.created_at)
        self.assertEqual(job.created_at.replace(microsecond=0), job.updated_at.replace(microsecond=0))

        # modify
        old_update = job.updated_at
        job.args = 'test'
        job.save()

        # has updated
        self.assertLess(old_update, job.updated_at)

    def test_success(self):
        # default success is False
        job = ETLJob.objects.create()
        self.assertFalse(job.success)

    def test_error(self):
        # set error
        job = ETLJob.objects.create()
        msg = 'test'
        job.set_error(msg)

        # error is set
        self.assertEqual(job.errors, msg)

        # error sends email
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(msg, mail.outbox[0].body)
