Fuer die Gebaudebrueter Datenbank auf Berlin Karte:

run nabuPageScraper.py to save all data entries from the database to csv

run generateLocationForPageMap.py to generate gps coordinates using OpenStreetMap
    if coordinates are not being generated are "longitude" and "latitude" are empty, adjust "Strasse", "Ort" etc. in 'nabupage_longlat.csv' and then run getMissingLocationForPageMap.py to check if changes make a difference
    if changes generate coordinates, go back to www.gebaeudebrueter-in-berlin.de and edit address

run long_lat_to_map_by_species to generate map separated by species

run long_lat_to_map_by_ersatz to generate map separated by ersatz yes/no, yet pins are still coloured according to species

