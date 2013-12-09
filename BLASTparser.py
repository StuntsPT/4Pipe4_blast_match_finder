#!/usr/bin/python3
#
#  BLASTparser.py
#
#  Copyright 2013 Francisco Pina Martins <f.pinamartins@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

from sys import argv
import re

def blast_parser(infile):
	"""Parses the tabular output of BLAST"""
	results = []
	blast_output = open(infile,'r')
	for lines in blast_output:
		if lines.startswith("#") == False:
			lines = lines.strip().split()
			results.append(lines)

	return results

def matching_snp(blast_results):
	"""Matches the SNP in the subject and query fields to make sure we're
	 talking about the same SNP"""
	matches = 0
	for hit in blast_results:
		query_snps = hit[0].split("#")[1:]
		subject_snps = hit[1].split("#")[1:]
		query_start = int(hit[6])
		query_end = int(hit[7])
		subject_start = int(hit[8])
		subject_end = int(hit[9])
		for qSNPs in query_snps:
			qSNPs = int(re.sub("\D*", "", qSNPs))
			if min(query_start, query_end) <= qSNPs <= max(query_start, query_end):
				for sSNPs in subject_snps:
					sSNPs = int(re.sub("\D*", "", sSNPs))
					if min(subject_start, subject_end) <= sSNPs <= max(subject_start, subject_end):
						if sSNPs - min(subject_start, subject_end) == qSNPs - min(query_start, query_end):
							matches += 1
							print(hit[0], hit[1])

	return matches

print(matching_snp(blast_parser(argv[1])))