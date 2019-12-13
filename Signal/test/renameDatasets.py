import ROOT
from ROOT import *
from optparse import OptionParser, make_option
import sys
import os


parser = OptionParser(option_list=[
        make_option("--inp-files",type='string',dest='inp_files',default='VBFHToGG_M-125_13TeV_powheg_pythia8,GluGluHToGG_M-125_13TeV_powheg_pythia8,bbHToGG_M-125_4FS_ybyt_13TeV_amcatnlo,bbHToGG_M-125_4FS_yb2_13TeV_amcatnlo,GluGluToHHTo2B2G_node_SM_13TeV-madgraph,ttHToGG_M125_13TeV_powheg_pythia8_v2,VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8'),
        make_option("--target-names",type='string',dest='target_names',default='vbf,ggh,bbh,bbh,gghh,tth,vh'),
        make_option("--inp-dir",type='string',dest="inp_dir",default='/afs/cern.ch/work/g/gbyu/public/WS_2016/'),
        make_option("--year",type='string',dest="year",default='2016'),
        make_option("--out-dir",type='string',dest="out_dir",default='/afs/cern.ch/work/g/gbyu/private/CMGTools/ws_signal/'),
        make_option("--cats",type='string',dest="cats",default='DoubleHTag_0,DoubleHTag_1,DoubleHTag_2,DoubleHTag_3,DoubleHTag_4,DoubleHTag_5,DoubleHTag_6,DoubleHTag_7,DoubleHTag_8,DoubleHTag_9,DoubleHTag_10,DoubleHTag_11'),
        ])

(options, args) = parser.parse_args()
cats = options.cats.split(',')
input_files = options.inp_files.split(',')
input_names = []
target_names = options.target_names.split(',')
target_files = []
for num,f in enumerate(input_files):
    print 'number and file ', num, f
    input_names.append(f.replace('-','_') +'_13TeV')
    print 'input_names ',input_names
    ########################SM generated#################
    #if "2017" in options.year : target_names.append(f.replace('-','_') +'_generated_2017_13TeV')
    #else : target_names.append(f.replace('-','_') +'_generated_13TeV')
    #input_files[num] = 'output_' + f  +'_original_generated'
    #target_files.append('output_' + f + '_generated' )
    #####################################################

    if "2017" in options.year :
        target_names[num]=replace(target_names[num],target_names[num]+'_2017_13TeV')
    else :
        target_names[num]=target_names[num]+'_13TeV'


    print 'target ', target_names[num]
    input_files[num] = 'output_' + f
    target_files.append('output_' + f )

    print 'input file : ',input_files[num]
    print 'target file : ',target_files[num]
    
masses = [0.]
higgs_mass = 125.
wsname = "tagsDumper/cms_hgg_13TeV"


for num,f in enumerate(input_files):
    print 'doing file ',f
    tfile = TFile(options.inp_dir + f+".root")
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

        if "2017" in options.year : out = TFile(options.out_dir + target_files[num] +"_2017.root","RECREATE")
        else : out = TFile(options.out_dir + target_files[num] +".root","RECREATE")
        out.mkdir("tagsDumper")
        out.cd("tagsDumper")
        neww = RooWorkspace("cms_hgg_13TeV","cms_hgg_13TeV") ;
        for dat in cat_datasets:
            getattr(neww, 'import')(dat, RooCmdArg())
        neww.Write()
        out.Close()
    
