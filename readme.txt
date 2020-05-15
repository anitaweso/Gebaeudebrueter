When starting from scratch:
    clone github repository
    copy api key into project folder (file is called api.key)

To generate Berlin map Gebäudebrüter:
    run nabuPageScraper.py to save all data entries from the Gebäudebrüter database in brueter.sqlite
    run generateLocationForPageMap.py to generate gps coordinates using GoogleMaps and OpenStreetMap
    run long_lat_to_map_by_species to generate map with OpenStreetMap coordinates grouped by species
        check if row 50 is still valid as three IDs are removed from the map



