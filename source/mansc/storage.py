from . import types
from datetime import datetime
import json
import io

class CSVEngine:
    
    def __init__(self, delimiter=","):
        self.__delimiter = delimiter

    def Export(self, objs : list) -> str:
        data = []

        for _ in objs:
            if type(_) == type(types.Model()):
                data.append(self._ExportModel(_))
            elif type(_) == type(types.Gallery()):
                data.append(self._ExportGallery(_))
            elif type(_) == type(types.Movie()):
                data.append(self._ExportMovie(_))

        return "\n".join([",".join(_) for _ in data])

    def _ExportModel(self, model: types.Model) -> list:
        return [
            model.Gender,
            model.Name,
            '\"' + model.Bio + '\"',
            str(model.CurrentAge),
            str(model.DebutAge),
            model.Eyecolor,
            model.Haircolor,
            str(model.Weight),
            str(model.Height),
            model.Breast,
            '\"' + ",".join([str(_) for _ in model.Measurements]) + '\"',
            model.Ethnic,
            model.Origin
        ]

    def _ExportMedia(self, media: types.Media) -> list:
        return [
            '\"' + media.Title + '\"',
            '\"' + media.Description + '\"',
            datetime.strftime(media.Release, "%Y-%m-%d"),
            media.Source,
            media.Photographer,
            "\"" + ",".join([(_.Name + ":" + str(media.GetModelAge(_))) for _ in media.Models]) + "\"",
            "\"" + ",".join(media.Tags) + "\""
        ]

    def _ExportGallery(self,  gallery: types.Gallery) -> list:
        return self._ExportMedia(gallery)

    def _ExportMovie(self, movie: types.Movie) -> list:
        return self._ExportMedia(movie) 

class JSONEngine:
    
    def Export(self, objs : list) -> str:
        
        models = []
        galleries = []
        movies = []

        for _ in objs:
            if type(_) == type(types.Model()):
                models.append(self._ExportModel(_))
            elif type(_) == type(types.Gallery()):
                galleries.append(self._ExportGallery(_))
            elif type(_) == type(types.Movie()):
                movies.append(self._ExportMovie(_))

        data = {}

        if len(models) > 0: data["models"] = models
        if len(galleries) > 0: data["galleries"] = galleries
        if len(movies) > 0: data["movies"] = movies

        return json.dumps(data)

    def _ExportModel(self, model: types.Model) -> dict:
        return {
            "gender": model.Gender,
            "name": model.Name,
            "bio": model.Bio,
            "currentage": model.CurrentAge,
            "debutage": model.DebutAge,
            "eyecolor": model.Eyecolor,
            "haircolor": model.Haircolor,
            "weight": model.Weight,
            "height": model.Height,
            "breast": model.Breast,
            "measurements": model.Measurements,
            "ethnic": model.Ethnic,
            "origin": model.Origin
        }

    def _ExportMedia(self, media: types.Media) -> list:
        return {
            "title": media.Title,
            "description": media.Description,
            "release": datetime.strftime(media.Release, "%Y-%m-%d"),
            "source": media.Source,
            "photographer": media.Photographer,
            "models": [{ "name": _.Name, "age": media.GetModelAge(_) } for _ in media.Models],
            "tags": media.Tags
        }

    def _ExportGallery(self,  gallery: types.Gallery) -> list:
        return self._ExportMedia(gallery)

    def _ExportMovie(self, movie: types.Movie) -> list:
        return self._ExportMedia(movie) 


def Export(objs: list, engine, stream):
    print(engine.Export(objs), file=stream)
