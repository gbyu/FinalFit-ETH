DATE="25_10_2019"

PROCS="tth_2016,ggh_2016,qqh_2016,vh_2016,tth_2017,ggh_2017,qqh_2017,vh_2017,tth_2018,ggh_2018,qqh_2018,vh_2018"
CATS="DoubleHTag_0,DoubleHTag_1,DoubleHTag_2,DoubleHTag_3,DoubleHTag_4,DoubleHTag_5,DoubleHTag_6,DoubleHTag_7,DoubleHTag_8,DoubleHTag_9,DoubleHTag_10,DoubleHTag_11"

#tests : 
#SYSINPUTFILE="/work/nchernya/DiHiggs/inputs/${DATE}/systematics_merged/output_allprocs.root"
SYSINPUTFILE="/work/nchernya/DiHiggs/inputs/${DATE}/output_hh_SM_generated_2016.root" # if no systematics, then whatever file is ok

SIGNALFILE="inputs/CMS-HGG_sigfit_singleHiggs2016_${DATE}.root,inputs/CMS-HGG_sigfit_singleHiggs2017_${DATE}.root,inputs/CMS-HGG_sigfit_singleHiggs2018_${DATE}.root"
DATAFILE="inputs/CMS-HGG_multipdf_HHbbgg_2016_2017_2018_${DATE}.root"
NODESFILE="inputs/CMS-HGG_sigfit_nodes2016_${DATE}.root,inputs/CMS-HGG_sigfit_nodes2017_${DATE}.root,inputs/CMS-HGG_sigfit_nodes2018_${DATE}.root"
INTLUMI2016=35.91
INTLUMI2017=41.53
INTLUMI2018=59.35

SCALES="HighR9EE,LowR9EE,HighR9EB,LowR9EB"
SMEARS="HighR9EERho,LowR9EERho,HighR9EEPhi,LowR9EEPhi,HighR9EBPhi,LowR9EBPhi,HighR9EBRho,LowR9EBRho"
SCALESCORR="MaterialCentralBarrel,MaterialOuterBarrel,MaterialForward"
SCALESGLOBAL="NonLinearity,Geant4,LightYield,Absolute"

SCALES=""
SMEARS=""
SCALESCORR=""
SCALESGLOBAL=""

#SMSIGNAL="GluGluToHHTo2B2G_node_SM_13TeV_madgraph,GluGluToHHTo2B2G_node_SM_13TeV_madgraph_2017"
SMSIGNAL="hh_SM_generated_2016,hh_SM_generated_2017,hh_SM_generated_2018"
#./makeParametricModelDatacardFLASHgg.py -i $SYSINPUTFILE -s $SIGNALFILE --signalProc $SMSIGNAL -d $DATAFILE -p $PROCS,$SMSIGNAL -c $CATS --photonCatScales $SCALES --photonCatSmears $SMEARS  --globalScales $SCALESGLOBAL --photonCatScalesCorr $SCALESCORR --isMultiPdf --intLumi2016 $INTLUMI2016 --intLumi2017 $INTLUMI2017 --intLumi2018 $INTLUMI2018 -o outputs/cms_HHbbgg_datacard_SMgenerated_${DATE}_systematics.txt

#for node in `seq 0 -1`;
for node in `seq 0 11` SM box;
do
   nodename="hh_node_${node}_2016,hh_node_${node}_2017,hh_node_${node}_2018"
   outname="outputs/cms_HHbbgg_datacard_node${node}_${DATE}_systematics.txt"
   SYSINPUTFILE="/work/nchernya/DiHiggs/inputs/${DATE}/output_hh_SM_generated_2016.root" # if no systematics, then whatever file is ok
  ./makeParametricModelDatacardFLASHgg.py -i $SYSINPUTFILE -s $SIGNALFILE --nodesFile $NODESFILE --signalProc $nodename -d $DATAFILE -p $PROCS,$nodename -c $CATS --photonCatScales ../Signal/dat/photonCatSyst.dat --photonCatSmears ../Signal/dat/photonCatSyst.dat --isMultiPdf  -o ${outname} --intLumi2016 $INTLUMI2016 --intLumi2017 $INTLUMI2017 --intLumi2018 $INTLUMI2018
  echo ./makeParametricModelDatacardFLASHgg.py -i $SYSINPUTFILE -s $SIGNALFILE --nodesFile $NODESFILE --signalProc $nodename -d $DATAFILE -p $PROCS,$nodename -c $CATS --photonCatScales ../Signal/dat/photonCatSyst.dat --photonCatSmears ../Signal/dat/photonCatSyst.dat --isMultiPdf  -o ${outname} --intLumi2016 $INTLUMI2016 --intLumi2017 $INTLUMI2017 --intLumi2018 $INTLUMI2018
done
