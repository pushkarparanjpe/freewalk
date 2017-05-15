'''
Created on 01-Oct-2014

@author: pushkar
'''
from collections import OrderedDict


# ORDERED{ GENOTYPE : PATH, }

genotypic_datapaths = OrderedDict((
								
				# WT
				#---			
# 				('CS-Fast' ,
# 					'/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Pushkar/analysis/CS-Fast'),
# 				('CS-Slow',
# 					'/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Pushkar/analysis/CS-Slow'),
								
				# Light Levels : [3280Lux, 3790Lux, 4520Lux, 5550Lux]
				('CS-3280Lux' ,
					'/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Pushkar/analysis/light-levels/3280Lux'),
				('CS-3790Lux' ,
					'/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Pushkar/analysis/light-levels/3790Lux'),
				('CS-4520Lux' ,
					'/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Pushkar/analysis/light-levels/4520Lux'),
				('CS-5550Lux' ,
					'/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Pushkar/analysis/light-levels/5550Lux'),


				# CONTROLS
				#---------
# 				('UAS-Rdli x CS'	,
# 					'/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Swetha/analysis/RNAi/Constitutive/CONTROLS/UAS-Rdli x CS/Consolidated_UAS-Rdli x CS'),
# 				('Adult(CS x UAS-Dicer2;OK371-GAL4;TubGal80ts)' ,
# 					'/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Swetha/analysis/RNAi/AdultSpecific/dicer;OK371;Gal80ts X CS/Consolidated_Genotypic_CTRLs'),
# 				('Temp18(UAS-Rdli x UAS-Dicer2;OK371-GAL4;TubGal80ts)' ,
# 					'/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Swetha/analysis/RNAi/AdultSpecific/Temperature_CTRLS/Consolidated_TempCtrls_RDLi'),
				('Adult(UAS-Dicer2;OK371-GAL4;TubGal80ts x UAS-mCD8GFP)' ,
					'/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Swetha/analysis/RNAi/AdultSpecific/UAS-Dicer2;OK371-GAL4;TubGAL80ts x UAS-mCD8GFP/Consolidated_UAS-Dicer2;OK371-GAl4;TubGAL80ts x UAS-mCD8GFP'),


###
				('UAS-Dicer2;OK371-GAL4 x UAS-mCD8GFP',
					'/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Swetha/analysis/RNAi/Constitutive/CONTROLS/UAS-Dicer2;OK371-GAL4 x UAS-mCD8GFP/Consolidated_UAS-Dicer2;OK371-GAL4 x UAS-mCD8GFP'),
# 					
# 
				('VGN-Intron-Region3-GAL4 x UAS_mCD8GFP',
					'/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Swetha/analysis/RNAi/Constitutive/CONTROLS/VGN-Intron-Region3-GAL4 x UAS_mCD8GFP'),
###


				# Constitutive knockdowns
				#------------------------
					# OK371
# 						# Rdli
# 						 ('UAS-Rdli x UAS-Dicer2;OK371-GAL4;TubGal80ts'	,
# 						 	'/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Swetha/analysis/RNAi/Constitutive/PanMn/Rdli/Consolidated_Rdli'),
# 					# OK371
# 						# GluCli
# 						('UAS-GluCli x UAS-Dicer2;OK371-GAL4;TubGal80ts'	,
# 							'/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Swetha/analysis/RNAi/Constitutive/PanMn/GluCLi/Consolidated_GluCli'),

###
					# VGN_IntronReg3
						# Rdli
						('UAS-Rdli x VGN_Intron_Region3-GAL4' ,
							'/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Swetha/analysis/RNAi/Constitutive/Subsets/Rdli/VGN Intron Region 3 GAL4/Consolidated_VGNReg3_Rdli'),
###

# 					# VGN_6341
# 						# GluCli
# 						('UAS-GluCli x VGN_6341-GAL4' ,
# 							'/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Swetha/analysis/RNAi/Constitutive/Subsets/GluCli/VGN 6341 GAL4/12-07-2014'),


###					
					# UAS-Dicer2;OK371-GAL4 x UAS-Rdli
						('Consolidated_UAS-Dicer2;OK371-GAL4 x UAS-Rdli',
								'/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Swetha/analysis/RNAi/Constitutive/PanMn/Rdli/Consolidated_UAS-Dicer2;OK371-GAL4 x UAS-Rdli'),
###

				# Adult-specific knockdowns
				#------------------------
					# OK371
						# Rdli
						('Adult(UAS-Rdli x UAS-Dicer2;OK371-GAL4;TubGal80ts)' ,
							'/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Swetha/analysis/RNAi/AdultSpecific/dicer;OK371;GAl80ts X rdl G-RNAi/consolidated_rdlgi'),

			))


plotspath = "/media/pushkar/ccc1f18b-7f26-4c0d-b510-a582d28d075e/pushkar/walking/data/Swetha/analysis/plots"




