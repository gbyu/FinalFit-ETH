import ROOT
from ROOT import *
from optparse import OptionParser, make_option
import sys
import os
import numpy as np


parser = OptionParser(option_list=[
    make_option("--inp-files",type='string',dest='inp_files',default='GluGluToHHTo2B2G_node_SM_13TeV-madgraph,VBFHToGG_M-125_13TeV_powheg_pythia8,GluGluHToGG_M-125_13TeV_powheg_pythia8,bbHToGG_M-125_4FS_amcatnlo,ttHToGG_M125_13TeV_powheg_pythia8_v2,VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8'),  #2016

    make_option("--inp-names",type='string',dest='inp_names',default='gghh,vbf,ggh,bbh,tth,vh'),
    make_option("--inp-dir",type='string',dest="inp_dir",default='/afs/cern.ch/work/g/gbyu/private/CMGTools/ws_made/rename/'),
    make_option("--out-dir",type='string',dest="out_dir",default='/afs/cern.ch/work/g/gbyu/private/CMGTools/ws_made/test/'),

    make_option("--cats",type='string',dest="cats",default='DoubleHTag_0,DoubleHTag_1,DoubleHTag_2,DoubleHTag_3,DoubleHTag_4,DoubleHTag_5,DoubleHTag_6,DoubleHTag_7,DoubleHTag_8,DoubleHTag_9,DoubleHTag_10,DoubleHTag_11'),
    make_option("--year",type='string',dest="year",default='2016'),
])

(options, args) = parser.parse_args()
cats = options.cats.split(',')
input_files = []

###################for nodes only#####################
#input_files=[]
#whichNodes = list('SM')
#whichNodes = list(np.arange(0,12,1))
#whichNodes.append('SM')
#whichNodes.append('box')
#for i in whichNodes:
#	input_files.append('GluGluToHHTo2B2G_node_%s_13TeV-madgraph'%i)
#input_files.append('GluGluToHHTo2B2G_node_SM_13TeV-madgraph')
######################################################

input_names = options.inp_names.split(',')
for num,f in enumerate(input_names):
#        input_names[num] = input_names[num]+'_13TeV'
 #       print 'input names : ',input_names[num]
	input_files.append('output_' + f)# K+'_M125_13TeV_'+options.year+'.root'
        print 'circulate f : ',f
        print input_files[num]
        
print 'input name : ',input_names
masses = [-5.,0.,5.]
higgs_mass = 125.
wsname = "tagsDumper/cms_hgg_13TeV"

for num,f in enumerate(input_names):
	print 'doing file ',f
	tfile = TFile(options.inp_dir + "output_"+f+'_M125_13TeV_'+options.year+'.root')

	ws = tfile.Get(wsname)
	for mass in masses :
			value = mass + higgs_mass 
			ws.Print()
			print 'doing mass ',mass
			cat_datasets=[]
			for cat in cats :
				print 'doing cat ',cat
                                #name = input_names[num]+'_'+cat
                                name = input_names[num]+'_13TeV_125_'+cat
				print 'name ',name
                                print((ws.data(name)))
				if value!=125:
                                        print((ws.data(name)),input_names[num]+"_%d_"%value+"13TeV_"+cat)    
                                        print 'input_names ', input_names[num]
                                        #dataset = (ws.data(name)).Clone(input_names[num]+"_%d_"%value+cat)
                                        dataset = (ws.data(name)).Clone(input_names[num]+"_%d_"%value+"13TeV_"+cat).reduce(RooArgSet(ws.var("CMS_hgg_mass"),ws.var("dZ"),ws.var("centralObjectWeight")))
                                        dataset.Print()
                                        dataset.changeObservableName("CMS_hgg_mass","CMS_hgg_mass_old")
                                        oldmass = dataset.get()["CMS_hgg_mass_old"]
                                        mass_new = RooFormulaVar( "CMS_hgg_mass", "CMS_hgg_mass", "(@0+%.1f)"%mass,RooArgList(oldmass) );
					dataset.SetName(input_names[num]+"_%d_"%value+"13TeV_"+cat)
                                        dataset.addColumn(mass_new).setRange(100,180)
                                        dataset.Print()
				else :
                                        #name = input_names[num]+'_125_'+cat
                                        #print 'name ', name
                                        dataset = (ws.data(name)).Clone(input_names[num]+"_%d_"%value+"13TeV_"+cat).reduce(RooArgSet(ws.var("CMS_hgg_mass"),ws.var("dZ"),ws.var("centralObjectWeight")))
                                        dataset.SetName(input_names[num]+"_%d_"%value+"13TeV_"+cat)
                                        dataset.Print()
				cat_datasets.append(dataset)

#			f_new = options.out_dir + f +"_%d"%value
#	if '2017' in options.year :
                        f_new = options.out_dir + "output_"+f +"_"+options.year+"_%d"%value
			out = TFile(f_new+".root","RECREATE")
			out.mkdir("tagsDumper")
			out.cd("tagsDumper")
			neww = RooWorkspace("cms_hgg_13TeV","cms_hgg_13TeV") ;
			for dat in cat_datasets:
				 getattr(neww, 'import')(dat, RooCmdArg())
			neww.Write()
			out.Close()
                                        #			delete dataset
#			delete oldmass
#			delete mass_new
#			delete neww



