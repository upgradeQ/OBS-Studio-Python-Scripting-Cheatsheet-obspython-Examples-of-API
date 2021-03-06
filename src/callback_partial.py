import obspython as obs
from itertools import cycle
from functools import partial

datacycle = cycle([1, 2, 3, 4, 5])
datatxt = cycle(['one','two','three','four','five'])

class Example:
    def __init__(self,source_name=None):
        self.source_name = source_name

    def update_text(self,flag_func=None):
        source = obs.obs_get_source_by_name(self.source_name)
        if source is not None:
            if not flag_func:
                data = str(next(datacycle))
            else:
                data= str(next(datatxt))
            settings = obs.obs_data_create()
            obs.obs_data_set_string(settings, "text", data)
            obs.obs_source_update(source, settings)
            obs.obs_data_release(settings)
            obs.obs_source_release(source)


eg = Example()  # class created ,obs part starts


def refresh_pressed(props, prop):
    print("refresh pressed")
    eg.update_text()


def script_description():
    return "Partial example"


def script_update(settings):
    eg.source_name = obs.obs_data_get_string(settings, "source")
    obs.timer_remove(eg.update_text)
    if eg.source_name != "":
        flag = obs.obs_data_get_bool(settings,"_obs_bool")
        print(flag)
        eg.update_text = partial(eg.update_text,flag_func=flag)
        obs.timer_add(eg.update_text, 1 * 1000)


def script_properties(): # ui 
    props = obs.obs_properties_create()
    p = obs.obs_properties_add_list(
        props,
        "source",
        "Text Source",
        obs.OBS_COMBO_TYPE_EDITABLE,
        obs.OBS_COMBO_FORMAT_STRING,
    )
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)

        obs.source_list_release(sources)
    obs.obs_properties_add_bool(props,"_obs_bool","Words")
    obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)
    return props
