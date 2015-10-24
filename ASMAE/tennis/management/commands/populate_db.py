from django.core.management.base import BaseCommand
from tennis.models import Participant
from django.contrib.auth.models import User
import datetime

RES_FILE = "res.csv"

class Command(BaseCommand):
    help = 'this method will populate the db with 100 participants'

    def _create_participants(self):
        with open(RES_FILE, "r") as file:
            data_read = file.read()
            data_read = data_read.split("\n")
            data_read.pop()
            for data in data_read:
                items = data.split(",")
                name = items[0].split(" ")
                nom = name[1]
                prenom = name[0]
                rue = items[1]
                numero = items[2]
                code = items[3]
                ville = items[4]
                telephone = items[5]
                date = items[6]
                date2 = date.split("/")
                datenaissance = datetime.datetime(int(date2[2]),int(date2[1]),int(date2[0]))
                email = items[7]
                username = items[8]
                mdp = items[9]
                user = User.objects.create_user(username, email, mdp)
                user.save()
                participant = Participant(user=user, titre = "Mr", nom=nom, prenom=prenom, rue=rue, numero=numero, boite="", codepostal=code, localite=ville, telephone="", fax="", gsm=telephone, classement="", oldparticipant=False, datenaissance=datenaissance).save() 

    def handle(self, *args, **options):
        self._create_participants()

