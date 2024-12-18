import os
from validators import url

def check_path_or_url(path_or_url):
    if os.path.isabs(path_or_url):
        if os.path.exists(path_or_url):
            return ("path", True)
        else:
            return ("path", False)
    elif url(path_or_url):
        return ("url", None)
    else:
        return (None, None)
    
def find_section_indices(content, section_title):
    start_index = None
    end_index = None
    for i, line in enumerate(content):
        if line.strip() == section_title:
            start_index = i + 1
        elif start_index is not None and line.strip() == "":
            end_index = i
            break
    return start_index, end_index