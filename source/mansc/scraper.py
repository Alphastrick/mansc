from . import types
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from datetime import datetime
import json

class _ModelParser:

    @staticmethod
    def ParseObject(jsonObject: dict) -> types.Model:
        model = types.Model()
        model.Name = jsonObject["name"]
        model.Bio = jsonObject["biography"]
        model.Ethnic = jsonObject["ethnicity"]
        model.Origin = jsonObject["country"]["name"]
        model.Breast = jsonObject["breasts"]
        model.Haircolor = jsonObject["hair"]
        model.Eyecolor = jsonObject["eyes"]
        model.Measurements = jsonObject["size"]
        model.Weight = jsonObject["weight"]
        model.Height = jsonObject["height"]
        model.Gender = jsonObject["gender"]
        model.CurrentAge = jsonObject["age"]
        model.DebutAge = jsonObject["firstAppearanceAge"]
        return model

    @staticmethod
    def ParseObjectMin(jsonObject: dict) -> types.Model:
        model = types.Model()
        model.Name = jsonObject["name"]
        return model

class _GalleryParser:

    @staticmethod
    def ParseObject(jsonObject: dict) -> types.Gallery:
        gallery = types.Gallery()
        gallery.SetTitle(jsonObject["name"])
        gallery.SetDescription(jsonObject["description"])
        gallery.SetReleaseDate(datetime.strptime(jsonObject["publishedAt"][:10], "%Y-%m-%d"))
        gallery.SetPhotographer(jsonObject["photographers"][0]["name"])
        for _ in jsonObject["tags"]:
            gallery.AddTag(_)
        for _ in jsonObject["models"]:
            gallery.AddModel(_ModelParser.ParseObjectMin(_), int(_["publishAge"]))
        return gallery

    @staticmethod
    def ParseObjectMin(jsonObject: dict) -> types.Gallery:
        gallery = types.Gallery(qualified=False)
        gallery.SetTitle(jsonObject["name"])
        gallery.SetReleaseDate(datetime.strptime(jsonObject["publishedAt"][:10], "%Y-%m-%d"))
        gallery.SetPhotographer(jsonObject["photographers"][0]["name"])
        for _ in jsonObject["models"]:
            gallery.AddModel(_ModelParser.ParseObjectMin(_), 0)
        return gallery

class _MovieParser:

    @staticmethod
    def ParseObject(jsonObject: dict) -> types.Movie:
        movie = types.Movie()
        movie.SetTitle(jsonObject["name"])
        movie.SetDescription(jsonObject["description"])
        movie.SetReleaseDate(datetime.strptime(jsonObject["publishedAt"][:10], "%Y-%m-%d"))
        movie.SetPhotographer(jsonObject["photographers"][0]["name"])
        for _ in jsonObject["tags"]:
            movie.AddTag(_)
        for _ in jsonObject["models"]:
            movie.AddModel(_ModelParser.ParseObject(_), int(_["publishAge"]))
        return movie

    def ParseObjectMin(jsonObject: dict) -> types.Movie:
        movie = types.Movie(qualified=False)
        movie.SetTitle(jsonObject["name"])
        movie.SetReleaseDate(datetime.strptime(jsonObject["publishedAt"][:10], "%Y-%m-%d"))
        movie.SetPhotographer(jsonObject["photographers"][0]["name"])
        for _ in jsonObject["models"]:
            movie.AddModel(_ModelParser.ParseObjectMin(_), 0)
        return movie


class Page:

    @staticmethod
    def Factory(url: str):
        page = Page(url)
        if ModelScraper.IsValid(page):
            return ModelScraper(page)
        elif GalleryScraper.IsValid(page):
            return GalleryScraper(page)
        elif MovieScraper.IsValid(page):
            return MovieScraper(page)
        elif UpdateScraper.IsValid(page):
            return UpdateScraper(page)

    def __init__(self, url: str):
        self.__url = url
        self.__file = urlopen(url)
        self.__file = BeautifulSoup(self.__file.read(), 'html.parser')
        
        js = self.__file.find_all("script", {"defer": "", "charset": "UTF-8"})
        if len(js) == 1:
            js = "".join(js[0].contents)
            js = js[js.find('=') + 1:js.rfind(';') - len(js)]
            self.__json = json.loads(js)
        else:
            self.__json = None

    def GetUrl(self) -> str:
        return self.__url

    def GetFile(self):
        return self.__file

    def GetJson(self):
        return self.__json

    Url = property(GetUrl)
    File = property(GetFile)
    Json = property(GetJson)

