This directory is mounted to the container when 'make test-cli' is executed. 

To test the interface the 'make test-cli' command will run the test_cli_profile.exp against an oet session 
(an iTango session using the ska profile so it has access to the OET domain objects.

The tests are run using an expect script.Any erros are displayed on screen and a full report from the 
run is written to report.txt in this folder.