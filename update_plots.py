from csse_covid19 import Csse_covid19, ScaleType
import altair as alt
from altair_saver import save

top_n = 10
list_status = [
    Csse_covid19.Confirmed, 
    Csse_covid19.Deaths,
    Csse_covid19.Recovered,
    Csse_covid19.Active]
list_scale = [
    ScaleType.Linear,
    ScaleType.Log_10]
list_normalize = [True, False]

for status in list_status:
    countries = status.get_top_countries(top_n)
    for scale in list_scale:
        for normalize in list_normalize:
            name = './plots/{}_top{}_{}{}.svg'.format(status.name, top_n, scale.name, '_normalized' if normalize else '')
            layer = status.alt_plot(countries,sort_legend=True, day_delta=2,
                         scale_type=scale, 
                         normalize_by_population=normalize,
                         show=False)
            save(layer, name)