class ModelScraper:
    
    class Invalid(Exception):
        def __init__(self):
            Exception.__init__(self, "Given page is not a valid model page")

    @staticmethod
    def IsValid(page: Page) -> bool:
        return page.Json["model"]["loaded"]

    def __init__(self, page: Page):
        if not ModelScraper.IsValid(page):
            raise ModelScraper.Invalid()
        self.__page = page

    def Scrape(self) -> types.Model:
        return _ModelParser.ParseObject(self.__page.Json["model"]["item"])

    def ScrapeFace(self):
        url = self.__page.Url
        url = url[:url.find(".com")+4] + self.__page.Json["model"]["item"]["headshotImagePath"]
        return ImageScraper.Scrape(url)

    def __PraseGalleryCount(self):
        return self.__page.Json["model"]["item"]["galleriesCount"]

    def __PraseMovieCount(self):
        return self.__page.Json["model"]["item"]["moviesCount"]

    def __ParseGalleries(self):
        galleries = []
        for _ in self.__page.Json["model"]["item"]["galleries"]:
            gallery = types.Gallery()
            gallery.SetTitle(_["name"])
            gallery.SetDescription(_["description"])
            gallery.SetReleaseDate(datetime.strptime(_["publishedAt"][:10], "%Y-%m-%d"))
            gallery.SetPhotographer(_["photographers"][0]["name"])
            for __ in _["tags"]:
                gallery.AddTag(__)
            galleries.append(gallery)
        return galleries

    def __ParseMovies(self):
        for _ in self.__page.Json["model"]["item"]["movies"]:
            pass
    
    Model = property(Scrape)
    NumGalleries = property(__PraseGalleryCount)
    Galleries = property(__ParseGalleries)
    NumMovies = property(__PraseMovieCount)
    Movies = property(__ParseMovies)

class GalleryScraper:

    class Invalid(Exception):
        def __init__(self):
            Exception.__init__(self, "Given page is not a valid gallery page")

    @staticmethod
    def IsValid(page: Page) -> bool:
        return page.Json["gallery"]["loaded"]

    def __init__(self, page : Page):
        if not GalleryScraper.IsValid(page):
            raise GalleryScraper.Invalid()
        self.__page = page

    def Scrape(self) -> types.Gallery:
        obj = _GalleryParser.ParseObject(self.__page.Json["gallery"]["item"])
        urlPrefix = self.__page.Url[:self.__page.Url.find(".com")+4]
        obj.SetCoverUrl(urlPrefix + self.__page.Json["gallery"]["item"]["coverImagePath"])
        obj.SetCleanCoverUrl(urlPrefix + self.__page.Json["gallery"]["item"]["coverCleanImagePath"])
        obj.SetSource(types.Source(self.__page.Json["site"]["name"].lower()))
        return obj

    Gallery = property(Scrape)

class MovieScraper:

    class InValid(Exception):
        def __init__(self):
            Exception.__init__(self, "Given page is not a valid movie page")

    @staticmethod
    def IsValid(page: Page) -> bool:
        return page.Json["movie"]["loaded"]

    def __init__(self, page: Page):
        if not MovieScraper.IsValid(page):
            raise MovieScraper.Invalid()
        self.__page = page

    def Scrape(self) -> types.Movie:
        obj = _MovieParser.ParseObject(self.__page.Json["movie"]["item"])
        urlPrefix = self.__page.Url[:self.__page.Url.find(".com")+4]
        obj.SetCoverUrl(urlPrefix + self.__page.Json["gallery"]["item"]["coverImagePath"])
        obj.SetCleanCoverUrl(urlPrefix + self.__page.Json["gallery"]["item"]["coverCleanImagePath"])
        obj.SetSource(types.Source(self.__page.Json["site"]["name"].lower()))
        return obj

    Movie = property(Scrape)

class UpdateScraper:
    
    class Invalid(Exception):
        def __init__(self):
            Exception.__init__(self, "Given page is not a valid update page")

    @staticmethod
    def IsValid(page: Page) -> bool:
        return page.Json["updates"]["loaded"]

    def __init__(self, page: Page):
        if not UpdateScraper.IsValid(page):
            raise UpdateScraper.Invalid()
        self.__page = page

    def Scrape(self) -> list:
        updates = []
        for _ in self.__page.Json["updates"]["galleries"]:
            if _["type"] == "GALLERY":
                updates.append(_GalleryParser.ParseObjectMin(_))
            elif _["type"] == "MOVIE":
                updates.append(_MovieParser.ParseObjectMin(_))
            else:
                continue;
            
            urlPrefix = self.__page.Url[:self.__page.Url.find(".com")+4]
            updates[-1].SetCoverUrl(urlPrefix + _["coverImagePath"])
            updates[-1].SetCleanCoverUrl(urlPrefix + _["coverCleanImagePath"])
            updates[-1].SetSource(types.Source(self.__page.Json["site"]["name"].lower()))

        return updates

    MediaUpdates = property(Scrape)

class ImageScraper:

    @staticmethod
    def Scrape(url: str):
        file = urlopen(url)
        return file.read()
