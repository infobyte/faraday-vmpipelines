CMDS="faraday-cli"

echo "Executing Faraday import"

for i in $CMDS
do
	command -v $i >/dev/null && continue || { echo "$i command not found. Install the missing command and try again"; exit 1; }
done

FARADAY_HOST=$1
FARADAY_USERNAME=$2
FARADAY_PASSWORD=$3
FARADAY_WORKSPACE=$4
FARADAY_REPORT_FILENAME=$5

if [[ -z "$FARADAY_HOST" || -z "$FARADAY_USERNAME" || -z "$FARADAY_PASSWORD" || -z "$FARADAY_WORKSPACE" || -z "$FARADAY_REPORT_FILENAME" ]]
then
   echo "Missing params."
   echo "Example: ./import_scan.sh https://localhost:5985 myUsername myPassword myWorkspace myReport"
   exit 1
fi

echo "Authenticating in Faraday"
echo "N" | faraday-cli auth --url $FARADAY_HOST --user $FARADAY_USERNAME --password $FARADAY_PASSWORD

echo "Creating workspace $FARADAY_WORKSPACE if it doesn't exists"
faraday-cli workspace -a create -n $FARADAY_WORKSPACE > /dev/null
echo "Workspace $FARADAY_WORKSPACE created/selected successfully"

echo "Uploading report to $FARADAY_WORKSPACE"
faraday-cli report -ws $FARADAY_WORKSPACE $FARADAY_REPORT_FILENAME

echo "Faraday import finished successfully"