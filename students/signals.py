# -*- coding: utf-8 -*-
import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from models import Student

@receiver(post_save, sender=Student)
#write info about added/updated student in log file
def log_student_updated_added_event(sender, **kwargs):

	logger = logging.getLogger(__name__)

	student = kwargs['instance']
	if kwargs ['created']:
		logger.info("Student added: %s %s (ID: %d)", student.first_name, student.last_name, student.id)
	else:
		logger.info("Student updated: %s %s (ID: %d)", student.first_name, student.last_name, student.id)


@receiver(post_delete, sender=Student)
#write info about deleted student in log file
def log_student_deleted_event(sender, **kwargs):
	logger = logging.getLogger(__name__)

	student = kwargs['instance']
	logger.info("Student deleted: %s %s (ID: %d)", student.first_name, student.last_name, student.id)
	