class Errors:
    
    @staticmethod
    def args_error(error = ""):
        """Exits because of args error"""

        print("Usage: python api.py -m MOVIE_NAME")
        print("Usage: python api.py -s SERIES_NAME SEASON_Number Episode_Number")
        if error:
            print(error)
        exit(1)
