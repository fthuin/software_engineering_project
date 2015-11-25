from django.core.management.base import BaseCommand
from tennis.models import Participant, Ranking
from django.contrib.auth.models import User
import datetime
import random

RES_FILE = "res.csv"

list_rankings = ["NC", "C30.5", "C30.4", "C30.3", "C30.2", "C30.1", "C30", "C15.5", "C15.4", "C15.3", "C15.2", "C15.1", "C15", "B+4/6", "B+2/6", "B0"]

class Command(BaseCommand):
    help = 'this method will populate the db with the participants of res.csv'

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
                latitude = items[10]
                longitude = items[11]
                classement = Ranking.objects.get(nom=random.choice(list_rankings))
                print(username)
                user = User.objects.create_user(username, email, mdp)
                user.save()
                participant = Participant(user=user, titre = "Mme", nom=nom, prenom=prenom, rue=rue, numero=numero, boite="", codepostal=code, localite=ville, telephone="", fax="", gsm=telephone, classement=classement, oldparticipant=random.choice([False, True]), datenaissance=datenaissance, latitude=latitude, isClassementVerified=random.choice([True, False]), longitude=longitude).save()

    def handle(self, *args, **options):
        self._create_participants()
