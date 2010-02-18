#!/usr/bin/env python

#
#	Looks at the output of the file command
#		e.g. find /media/WINDOWS/ -exec file --mime-type '{}' \;
#
#	or better:
#		find /media/WINDOWS/ -type f -print0 | xargs -0 file --mime-type 
#
#	and checks that the extensions match the values in the file mimetypes.txt
#		which is a set of mimetypes downloaded from the internet.
#		Found by searching for "file extension" and mimetype
#

from optparse import OptionParser
from collections import defaultdict
import sys

parser = OptionParser()

(options, args) = parser.parse_args()

#
#	First build up the dictionary so that exts[ext] returns a list of valid mimetypes for this extension
#		that is exts['xml'] will return a list of valid mimetimes for the 'xml' extension
#
exts = defaultdict(list)

for line in open("mimetypes.txt"):
	fields = line.split()
	if len(fields) == 2 :
		# Extract the extension and the mimetype from the line
		ext, mimetype = fields
		ext = ext[1:]	# lose the first character (a dot)
		exts[ext].append(mimetype) # Add this mimetype to this extension

#
#	This should be the output from the find command, a filename and mimetype separated by a colon.
#
for line in sys.stdin:
	line = line.strip()
	words = line.rsplit(":") # bugger! file output occasionally has a ':' in the mime-type
	if len(words) == 2:
		# There should only be two if the output really is from the find command.
		filename, actualMimeType = words[0], words[1].strip()
		# Remove parent directories from the filename
		# why? ... Problem here if the filename has no extension, but a parent directory contains a dot
		filename = filename.split("/")[-1]

		if '.' not in filename:
			ext = ""
		else:
			# Extract the extension.
			ext = filename.split(".")[-1]
			ext = ext.lower()

		message = words[0] + ":" + ext + ": " + actualMimeType
		if ext not in exts:
			print "unknown extension ",
		else:
			# Is the mimetype in the list of correct values?
			if actualMimeType in exts[ext]:
				print "match",		# ... yep
			else:
				# maybe there's a partial match?
				actualMimeParts = actualMimeType.split("/")
				for mimes in exts[ext]:
					correctMimeParts = mimes.split("/")
					if actualMimeParts[0] == correctMimeParts[0]:
						print "partial match",
						break
				else:
					print "mismatch",

		print message
	else:
		print "Error :" + line + ":"
