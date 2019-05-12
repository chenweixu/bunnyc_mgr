import yaml
from pathlib import Path

def conf_data(style, *args):
    if style == "work_dir":
        return str(Path(__file__).parent.parent)

    if style == "work_tmp_dir":
        return str(Path(__file__).parent.parent.parent / "tmp/")

    if style == "work_conf_dir":
        return str(Path(__file__).parent.parent.parent / "conf/")

    if style == "work_log_dir":
        return str(Path(__file__).parent.parent.parent / "log/")

    if style == "work_log":
        return str(Path(__file__).parent.parent.parent / "log/work.log")

    if style == "error_log":
        return str(Path(__file__).parent.parent.parent / "log/error.log")

    conf_file = Path(__file__).parent.parent / 'conf/conf.yaml'

    data = yaml.load(conf_file.read_text(), Loader=yaml.FullLoader)

    if not args:
        return data.get(style)
    else:
        new_data = data.get(style)
        for i in iter(args):
            new_data = new_data.get(i)
        return new_data
