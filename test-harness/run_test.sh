# setup the tools environment
echo Scripting the OET to test devices
echo Installing dependencies - 'expect' is needed to run script
echo ------------------------

sudo apt-get update < /dev/null > /dev/null
sudo apt-get install -qq expect < /dev/null > /dev/null

echo install complete
#run the script
echo testing the telescope ...
/app/test-harness/test_cli_profile.exp > /app/test-harness/report.txt
cat /app/test-harness/report.txt|grep Problem -B 3

#exit
echo test complete
exit
 
