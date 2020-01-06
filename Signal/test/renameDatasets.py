import ROOT
from ROOT import *
from optparse import OptionParser, make_option
import sys
import os


parser = OptionParser(option_list=[
    make_option("--inp-files",type='string',dest='inp_files',default='vbf_M125_13TeV,ggh_M125_13TeV,bbh_M125_13TeV,gghh_M125_13TeV,tth_M125_13TeV,vh_M125_13TeV'),
    make_option("--target-names",type='string',dest='target_names',default='vbf,ggh,bbh,gghh,tth,vh'),
    make_option("--inp-dir",type='string',dest="inp_dir",default='/afs/cern.ch/work/g/gbyu/private/CMGTools/ws_made/'),
    make_option("--year",type='string',dest="year",default='2016'),
    make_option("--out-dir",type='string',dest="out_dir",default='/afs/cern.ch/work/g/gbyu/private/CMGTools/ws_made/rename/'),
    make_option("--cats",type='string',dest="cats",default='DoubleHTag_0,DoubleHTag_1,DoubleHTag_2,DoubleHTag_3,DoubleHTag_4,DoubleHTag_5,DoubleHTag_6,DoubleHTag_7,DoubleHTag_8,DoubleHTag_9,DoubleHTag_10,DoubleHTag_11'),
])

(options, args) = parser.parse_args()
cats = options.cats.split(',')
input_files = []
input_names = []
target_names = options.target_names.split(',')
target_files = []
for num,f in enumerate(target_names):
    print 'number and target ', num, f

    ########################SM generated#################
    #if "2017" in options.year : target_names.append(f.replace('-','_') +'_generated_2017_13TeV')
    #else : target_names.append(f.replace('-','_') +'_generated_13TeV')
    #input_files[num] = 'output_' + f  +'_original_generated'
    #target_files.append('output_' + f + '_generated' )
    #####################################################

    #   target_names[num]=replace(target_names[num],target_names[num]+'_'+year)

    print 'target ', f
    
    input_names.append(f+"_13TeV_125")
    input_files.append( 'output_' + f+"_M125_13TeV_"+options.year)
    target_files.append(input_files[num])

    print 'input_names ',input_names[num]
    print 'input file : ',input_files[num]
    print 'target file : ',target_files[num]

    target_names[num]=target_names[num]+"_13TeV_125"
    print "target_names[num] (rename) : ",target_names[num]
    
masses = [0.]
higgs_mass = 125.
wsname = "tagsDumper/cms_hgg_13TeV"

for num,f in enumerate(input_files):
    print 'doing file ',f
    tfile = TFile(options.inp_dir + input_files[num]+".root")
    ws = tfile.Get(wsname)
    for mass in masses :
        value = mass + higgs_mass
        ws.Print()
        print 'doing mass ',mass
        cat_datasets=[]
        for cat in cats :
            print 'doing cat ',cat
            name = input_names[num]+'_'+cat
            print 'name ',name
            dataset = (ws.data(name)).Clone(target_names[num]+"_"+cat)
            dataset.Print()
            dataset.changeObservableName("CMS_hgg_mass","CMS_hgg_mass_oldname")
            oldmass = dataset.get()["CMS_hgg_mass_oldname"]
            mass_new = RooFormulaVar( "CMS_hgg_mass", "CMS_hgg_mass", "(@0+%.1f)"%mass,RooArgList(oldmass) );
            dataset.addColumn(mass_new).setRange(100,180)
            dataset.Print()
            cat_datasets.append(dataset)

            out = TFile(options.out_dir + target_files[num] +".root","RECREATE")

            out.mkdir("tagsDumper")
            out.cd("tagsDumper")
            neww = RooWorkspace("cms_hgg_13TeV","cms_hgg_13TeV") ;
            for dat in cat_datasets:
                getattr(neww, 'import')(dat, RooCmdArg())
            neww.Write()
            out.Close()
    
