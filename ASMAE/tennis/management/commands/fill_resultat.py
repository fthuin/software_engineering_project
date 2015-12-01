#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from tennis.models import TournoiCategorie, TournoiTitle, Tournoi, Resultat, infoTournoi
import datetime

class Command(BaseCommand):
	def addResult(self):
		#Information sur l'edition 41
		for elem in infoTournoi.objects.filter(edition=41):
			elem.delete()
		i = infoTournoi(prix=20,date=datetime.date(2015, 9, 12),addr="Place des Carabiniers, 5, 1030 Bruxelles",edition=41)
		i.save()

		#Titre 
		TF = TournoiTitle.objects.get(nom="Tournoi des familles")
		DM = TournoiTitle.objects.get(nom="Double mixte")
		DH = TournoiTitle.objects.get(nom="Double hommes")
		DF = TournoiTitle.objects.get(nom="Double femmes")

		list_categorie = ['Pre minimes', 'Minimes', 'Cadets', 'Scolaires', 'Juniors', 'Seniors', 'Elites']
		#Catégorie
		PM = TournoiCategorie.objects.get(nom="Pre minimes")
		MI = TournoiCategorie.objects.get(nom="Minimes")
		CA = TournoiCategorie.objects.get(nom="Cadets")
		SC = TournoiCategorie.objects.get(nom="Scolaires")
		JU = TournoiCategorie.objects.get(nom="Juniors")
		SE = TournoiCategorie.objects.get(nom="Seniors")
		EL = TournoiCategorie.objects.get(nom="Elites")
		TFC = TournoiCategorie.objects.get(nom="Tournoi des familles")

		#Resultats
		#Double Mixte
		t = Tournoi.objects.get(titre=DM, categorie=MI)
		r = Resultat(tournoi=t,gagnants_alt="Julie RYELANDT et Evrard THIJSSEN",finalistes_alt="Lou COURBIAU et Alaric KALISH")
		r.save()
		i.resultats.add(r)

		t = Tournoi.objects.get(titre=DM, categorie=CA)
		r = Resultat(tournoi=t,gagnants_alt="Amandine PRIOUX et Antoine BOONE",finalistes_alt="Chloe OLESEN et Maxime de RIBAUCOURT")
		r.save()
		i.resultats.add(r)

		t = Tournoi.objects.get(titre=DM, categorie=SC)
		r = Resultat(tournoi=t,gagnants_alt="Eleonore BOONEN et Guillaume-Constant CLAES",finalistes_alt="Maroussia Cattoir et Amaury Cattoir")
		r.save()
		i.resultats.add(r)

		t = Tournoi.objects.get(titre=DM, categorie=JU)
		r = Resultat(tournoi=t,gagnants_alt="Anouchka LAURENT JOSI et Antoine de BORREKENS",finalistes_alt="Anouchka LAURENT JOSI et Antoine de BORREKENS")
		r.save()
		i.resultats.add(r)

		t = Tournoi.objects.get(titre=DM, categorie=EL)
		r = Resultat(tournoi=t,gagnants_alt="Julie RYELANDT et Evrard THIJSSEN",finalistes_alt="Lou COURBIAU et Alaric KALISH")
		r.save()
		i.resultats.add(r)

		#Double Femmes
		t = Tournoi.objects.get(titre=DF, categorie=MI)
		r = Resultat(tournoi=t,gagnants_alt="Julie RYELANDT et Lola SCHMID",finalistes_alt="Zoe VERHOOSEL et Alexia JACOB")
		r.save()
		i.resultats.add(r)

		t = Tournoi.objects.get(titre=DF, categorie=CA)
		r = Resultat(tournoi=t,gagnants_alt="Antoinette ADAM et Victorine ADAM",finalistes_alt="Agathe DE MOL et Louise-Marie DUPREZ")
		r.save()
		i.resultats.add(r)


		t = Tournoi.objects.get(titre=DF, categorie=SC)
		r = Resultat(tournoi=t,gagnants_alt="Delphine SPRUYTTE et Ludivine D'YDEWALLE",finalistes_alt="Juliette DAVIGNON et Charlotte-Lucie DELBECQUE")
		r.save()
		i.resultats.add(r)


		t = Tournoi.objects.get(titre=DF, categorie=JU)
		r = Resultat(tournoi=t,gagnants_alt="Laura DECLETY et Sophie GOFFAU",finalistes_alt="Alexia KASTEEL et Louise MONVILLE")
		r.save()
		i.resultats.add(r)

		#Double Hommes
		t = Tournoi.objects.get(titre=DH, categorie=MI)
		r = Resultat(tournoi=t,gagnants_alt="Arnaud DAVIGNON et Hidde DOMS",finalistes_alt="Alexis MENCIK et Jules RAEMDONCK")
		r.save()
		i.resultats.add(r)

		t = Tournoi.objects.get(titre=DH, categorie=CA)
		r = Resultat(tournoi=t,gagnants_alt="Quentin DAVIGNON et Alexandre VERHULST",finalistes_alt="Diego TIELENS et Alexandre de STAERCKE")
		r.save()
		i.resultats.add(r)

		t = Tournoi.objects.get(titre=DH, categorie=SC)
		r = Resultat(tournoi=t,gagnants_alt="Charles le GRELLE et Martin van der MEERSCHEN",finalistes_alt="François DAVID et Antoine LEGRAND")
		r.save()
		i.resultats.add(r)

		t = Tournoi.objects.get(titre=DH, categorie=JU)
		r = Resultat(tournoi=t,gagnants_alt="Augustin BOSSAERT DERACHE et Diego MOMMAERTS",finalistes_alt="Felix de PATOUL et Nicolas van HAVRE")
		r.save()
		i.resultats.add(r)

		t = Tournoi.objects.get(titre=DH, categorie=EL)
		r = Resultat(tournoi=t,gagnants_alt="Olivier MARTINOT et Didier PERWEZ",finalistes_alt="Philippe DE BRUYNE et Alain VERGAUWEN")
		r.save()
		i.resultats.add(r)

		#Tournoi des familles
		t = Tournoi.objects.get(titre=TF, categorie=TFC)
		r = Resultat(tournoi=t,gagnants_alt="Guillaume van LINT et Eric van LINT",finalistes_alt="Briac LOHEST et Emmanuel LOHEST")
		r.save()
		i.resultats.add(r)

		i.save()

	def handle(self, *args, **options):
		print("Ajout des resultats de 2015")
		self.addResult()