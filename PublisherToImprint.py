# PublisherToImprint.py
# A plugin script for ComicRack
# (c) 2017 Bryn Mosher (BadMonkey0001)
# GPL v3 License
################################################################################

import clr
import System
import re

clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import *

scriptOutputPrefix = "[PublisherToImprint] "
scriptWindowTitle = "Publisher To Imprint"
rgxAllWhitespaceOrEmpty = re.compile("^\s*$")

#@Name	Publisher To Imprint
#@Hook	Books
#@Description Publisher To Imprint: If the Imprint is blank, put the Publisher name in if available.
#@Image PublisherToImprint.png
def PublisherToImprint(books):
	stats = {
		'bookCount': 0,
		'skipped': 0,
		'emptyPub': 0,
		'imprintExisted': 0,
		'processed': 0,
	}

	if books:
		# needs a confirmation box here

		for book in books:
			stats['bookCount'] += 1
			identifier = getIdentifier(book)
			publisher = getPublisherFromBook(book)

			if publisher:
				log("Found book to process \""+identifier+"\".")

				imprint = getImprintFromBook(book)
				if imprint:
					stats['imprintExisted'] += 1
					stats['skipped'] += 1
					log("Book already has an imprint of \""+imprint+"\" for \""+identifier+"\".")
					continue

				book.Imprint = publisher
				stats['processed'] += 1
				log("Processed \""+book.Imprint+"\" for \""+identifier+"\".")

			else:
				stats['emptyPub'] += 1
				stats['skipped'] += 1
				log("Book \""+identifier+"\" has an empty Publisher. Skipping.")

		showResults(stats)
	else:
		MessageBox.Show("You don't have any books selected.\n\nPlease select at least one book.", scriptWindowTitle, MessageBoxButtons.OK, MessageBoxIcon.Information)

def showResults(stats):
	outStringList = []
	outStringList.append("Finished processing books. Here are the results.")
	outStringList.append("\n")
	outStringList.append("Overall Summary")
	outStringList.append("----------------------------------------")
	outStringList.append("Total Books Examined: "+str(stats['bookCount']))
	outStringList.append("Total Books Processed: "+str(stats['processed']))
	outStringList.append("\n")
	outStringList.append("Skipped Books Summary")
	outStringList.append("----------------------------------------")
	outStringList.append("Total: "+str(stats['skipped']))
	outStringList.append("Imprint Existed: "+str(stats['imprintExisted']))
	outStringList.append("Publisher Empty: "+str(stats['emptyPub']))
	outStringList.append("\n")

	MessageBox.Show("\n".join(outStringList), scriptWindowTitle, MessageBoxButtons.OK)

def getIdentifier(book):
	idStirng = "";

	if book.Series and not rgxAllWhitespaceOrEmpty.match(book.Series):
		idStirng = book.Series.strip()

	if not idStirng and book.ShadowSeries and not rgxAllWhitespaceOrEmpty.match(book.ShadowSeries):
		idStirng = book.ShadowSeries.strip()

	if not idStirng:
		return book.FilePath

	if book.Number and not rgxAllWhitespaceOrEmpty.match(str(book.Number)):
		idStirng += " #"+str(book.Number)
	elif book.ShadowNumber and not rgxAllWhitespaceOrEmpty.match(str(book.ShadowNumber)):
		idStirng += " #"+str(book.ShadowNumber)

	return idStirng

def getPublisherFromBook(book):
	if book.Publisher and not rgxAllWhitespaceOrEmpty.match(book.Publisher):
		return book.Publisher.strip()

	return ""

def getImprintFromBook(book):
	if book.Imprint and not rgxAllWhitespaceOrEmpty.match(book.Imprint):
		return book.Imprint.strip()

	return ""

def log(msg):
	print scriptOutputPrefix+msg

