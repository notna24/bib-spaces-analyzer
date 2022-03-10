# bib-spaces-analyzer

This program fetches the number of available seats in my universitys libraries
and analyzes them, so that I can figure out, when it is most visited and how
the numbers differ in finals week. Just some fun things to do with the collected Data.

# run

# Running the robot as a service

There is a example service file included in the bib-spaces-analyzer/service directory.

First: Replace the parts that say User in the bib-spaces-analyzer.service file with the name of the user that will run the service.

Second: move the parent directory of this directory in your users home folder.

Third: Install the service.

Note: If you want to alter the path of the bib-spaces-analyzer directory, please don't forget to edit the ExecStart path in the service file.

# results