from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from students.models import Student, Group, Exam

class Command(BaseCommand):
	args = '<model_name model_name ...>'
	help = "Prints to console number of student related objects in a database."

	models = (('student', Student), ('group', Group), ('exam', Exam), ('user', User))

	def handle(self, *args, **options):
		for name, model in self.models:
			self.stdout.write('Number of %ss in database: %d' %
				(name, model.objects.count()))