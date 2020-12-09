# CAN_Analysis_Project
- The paths are supposed to be cross-platform. If you encounter any problems, enter the paths manually.
- The script reads from the Input_CSVs folder and writes to the Output_CSVs folder, with a helper Makeshift_DB folder that does not need to be accessed.

- In the body_CAN_script.py, you can adjust the time resolution (the variable "seconds" around line 27) for matching the IDs' timestamps to the Timelog Actions. 3 seconds seemed like a reasonable amount given the lack of syncronicity.
- Check the Output_CSVs folder for the different csv files with the filtered and/or sorted data.
- Use the ID_to_Timelog_Match.py script to get a csv with the payload changes and corresponding times in a csv file. Customise the script to ensure you get exactly what you want and where you want it.
