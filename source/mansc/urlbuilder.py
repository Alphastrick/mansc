from datetime import datetime
from . import types

def __GetSideUrl(source: types.Source) -> str:
    if source == types.Source.ErroticaArchives:
        return "https://www.errotica-archives.com"
    else:
        return "https://www.{name}.com".format(name=source.value.replace(' ', ''))

def BuildModelUrl(source: types.Source, model: str):
    _model = model.lower().replace(' ', '-')
    _source = __GetSideUrl(source)
    return "{source}/model/{model}".format(source=_source,model=_model)

def BuildGalleryUrl(source: types.Source, title: str, model: str, date: datetime):
    _model = model.lower().replace(' ', '-')
    _title = title.upper().replace(' ', '_').replace('&','_')
    _date = date.strftime("%Y%m%d")
    _source = __GetSideUrl(source)
    return "{source}/model/{model}/gallery/{date}/{title}".format(source=_source,model=_model,date=_date,title=_title)

def BuildMovieUrl(source: types.Source, title: str, model: str, date: datetime):
    _model = model.lower().replace(' ', '-')
    _title = title.upper().replace(' ', '_').replace('&','_')
    _date = date.strftime("%Y%m%d")
    _source = __GetSideUrl(source)
    return "{source}/model/{model}/movie/{date}/{title}".format(source=_source,model=_model,date=_date,title=_title)

def BuildUpdatesUrl(source: types.Source):
    _source = __GetSideUrl(source)
    return "{source}/updates".format(source=_source)