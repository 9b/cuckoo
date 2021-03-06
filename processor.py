#!/usr/bin/python
# Cuckoo Sandbox - Automated Malware Analysis
# Copyright (C) 2010-2011  Claudio "nex" Guarnieri (nex@cuckoobox.org)
# http://www.cuckoobox.org
#
# This file is part of Cuckoo.
#
# Cuckoo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cuckoo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.

import os
import sys

from cuckoo.processing.analysis import Analysis

# The following is just a basic default example of a possible postprocessing
# script, just to show you how you should be using the provided processing APIs.
# Another example would be for example to pass the "results" variable to a JSON
# encoder, in order to transmit data to a remote HTTP server.

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(-1)

    # The first argument being passed to this script is the path to the current
    # analysis result. This is necessary and it's automatically generated and
    # provided by main Cuckoo's process.
    if not os.path.exists(sys.argv[1]):
        sys.exit(-1)

    # The second argument being passed is the value specified in the custom
    # field in the SQLite3 Queue database. You can use it to pass along anything
    # you wish.
    try:
        print sys.argv[2]
    except IndexError:
        pass

    # Generate the log files path.
    logs_path = os.path.join(sys.argv[1], "logs")

    # Process the log files and normalize the data into a dictionary.
    results = Analysis(logs_path).process()

    # Check if any resuls were provided back.
    if not results:
        sys.exit()

    if len(results) == 0:
        sys.exit()

    # Following is just an example of using the generated dict for creating a
    # simple .txt report file.
    report = open(os.path.join(sys.argv[1], "report.txt"), "w")

    for process in results:
        report.write("PROCESS: " + str(process["process_id"]) + " - " + str(process["process_name"]) + "\n")

        for call in process["calls"]:
            report.write("\tCALL: " + call["timestamp"] + ", " + call["api"] + ", Status: " + call["status"] + ", Return Value: " + call["return"] + "\n")
            for argument in call["arguments"]:
                report.write("\t\tARGUMENT: " + argument["name"] + " -> " + argument["value"] + "\n")

        report.write("\n")

    report.close()
