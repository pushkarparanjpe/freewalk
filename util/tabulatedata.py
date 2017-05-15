'''
Created on 01-Oct-2014

@author: pushkar


Generate custom TSV data views from the entire DataSet.

'''
from datapaths import genotypic_datapaths
from Track import Track, LEG
from Genotype import Genotype
# import HTML



def add_table_tags(htmltable):
	return '<TABLE cellpadding="4" style="border: 1px solid #000000; border-collapse: collapse;" border="1">' + htmltable + '</TABLE>'



def remove_table_tags(htmltable):
	return htmltable.replace('<TABLE cellpadding="4" style="border: 1px solid #000000; border-collapse: collapse;" border="1">', "").replace('</TABLE>', "")


# mat1 and mat2 should have equal number of columns
def columnarMerge(mat1, mat2):
	[mat1[k].extend(mat2[k]) for k in range(len(mat1))]
	return mat1


# Extend each column vector of the matrix (by appending 'None') such that the len() of all columns is equal
def equalizeColumnLenghts(mat):
	maxlen = max(map(len, mat))
	[col.extend([None] * (maxlen - len(col))) for col in mat]
	assert min(map(len, mat)) == maxlen
	return mat















