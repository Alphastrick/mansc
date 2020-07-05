import enum
from datetime import datetime

class Source(enum.Enum):
    MetArt = "metart"
    MetArtX = "metart x"
    SexArt = "sexart"
    TheLifeErotic = "the life erotic"
    VivThomas = "viv thomas"
    Domai = "domai"
    GoddessNudes = "goddess nudes"
    EroticBeauty = "erotic beauty"
    ErroticaArchives = "errotica archives"


class Model:

    def __init__(self, qualified=True):
        self.__qualified = qualified
        self.__name = ""
        self.__bio = ""
        self.__currentAge = 0
        self.__debutage = 0
        self.__gender = ""
        self.__eyecolor = ""
        self.__haircolor = ""
        self.__breast = ""
        self.__measurements = [0, 0, 0]
        self.__height = 0
        self.__weight = 0
        self.__ethnic = ""
        self.__origin = ""

    def SetName(self, name: str):
        self.__name = name

    def GetName(self) -> str:
        return self.__name

    def SetBio(self, bio: str):
        self.__bio = bio.rstrip()

    def GetBio(self) -> str:
        return self.__bio

    def SetCurrentAge(self, age: int):
        self.__currentAge = age

    def GetCurrentAge(self) -> int:
        return self.__currentAge

    def SetDebutAge(self, age: int):
        self.__debutage = age

    def GetDebutAge(self) -> int:
        return self.__debutage

    def SetGender(self, gender: str):
        self.__gender = gender

    def GetGender(self) -> str:
        return self.__gender

    def SetEyecolor(self, eyecolor : str):
        self.__eyecolor = eyecolor

    def GetEyecolor(self) -> str:
        return self.__eyecolor

    def SetHaircolor(self, haircolor : str):
        self.__haircolor = haircolor

    def GetHaircolor(self) -> str:
        return self.__haircolor

    def SetBreast(self, breast : str):
        self.__breast = breast

    def GetBreast(self) -> str:
        return self.__breast

    def SetMeasurements(self, string : str):
        self.__measurements[0] = int(string[0:2])
        self.__measurements[1] = int(string[3:5])
        self.__measurements[2] = int(string[6:8])

    # def SetMeasurements(self, chest : int, waist : int,  hip: int):
    #     self.__measurements = [chest, waist, hip]

    def GetMeasurements(self) -> list:
        return self.__measurements

    def SetHeight(self, height: int):
        self.__height = height

    def GetHeight(self) -> int:
        return self.__height

    def SetWeight(self, weight: int):
        self.__weight = weight

    def GetWeight(self) -> int:
        return self.__weight

    def SetEthnic(self, ethnic : str):
        self.__ethnic = ethnic

    def GetEthnic(self) -> str:
        return self.__ethnic
    
    def SetOrigin(self, origin : str):
        self.__origin = origin

    def GetOrigin(self) -> str:
        return self.__origin
    
    def __str__(self) -> str:
        return (
                "Name     : {name}\n" + \
                "Bio      : {bio}\n" + \
                "Age      : Debut {debutage}, Current {age}\n" + \
                "Eyecolor : {eyecolor}\n" + \
                "Haircolor: {haircolor}\n" + \
                "Weight   : {weight}\n" + \
                "Height   : {height}\n" + \
                "Origin   : {origin}\n" + \
                "Ethnic   : {ethnic}\n"
            ).format(
                name=self.Name,
                bio=self.Bio,
                age=self.CurrentAge,
                debutage=self.DebutAge,
                eyecolor=self.Eyecolor,
                haircolor=self.Haircolor,
                weight=self.Weight,
                height=self.Height,
                origin=self.Origin,
                ethnic=self.Ethnic
            )

    Name = property(GetName, SetName)
    Bio = property(GetBio, SetBio)
    CurrentAge = property(GetCurrentAge, SetCurrentAge)
    DebutAge = property(GetDebutAge, SetDebutAge)
    Gender = property(GetGender, SetGender)
    Eyecolor = property(GetEyecolor, SetEyecolor)
    Haircolor = property(GetHaircolor, SetHaircolor)
    Breast = property(GetBreast, SetBreast)
    Measurements = property(GetMeasurements, SetMeasurements)
    Height = property(GetHeight, SetHeight)
    Weight = property(GetWeight, SetWeight)
    Ethnic = property(GetEthnic, SetEthnic)
    Origin = property(GetOrigin, SetOrigin)

