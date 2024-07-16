#!/usr/bin/env python3

__author__="prosaddas888@gmail.com"
__version__= "v.0.1"

import os
import sys
import subprocess
from pathlib import Path

def primer_blast(db_path: str, query_path: str) -> None:
	outfile = Path(query_path).stem + "_blast_out.txt"
	seq_ity = "60"
	outfmt = "6"
	cmd_db = ["makeblastdb", "-in", db_path, "-dbtype", "nucl"]
	cmd_blast = ["blastn", "-query", query_path, "-db", db_path, "-ungapped", "-perc_identity", seq_ity, "-outfmt", outfmt, "-out", outfile]
	blast_db_files = [ db_path + ext for ext in [".nhr", ".nin", ".nsq"] ]
	all_db_files = all( os.path.isfile(file_path) for file_path in blast_db_files )
	if not all_db_files:
		try:
			subprocess.run(cmd_db)
			print(f"Database created for {db_path}!")
		except Exception as e:
			print(f"Error creating BLASTn database! {e}")
			return None
	else:
		print("Database already exists.")
	try:
		subprocess.run(cmd_blast)
		print("BLASTn completed.")
		return outfile
	except Exception as e:
		print(f"Error running BLASTn! {e}")
		return None
	
def parse_blast_out(blast_path: str) -> list:
	results = []
	try:
		with open(blast_path, mode = "r", encoding = "utf-8") as fh:
			for line in fh:
				results.append(line.rstrip("\n").split("\t"))
		return results
	except Exception as e:
		print(f"BLASTn result not found! {e}")
		return None
		
def find_primer_ot(blast_results: list):
	primers = [ i[0] for i in blast_results]
	count_of_primers: dict = {item: primers.count(item) for item in set(primers)}
	sorted_count_of_primers = dict( sorted( count_of_primers.items(), key = lambda item: item[1] ) )
	return sorted_count_of_primers
	
if __name__ == "__main__":
	
	if len(sys.argv) <= 2:
		print("Useage: run_blast.py [path to query fasta file] [path to query fasta file]")
		sys.exit(1)
		
	database = sys.argv[1]
	query = sys.argv[2]
	
	blast_result = primer_blast(db_path = database, query_path = query)
	if blast_result is not None:
		primers_ots = find_primer_ot(parse_blast_out(blast_result))
		for key, value in primers_ots.items():
			print(f"{key} appeared {value} time(s) in {database}")
