class Errors:
    
    @staticmethod
    def args_error(error = ""):
        """Exits because of args error"""

        print("Usage: python api.py -m MOVIE_NAME FORMAT LANGUAGE")
        print("Usage: python api.py -s SERIES_NAME FORMAT LANGUAGE SEASON_Number Episode_Number")
        if error:
            print(error)
        exit(1)

    @staticmethod
    def location_error(error = ""):
        """Exits because of location error (the location couldn't be found or anything else)"""

        print("There was a problem during writing to the specified location!")
        if error:
            print(error)
        exit(1)