class Media:
    
    class ModelWrapper:

        def __init__(self, model, age: int):
            self.__model = model
            self.__age = age

        def GetModel(self):
            return self.__model

        def GetAge(self) -> int:
            return self.__age

        Model = property(GetModel)
        Age = property(GetAge)

    def __init__(self, qualified=True):
        self.__qualified = qualified
        self.__coverUrl = ""
        self.__coverCleanUrl = ""
        self.__title = ""
        self.__description = ""
        self.__release = datetime(2000,1,1)
        self.__photographer = ""
        self.__source = ""
        self.__tags = []
        self.__models = []

    def SetCoverUrl(self, url: str) -> str:
        self.__coverUrl = url

    def GetCoverUrl(self) -> str:
        return self.__coverUrl

    def SetCleanCoverUrl(self, url: str) -> str:
        self.__coverCleanUrl = url

    def GetCleanCoverUrl(self) -> str:
        return self.__coverCleanUrl

    def SetTitle(self, title: str):
        self.__title = title

    def GetTitle(self) -> str:
        return self.__title

    def SetDescription(self, description: str):
        self.__description = description

    def GetDescription(self) -> str:
        return self.__description

    def SetReleaseDate(self, date: datetime):
        self.__release = date

    def GetReleaseDate(self) -> datetime:
        return self.__release

    def SetPhotographer(self, photographer: str):
        self.__photographer = photographer

    def GetPhotographer(self) -> str:
        return self.__photographer

    def SetSource(self, source):
        self.__source = source

    def GetSource(self) -> str:
        return self.__source.name

    def AddTag(self, tag: str):
        if not (tag in self.__tags):
            self.__tags.append(tag)

    def RemoveTag(self, tag: str):
        if tag in self.__tags:
            self.__tags.remove(tag)

    def GetTags(self):
        return self.__tags

    def AddModel(self, model, age: int):
        for _ in self.__models:
            if _.Model.Name == model.Name:
                return
        self.__models.append(Media.ModelWrapper(model, age))

    def RemoveModel(self, model):
        for _ in self.__models:
            if _.Model.Name == model.Name:
                self.__models.remove(_)
                break

    def GetModelAge(self, model) -> int:
        if type(model) == type(""):
            for _ in self.__models:
                if _.Model.Name == model:
                    return _.Age
        else:
            for _ in self.__models:
                if _.Model.Name == model.Name:
                    return _.Age
        raise Types.ModelNotContaiendException(model)

    def GetModels(self) -> list:
        return [_.Model for _ in self.__models]

    def IsQualified(self) -> bool:
        return self.__qualified

    def __str__(self) -> str:
        return (
            "Source      : {source}\n" + \
            "Title       : {title}\n" + \
            "Description : {description}\n" + \
            "Release     : {date}\n" + \
            "Photographer: {photographer}\n" + \
            "Tags        : {tags}\n" + \
            "Models      : {models}\n"
        ).format(title=self.Title,
                    description=self.Description,
                    date=datetime.strftime(self.Release, "%Y/%m/%d"),
                    photographer=self.Photographer,
                    tags=", ".join(self.Tags),
                    source=self.Source,
                    models=", ".join(["{name} ({age})".format(name=_.Name, age=self.GetModelAge(_.Name)) for _ in self.Models])
        )

    CoverUrl = property(GetCoverUrl)
    CleanCoverUrl = property(GetCleanCoverUrl)
    Title = property(GetTitle)
    Description = property(GetDescription)
    Release = property(GetReleaseDate)
    Photographer = property(GetPhotographer)
    Source = property(GetSource)
    Tags =  property(GetTags)
    Models = property(GetModels)     

class Gallery(Media):

    def __init__(self, qualified=True):
        self.__qualified = qualified
        Media.__init__(self, qualified)

    def IsQualified(self) -> bool:
        return Media.IsQualified(self) and self.__qualified

    def __str__(self):
        return "-- Gallery {qualified}\n{media}".format(
            media=Media.__str__(self),
            qualified=("" if self.IsQualified() == True else "< not fully qualified >")
        )

class Movie(Media):
    
    def __init__(self, qualified=True):
        self.__qualified = qualified
        Media.__init__(self, qualified)

    def IsQualified(self) -> bool:
        return Media.IsQualified(self) and self.__qualified

    def __str__(self):
        return "-- Movie {qualified}\n{media}".format(
            media=Media.__str__(self),
            qualified=("" if self.IsQualified == True else "< not fully qualified >")
        )

class ModelNotContaiendException(Exception):
    def __init__(self, model):
        Exception.__init__(self, "Model '{model}' is not listed".format(model=model.Name))

