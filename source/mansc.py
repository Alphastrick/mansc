from datetime import datetime
import sys
import argparse
import json
import mansc
import io

def Main():

    parser = argparse.ArgumentParser(description="MAN:SC - MetArt-Network Scraper / Crawler")

    parser.add_argument("--Source",
                        dest="Source",
                        default="MetArt",
                        help="Change source site",
                        choices=[_.name for _ in mansc.types.Source]
                        )

    parser.add_argument("--Result",
                        dest="Result",
                        default="json",
                        help="Change result type",
                        choices=["json", "csv"]
                        )


    subparsers = parser.add_subparsers(help="Select scraper mode", dest='CMD')

    mode_model = subparsers.add_parser("model", help="Scrape model information")
    mode_model.add_argument("-m", "--Model", dest="Model", help="Set Model")

    mode_media = subparsers.add_parser("media", help="Scrape media information")
    mode_media.add_argument("-o", "--type", dest="Type", default="gallery", choices=["gallery", "movie"], help="Set media type", required=True)
    mode_media.add_argument("-m", "--Models", dest="Model", nargs='+', default=[], help="Add model")
    mode_media.add_argument("-d", "--Date", dest="Date", help="Set Date")
    mode_media.add_argument("-t", "--Title", dest="Title", help="Set Title")

    arguments = parser.parse_args()

    sourceSite = mansc.types.Source[arguments.Source]

    result = []

    if arguments.CMD == "model":
            url = mansc.urlbuilder.BuildModelUrl(sourceSite,
                                                 model=arguments.Model.lower().replace(' ', '-')
                                                )
            scraper = mansc.scraper.ModelScraper(mansc.scraper.Page(url))
            result.append(scraper.Model)
    elif arguments.CMD == "media":
        if  arguments.Type == "gallery":
            url = mansc.urlbuilder.BuildGalleryUrl(sourceSite,
                                                   model="-and-".join(arguments.Model).lower().replace(' ', '-'),
                                                   date=datetime.strptime(arguments.Date, "%Y-%m-%d"),
                                                   title=arguments.Title
                                                )
            scraper = mansc.scraper.GalleryScraper(mansc.scraper.Page(url))
            result.append(scraper.Gallery)
        elif arguments.Type == "movie":
            url = mansc.urlbuilder.BuildMovieUrl(sourceSite,
                                                 model="-and-".join(arguments.Model).lower().replace(' ', '-'),
                                                 date=datetime.strptime(arguments.Date, "%Y-%m-%d"),
                                                 title=arguments.Title
                                                )
            scraper = mansc.scraper.MovieScraper(mansc.scraper.Page(url))
            result.append(scraper.Movie)

    engine = None

    if arguments.Result == "json": engine = mansc.storage.JSONEngine()
    elif arguments.Result == "csv": engine = mansc.storage.CSVEngine()

    mansc.storage.Export(result, engine, sys.stdout)

    return 0

if __name__ == "__main__":
    sys.exit(Main())