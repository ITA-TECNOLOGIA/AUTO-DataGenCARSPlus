CURRFOLDER=$(pwd)
TMPFOLDER=/tmp 
ARCHIVEFILENAME=certificado.tar 
CERTIFICATESFOLDER=/project/cert/ 
CERTIFICATEFILES_ARCHIVE_FULLPATH="itainnova.es/privkey1.pem, itainnova.es/fullchain1.pem"
CERTIFICATEFILES_FINALDEST_RELPATH="itainnova.es/privkey.pem, itainnova.es/fullchain.pem"
# CERTIFICATEFILES_FINALPERMISSIONS="600, 644"
IFS=', ' read -r -a InputFiles2Move <<< $CERTIFICATEFILES_ARCHIVE_FULLPATH
IFS=', ' read -r -a OutputFiles2Move <<< $CERTIFICATEFILES_FINALDEST_RELPATH
# IFS=', ' read -r -a OutputFiles2MovePermissions <<< $CERTIFICATEFILES_FINALPERMISSIONS
WORKINGFOLDER=$TMPFOLDER/$(date +%Y%m%d_%H%M%S)
echo Deploying stuff at $WORKINGFOLDER...
mkdir -p $WORKINGFOLDERcd $WORKINGFOLDER
wget -qnp -NP $WORKINGFOLDER --secure-protocol=auto ftp://certificado:637*qraZLU@ftpbigdata:/$ARCHIVEFILENAME
Idx=0
for file2Move in "${InputFiles2Move[@]}"
do 
    echo Extracting "$file2Move" file into $CERTIFICATESFOLDER${OutputFiles2Move[$Idx]}... 
    tar --extract -p --overwrite --file=$WORKINGFOLDER/$ARCHIVEFILENAME $file2Move 
    mv $file2Move $CERTIFICATESFOLDER${OutputFiles2Move[$Idx]} 
    Idx=$((Idx+1))
done
echo Cleaning working folder $WORKINGFOLDER... 
cd .. 
rm $WORKINGFOLDER -R
cd $CURRFOLDER