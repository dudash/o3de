#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
#
"""
Contains functions for data from json files such as the o3de_manifests.json, engine.json, project.json, etc...
"""

import json
import logging
import os
import pathlib

from o3de import validation, utils, repo, compatibility

logging.basicConfig(format=utils.LOG_FORMAT)
logger = logging.getLogger('o3de.manifest')
logger.setLevel(logging.INFO)

# Directory methods

def get_this_engine_path() -> pathlib.Path:
    return pathlib.Path(os.path.realpath(__file__)).parents[3].resolve()


def get_home_folder() -> pathlib.Path:
    return pathlib.Path(os.path.expanduser("~")).resolve()


def get_o3de_folder() -> pathlib.Path:
    o3de_folder = get_home_folder() / '.o3de'
    o3de_folder.mkdir(parents=True, exist_ok=True)
    return o3de_folder


def get_o3de_user_folder() -> pathlib.Path:
    o3de_user_folder = get_home_folder() / 'O3DE'
    o3de_user_folder.mkdir(parents=True, exist_ok=True)
    return o3de_user_folder


def get_o3de_registry_folder() -> pathlib.Path:
    registry_folder = get_o3de_folder() / 'Registry'
    registry_folder.mkdir(parents=True, exist_ok=True)
    return registry_folder


def get_o3de_cache_folder() -> pathlib.Path:
    cache_folder = get_o3de_folder() / 'Cache'
    cache_folder.mkdir(parents=True, exist_ok=True)
    return cache_folder


def get_o3de_download_folder() -> pathlib.Path:
    download_folder = get_o3de_folder() / 'Download'
    download_folder.mkdir(parents=True, exist_ok=True)
    return download_folder


def get_o3de_engines_folder() -> pathlib.Path:
    engines_folder = get_o3de_user_folder() / 'Engines'
    engines_folder.mkdir(parents=True, exist_ok=True)
    return engines_folder


def get_o3de_projects_folder() -> pathlib.Path:
    projects_folder = get_o3de_user_folder() / 'Projects'
    projects_folder.mkdir(parents=True, exist_ok=True)
    return projects_folder


def get_o3de_gems_folder() -> pathlib.Path:
    gems_folder = get_o3de_user_folder() / 'Gems'
    gems_folder.mkdir(parents=True, exist_ok=True)
    return gems_folder


def get_o3de_templates_folder() -> pathlib.Path:
    templates_folder = get_o3de_user_folder() / 'Templates'
    templates_folder.mkdir(parents=True, exist_ok=True)
    return templates_folder


def get_o3de_restricted_folder() -> pathlib.Path:
    restricted_folder = get_o3de_user_folder() / 'Restricted'
    restricted_folder.mkdir(parents=True, exist_ok=True)
    return restricted_folder


def get_o3de_logs_folder() -> pathlib.Path:
    logs_folder = get_o3de_folder() / 'Logs'
    logs_folder.mkdir(parents=True, exist_ok=True)
    return logs_folder


def get_o3de_third_party_folder() -> pathlib.Path:
    third_party_folder = get_o3de_folder() / '3rdParty'
    third_party_folder.mkdir(parents=True, exist_ok=True)
    return third_party_folder


# o3de manifest file methods
def get_default_o3de_manifest_json_data() -> dict:
    """
    Returns dict with default values suitable for storing
    in the o3de_manifests.json
    """
    username = os.path.split(get_home_folder())[-1]

    o3de_folder = get_o3de_folder()
    default_registry_folder = get_o3de_registry_folder()
    default_cache_folder = get_o3de_cache_folder()
    default_downloads_folder = get_o3de_download_folder()
    default_logs_folder = get_o3de_logs_folder()
    default_engines_folder = get_o3de_engines_folder()
    default_projects_folder = get_o3de_projects_folder()
    default_gems_folder = get_o3de_gems_folder()
    default_templates_folder = get_o3de_templates_folder()
    default_restricted_folder = get_o3de_restricted_folder()
    default_third_party_folder = get_o3de_third_party_folder()

    default_restricted_projects_folder = default_restricted_folder / 'Projects'
    default_restricted_projects_folder.mkdir(parents=True, exist_ok=True)
    default_restricted_gems_folder = default_restricted_folder / 'Gems'
    default_restricted_gems_folder.mkdir(parents=True, exist_ok=True)
    default_restricted_engine_folder = default_restricted_folder / 'Engines' / 'o3de'
    default_restricted_engine_folder.mkdir(parents=True, exist_ok=True)
    default_restricted_templates_folder = default_restricted_folder / 'Templates'
    default_restricted_templates_folder.mkdir(parents=True, exist_ok=True)
    default_restricted_engine_folder_json = default_restricted_engine_folder / 'restricted.json'
    if not default_restricted_engine_folder_json.is_file():
        with default_restricted_engine_folder_json.open('w') as s:
            restricted_json_data = {}
            restricted_json_data.update({'restricted_name': 'o3de'})
            s.write(json.dumps(restricted_json_data, indent=4) + '\n')

    json_data = {}
    json_data.update({'o3de_manifest_name': f'{username}'})
    json_data.update({'origin': o3de_folder.as_posix()})
    json_data.update({'default_engines_folder': default_engines_folder.as_posix()})
    json_data.update({'default_projects_folder': default_projects_folder.as_posix()})
    json_data.update({'default_gems_folder': default_gems_folder.as_posix()})
    json_data.update({'default_templates_folder': default_templates_folder.as_posix()})
    json_data.update({'default_restricted_folder': default_restricted_folder.as_posix()})
    json_data.update({'default_third_party_folder': default_third_party_folder.as_posix()})
    json_data.update({'projects': []})
    json_data.update({'external_subdirectories': []})
    json_data.update({'templates': []})
    json_data.update({'restricted': [default_restricted_engine_folder.as_posix()]})
    json_data.update({'repos': []})
    json_data.update({'engines': []})
    return json_data

def get_o3de_manifest() -> pathlib.Path:
    return get_o3de_folder() / 'o3de_manifest.json'


def load_o3de_manifest(manifest_path: pathlib.Path = None) -> dict:
    """
    Loads supplied manifest file or ~/.o3de/o3de_manifest.json if None
    If the supplied manifest_path is None and  ~/.o3de/o3de_manifest.json doesn't exist default manifest data
    is instead returned.
    Note: There is a difference between supplying a manifest_path parameter of None and '~/.o3de/o3de_manifest.json'
    In the former if the o3de_manifest.json doesn't exist, default o3de manifest data is returned.
    In the later that the o3de_manifest.json must exist as the caller explicitly specified the manifest path

    raises Json.JSONDecodeError if manifest data could not be decoded to JSON
    :param manifest_path: optional path to manifest file to load
    """
    if not manifest_path:
        manifest_path = get_o3de_manifest()
        # If the default o3de manifest file doesn't exist and the manifest_path parameter was not supplied
        # return the default o3de manifest data
        if not manifest_path.is_file():
            logger.info(f'A manifest path of None has been supplied and the {manifest_path} does not exist.'
                        ' The default o3de manifest data dictionary will be returned.')
            return get_default_o3de_manifest_json_data()

    with manifest_path.open('r') as f:
        try:
            json_data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f'Manifest json failed to load at path "{manifest_path}": {str(e)}')
            # Re-raise the exception and let the caller
            # determine if they can proceed
            raise
        else:
            return json_data


def save_o3de_manifest(json_data: dict, manifest_path: pathlib.Path = None) -> bool:
    """
    Save the json dictionary to the supplied manifest file or ~/.o3de/o3de_manifest.json if None

    :param json_data: dictionary to save in json format at the file path
    :param manifest_path: optional path to manifest file to save
    """
    if not manifest_path:
        manifest_path = get_o3de_manifest()
    with manifest_path.open('w') as s:
        try:
            s.write(json.dumps(json_data, indent=4) + '\n')
            return True
        except OSError as e:
            logger.error(f'Manifest json failed to save: {str(e)}')
            return False


def get_gems_from_external_subdirectories(external_subdirs: list) -> list:
    '''
    Helper Method for scanning a set of external subdirectories for gem.json files
    '''
    gem_directories = []

    if external_subdirs:
        for subdirectory in external_subdirs:
            gem_json_path = pathlib.Path(subdirectory).resolve() / 'gem.json'
            if gem_json_path.is_file():
                gem_directories.append(pathlib.PurePath(subdirectory).as_posix())

    return gem_directories


# Data query methods
def get_manifest_engines() -> list:
    json_data = load_o3de_manifest()
    engine_list = json_data['engines'] if 'engines' in json_data else []
    # Convert each engine dict entry into a string entry
    return list(map(
        lambda engine_object: engine_object.get('path', '') if isinstance(engine_object, dict) else engine_object,
        engine_list))


def get_manifest_projects() -> list:
    json_data = load_o3de_manifest()
    return json_data['projects'] if 'projects' in json_data else []


def get_manifest_gems() -> list:
    return get_gems_from_external_subdirectories(get_manifest_external_subdirectories())


def get_manifest_external_subdirectories() -> list:
    json_data = load_o3de_manifest()
    return json_data['external_subdirectories'] if 'external_subdirectories' in json_data else []


def get_manifest_templates() -> list:
    json_data = load_o3de_manifest()
    return json_data['templates'] if 'templates' in json_data else []


def get_manifest_restricted() -> list:
    json_data = load_o3de_manifest()
    return json_data['restricted'] if 'restricted' in json_data else []


def get_manifest_repos() -> list:
    json_data = load_o3de_manifest()
    return json_data['repos'] if 'repos' in json_data else []


# engine.json queries
def get_engine_projects(engine_path:pathlib.Path = None) -> list:
    engine_path = engine_path or get_this_engine_path()
    engine_object = get_engine_json_data(engine_path=engine_path)
    if engine_object:
        return list(map(lambda rel_path: (pathlib.Path(engine_path) / rel_path).as_posix(),
                        engine_object['projects'])) if 'projects' in engine_object else []
    return []


def get_engine_gems(engine_path:pathlib.Path = None) -> list:
    return get_gems_from_external_subdirectories(get_engine_external_subdirectories(engine_path))


def get_engine_external_subdirectories(engine_path:pathlib.Path = None) -> list:
    engine_path = engine_path or get_this_engine_path()
    engine_object = get_engine_json_data(engine_path=engine_path)
    if engine_object:
        return list(map(lambda rel_path: (pathlib.Path(engine_path) / rel_path).as_posix(),
                        engine_object['external_subdirectories'])) if 'external_subdirectories' in engine_object else []
    return []


def get_engine_templates() -> list:
    engine_path = get_this_engine_path()
    engine_object = get_engine_json_data(engine_path=engine_path)
    if engine_object:
        return list(map(lambda rel_path: (pathlib.Path(engine_path) / rel_path).as_posix(),
                        engine_object['templates'])) if 'templates' in engine_object else []
    return []


# project.json queries
def get_project_gems(project_path: pathlib.Path) -> list:
    return get_gems_from_external_subdirectories(get_project_external_subdirectories(project_path))


def get_project_external_subdirectories(project_path: pathlib.Path) -> list:
    project_object = get_project_json_data(project_path=project_path)
    if project_object:
        return list(map(lambda rel_path: (pathlib.Path(project_path) / rel_path).as_posix(),
                        project_object['external_subdirectories'])) if 'external_subdirectories' in project_object else []
    return []

def get_project_engine_path(project_path: pathlib.Path, 
                            project_json_data: dict = None, 
                            user_project_json_data: dict = None, 
                            engines_json_data: dict = None) -> pathlib.Path or None:
    """
    Returns the most compatible engine path for a project based on the project's 
    'engine' field and taking into account <project_path>/user/project.json overrides
    or the engine the project is registered with.
    :param project_path: Path to the project
    :param project_json_data: Optional json data to use to avoid reloading project.json  
    :param user_project_json_data: Optional json data to use to avoid reloading <project_path>/user/project.json  
    :param engines_json_data: Optional engines json data to use for engines to avoid reloading all engine.json files
    """
    engine_path = compatibility.get_most_compatible_project_engine_path(project_path, 
                                                                        project_json_data, 
                                                                        user_project_json_data, 
                                                                        engines_json_data)
    if engine_path:
        return engine_path

    # check if the project is registered in an engine.json
    # in a parent folder
    resolved_project_path = pathlib.Path(project_path).resolve()
    engine_path = utils.find_ancestor_dir_containing_file(pathlib.PurePath('engine.json'), resolved_project_path)
    if engine_path:
        projects = get_engine_projects(engine_path)
        for engine_project_path in projects:
            if resolved_project_path.samefile(pathlib.Path(engine_project_path).resolve()):
                return engine_path

    return None

def get_project_templates(project_path: pathlib.Path) -> list:
    project_object = get_project_json_data(project_path=project_path)
    if project_object:
        return list(map(lambda rel_path: (pathlib.Path(project_path) / rel_path).as_posix(),
                        project_object['templates'])) if 'templates' in project_object else []
    return []


# gem.json queries
def get_gem_gems(gem_path: pathlib.Path) -> list:
    return get_gems_from_external_subdirectories(get_gem_external_subdirectories(gem_path, list(), dict()))


def get_gem_external_subdirectories(gem_path: pathlib.Path, visited_gem_paths: list, gems_json_data_by_path: dict = None) -> list:
    '''
    recursively visit each gems "external_subdirectories" entries and return them in a list
    :param: gem_path path to the gem whose gem.json will be queried for the "external_subdirectories" field
    :param: visited_gem_paths stores the list of gem paths visited so far up until this get_path
    The visited_gem_paths is a list instead of a set to maintain insertion order
    :param: gems_json_data_by_path a cache of gem.json data with the gem_path as the key 
    '''

    # Resolve the path before to make sure it is absolute before adding to the visited_gem_paths set
    gem_path = pathlib.Path(gem_path).resolve()
    if gem_path in visited_gem_paths:
        logger.warning(f'A cycle has been detected when visiting external subdirectories at gem path "{gem_path}". The visited paths are: {visited_gem_paths}')
        return []
    visited_gem_paths.append(gem_path)

    if isinstance(gems_json_data_by_path, dict):
        # Use the cache 
        if gem_path in gems_json_data_by_path:
            gem_object = gems_json_data_by_path[gem_path]
        else:
            gem_object = get_gem_json_data(gem_path=gem_path)
            # store the value even if its None so we don't open the file again
            gems_json_data_by_path[gem_path] = gem_object
    else:
        gem_object = get_gem_json_data(gem_path=gem_path)

    external_subdirectories = []
    if gem_object:
        external_subdirectories = list(map(lambda rel_path: (pathlib.Path(gem_path) / rel_path).resolve().as_posix(),
            gem_object['external_subdirectories'])) if 'external_subdirectories' in gem_object else []

        # recurse into gem subdirectories
        for external_subdirectory in external_subdirectories:
            external_subdirectory = pathlib.Path(external_subdirectory)
            gem_json_path = external_subdirectory / 'gem.json'
            if gem_json_path.is_file():
                external_subdirectories.extend(get_gem_external_subdirectories(external_subdirectory, visited_gem_paths, gems_json_data_by_path))

    # The gem_path has completely visited, remove it from the visit set
    visited_gem_paths.remove(gem_path)

    return list(dict.fromkeys(external_subdirectories))


def get_gem_templates(gem_path: pathlib.Path) -> list:
    gem_object = get_gem_json_data(gem_path=gem_path)
    if gem_object:
        return list(map(lambda rel_path: (pathlib.Path(gem_path) / rel_path).as_posix(),
                        gem_object['templates'])) if 'templates' in gem_object else []
    return []


# Combined manifest queries
def get_all_projects() -> list:
    projects_data = get_manifest_projects()
    projects_data.extend(get_engine_projects())
    # Remove duplicates from the list
    return list(dict.fromkeys(projects_data))


def get_all_gems(project_path: pathlib.Path = None) -> list:
    return get_gems_from_external_subdirectories(get_all_external_subdirectories(project_path=project_path, gems_json_data_by_path=dict()))


def add_dependency_gem_names(gem_name:str, gems_json_data_by_name:dict, all_gem_names:set):
    """
    Add gem names for all gem dependencies to the all_gem_names set recursively
    param: gem_name the gem name to add with its dependencies
    param: gems_json_data_by_name a dict of all gem json data to use
    param: all_gem_names the set that all dependency gem names are added to
    """
    gem_json_data = gems_json_data_by_name.get(gem_name, None)
    if gem_json_data:
        dependencies = gem_json_data.get('dependencies',[])
        for dependency_gem_name in dependencies:
            if dependency_gem_name not in all_gem_names:
                all_gem_names.add(dependency_gem_name)
                add_dependency_gem_names(dependency_gem_name, gems_json_data_by_name, all_gem_names)


def remove_non_dependency_gem_json_data(gem_names:list, gems_json_data_by_name:dict) -> None:
    """
    Given a list of gem names and a dict of all gem json data, remove all gem entries that are not
    in the list and not dependencies. 
    param: gem_names the list of gem names
    param: gems_json_data_by_name a dict of all gem json data that will be modified
    """
    gem_names_to_keep = set(gem_names)
    for gem_name in set(gem_names):
        add_dependency_gem_names(gem_name, gems_json_data_by_name, gem_names_to_keep)

    gem_names_to_remove = [gem_name for gem_name in gems_json_data_by_name if gem_name not in gem_names_to_keep]
    for gem_name in gem_names_to_remove:
        del gems_json_data_by_name[gem_name]


def get_gems_json_data_by_name(engine_path:pathlib.Path = None, 
                               project_path: pathlib.Path = None, 
                               include_manifest_gems: bool = False,
                               include_engine_gems: bool = False,
                               external_subdirectories: list = None) -> dict:
    """
    Create a dictionary of gem.json data with gem names as keys based on the provided list of
    external subdirectories, engine_path or project_path.  Optionally, include gems
    found using the o3de manifest.

    It's often more efficient to open all gem.json files instead of 
    looking up each by name, which will load many gem.json files multiple times
    It takes about 150ms to populate this structure with 137 gems, 4696 bytes in total

    param: engine_path optional engine path
    param: project_path optional project path
    param: include_manifest_gems if True, include gems found using the o3de manifest 
    param: include_engine_gems if True, include gems found using the engine, 
    will use the current engine if no engine_path is provided and none can be deduced from
    the project_path
    param: external_subdirectories optional external_subdirectories to include
    return: a dictionary of gem_name -> gem.json data
    """
    all_gems_json_data = {}

    # we don't use a default list() value in the function params
    # because Python will persist changes to this default list across
    # multiple function calls which is FUN to debug
    external_subdirectories = list() if not external_subdirectories else external_subdirectories

    if include_manifest_gems:
        external_subdirectories.extend(get_manifest_external_subdirectories())

    if project_path:
        external_subdirectories.extend(get_project_external_subdirectories(project_path))
        if not engine_path and include_engine_gems:
            engine_path = get_project_engine_path(project_path=project_path)

    if engine_path or include_engine_gems:
        # this will use the current engine if engine_path is None
        external_subdirectories.extend(get_engine_external_subdirectories(engine_path))

    # Filter out duplicate external_subdirectories before querying if they contain gem.json files
    external_subdirectories = list(dict.fromkeys(external_subdirectories))

    gem_paths = get_gems_from_external_subdirectories(external_subdirectories)
    for gem_path in gem_paths:
        get_gem_external_subdirectories(gem_path, list(), all_gems_json_data)

    # convert from being keyed on gem_path to gem_name and store the paths
    utils.replace_dict_keys_with_value_key(all_gems_json_data, value_key='gem_name', replaced_key_name='path')

    return all_gems_json_data


def get_all_external_subdirectories(engine_path:pathlib.Path = None, project_path: pathlib.Path = None, gems_json_data_by_path: dict = None) -> list:
    external_subdirectories_data = get_manifest_external_subdirectories()
    external_subdirectories_data.extend(get_engine_external_subdirectories(engine_path))
    if project_path:
        external_subdirectories_data.extend(get_project_external_subdirectories(project_path))

    # Filter out duplicate external_subdirectories before querying if they contain gem.json files
    external_subdirectories_data = list(dict.fromkeys(external_subdirectories_data))

    gem_paths = get_gems_from_external_subdirectories(external_subdirectories_data)
    for gem_path in gem_paths:
        external_subdirectories_data.extend(get_gem_external_subdirectories(gem_path, list(), gems_json_data_by_path))

    # Remove duplicates from the list
    return list(dict.fromkeys(external_subdirectories_data))


def get_all_templates(project_path: pathlib.Path = None) -> list:
    templates_data = get_manifest_templates()
    templates_data.extend(get_engine_templates())
    if project_path:
        templates_data.extend(get_project_templates(project_path))

    gems_data = get_all_gems(project_path)
    for gem_path in gems_data:
        templates_data.extend(get_gem_templates(gem_path))

    # Remove duplicates from the list
    return list(dict.fromkeys(templates_data))


# Template functions
def get_templates_for_project_creation(project_path: pathlib.Path = None) -> list:
    project_templates = []
    for template_path in get_all_templates(project_path):
        template_path = pathlib.Path(template_path)
        template_json_path = template_path / 'template.json'
        if not validation.valid_o3de_template_json(template_json_path):
            continue
        project_json_path = template_path / 'Template' / 'project.json'
        if validation.valid_o3de_project_json(project_json_path):
            project_templates.append(template_path)

    return project_templates


def get_templates_for_gem_creation(project_path: pathlib.Path = None) -> list:
    gem_templates = []
    for template_path in get_all_templates(project_path):
        template_path = pathlib.Path(template_path)
        template_json_path = template_path / 'template.json'
        if not validation.valid_o3de_template_json(template_json_path):
            continue

        gem_json_path = template_path / 'Template' / 'gem.json'
        if validation.valid_o3de_gem_json(gem_json_path):
            gem_templates.append(template_path)
    return gem_templates


def get_templates_for_generic_creation(project_path: pathlib.Path = None) -> list:
    generic_templates = []
    for template_path in get_all_templates(project_path):
        template_path = pathlib.Path(template_path)
        template_json_path = template_path / 'template.json'
        if not validation.valid_o3de_template_json(template_json_path):
            continue
        gem_json_path = template_path / 'Template' / 'gem.json'
        project_json_path = template_path / 'Template' / 'project.json'
        if not validation.valid_o3de_gem_json(gem_json_path) and\
                not validation.valid_o3de_project_json(project_json_path):
            generic_templates.append(template_path)

    return generic_templates


def get_json_file_path(object_typename: str,
                       object_path: str or pathlib.Path) -> pathlib.Path:
    if not object_typename or not object_path:
        logger.error('Must specify an object typename and object path.')
        return None

    object_path = pathlib.Path(object_path).resolve()
    return object_path / f'{object_typename}.json'


def get_json_data_file(object_json: pathlib.Path,
                       object_typename: str,
                       object_validator: callable) -> dict or None:
    if not object_typename:
        logger.error('Missing object typename.')
        return None

    if not object_json or not object_json.is_file():
        logger.error(f'Invalid {object_typename} json {object_json} supplied or file missing.')
        return None

    if not object_validator or not object_validator(object_json):
        logger.error(f'{object_typename} json {object_json} is not valid or could not be validated.')
        return None

    with object_json.open('r') as f:
        try:
            object_json_data = json.load(f)
        except json.JSONDecodeError as e:
            logger.warning(f'{object_json} failed to load: {e}')
        else:
            return object_json_data

    return None


def get_json_data(object_typename: str,
                  object_path: str or pathlib.Path,
                  object_validator: callable) -> dict or None:
    object_json = get_json_file_path(object_typename, object_path)

    return get_json_data_file(object_json, object_typename, object_validator)


def get_engine_json_data(engine_name: str = None,
                         engine_path: str or pathlib.Path = None) -> dict or None:
    if not engine_name and not engine_path:
        logger.error('Must specify either a Engine name or Engine Path.')
        return None

    if engine_name and not engine_path:
        engine_path = get_registered(engine_name=engine_name)

    return get_json_data('engine', engine_path, validation.valid_o3de_engine_json)


def get_project_json_data(project_name: str = None,
                          project_path: str or pathlib.Path = None,
                          user: bool = False) -> dict or None:
    if not project_name and not project_path:
        logger.error('Must specify either a Project name or Project Path.')
        return None

    if project_name and not project_path:
        project_path = get_registered(project_name=project_name)

    if pathlib.Path(project_path).is_file():
        return get_json_data_file(project_path, 'project', validation.valid_o3de_project_json)
    elif user:
        # create the project user folder if it doesn't exist
        user_project_folder = pathlib.Path(project_path) / 'user'
        user_project_folder.mkdir(parents=True, exist_ok=True)

        user_project_json_path = user_project_folder / 'project.json'

        # return an empty json object if no file exists
        if not user_project_json_path.exists():
            return {}
        else:
            # skip validation because a user project.json is only for overrides and can be empty
            return get_json_data('project', user_project_folder, validation.always_valid) or {}
    else:
        return get_json_data('project', project_path, validation.valid_o3de_project_json)


def get_gem_json_data(gem_name: str = None, gem_path: str or pathlib.Path = None,
                      project_path: pathlib.Path = None) -> dict or None:
    if not gem_name and not gem_path:
        logger.error('Must specify either a Gem name or Gem Path.')
        return None

    if gem_name and not gem_path:
        gem_path = get_registered(gem_name=gem_name, project_path=project_path)

    # Call get_json_data_file if the path is an existing file as get_json_data appends gem.json
    if pathlib.Path(gem_path).is_file():
        return get_json_data_file(gem_path, 'gem', validation.valid_o3de_gem_json)
    else:
        return get_json_data('gem', gem_path, validation.valid_o3de_gem_json)


def get_template_json_data(template_name: str = None, template_path: str or pathlib.Path = None,
                           project_path: pathlib.Path = None) -> dict or None:
    if not template_name and not template_path:
        logger.error('Must specify either a Template name or Template Path.')
        return None

    if template_name and not template_path:
        template_path = get_registered(template_name=template_name, project_path=project_path)

    # Call get_json_data_file if the path is an existing file as get_json_data appends template.json
    if pathlib.Path(template_path).is_file():
        return get_json_data_file(template_path, 'template', validation.valid_o3de_template_json)
    else:
        return get_json_data('template', template_path, validation.valid_o3de_template_json)


def get_restricted_json_data(restricted_name: str = None, restricted_path: str or pathlib.Path = None,
                             project_path: pathlib.Path = None) -> dict or None:
    if not restricted_name and not restricted_path:
        logger.error('Must specify either a Restricted name or Restricted Path.')
        return None

    if restricted_name and not restricted_path:
        restricted_path = get_registered(restricted_name=restricted_name, project_path=project_path)

    return get_json_data('restricted', restricted_path, validation.valid_o3de_restricted_json)


def get_repo_json_data(repo_uri: str) -> dict or None:
    if not repo_uri:
        logger.error('Must specify a Repo Uri.')
        return None

    repo_json = get_repo_path(repo_uri=repo_uri)

    return get_json_data_file(repo_json, "Repo", validation.valid_o3de_repo_json)


def get_repo_path(repo_uri: str, cache_folder: str or pathlib.Path = None) -> pathlib.Path:
    repo_manifest = f'{repo_uri}/repo.json'
    cache_file, _ = repo.get_cache_file_uri(repo_manifest)
    return cache_file


def get_registered(engine_name: str = None,
                   project_name: str = None,
                   gem_name: str = None,
                   template_name: str = None,
                   default_folder: str = None,
                   repo_name: str = None,
                   restricted_name: str = None,
                   project_path: pathlib.Path = None) -> pathlib.Path or None:
    """
       Looks up a registered entry in either the  ~/.o3de/o3de_manifest.json, <this-engine-root>/engine.json
       or the <project-path>/project.json (if the project_path parameter is supplied)

       :param engine_name: Name of a registered engine to lookup in the ~/.o3de/o3de_manifest.json file
       :param project_name: Name of a project to lookup in either the ~/.o3de/o3de_manifest.json or
              <this-engine-root>/engine.json file
       :param gem_name: Name of a gem to lookup in either the ~/.o3de/o3de_manifest.json, <this-engine-root>/engine.json
            or <project-path>/project.json. NOTE: The project_path parameter must be supplied to lookup the registration
            with the project.json
       :param template_name: Name of a template to lookup in either the ~/.o3de/o3de_manifest.json, <this-engine-root>/engine.json
            or <project-path>/project.json. NOTE: The project_path parameter must be supplied to lookup the registration
            with the project.json
       :param repo_name: Name of a repo to lookup in the ~/.o3de/o3de_manifest.json
       :param default_folder: Type of "default" folder to lookup in the ~/.o3de/o3de_manifest.json
              Valid values are "engines", "projects", "gems", "templates,", "restricted"
       :param restricted_name: Name of a restricted directory object to lookup in either the ~/.o3de/o3de_manifest.json,
            <this-engine-root>/engine.json or <project-path>/project.json.
            NOTE: The project_path parameter must be supplied to lookup the registration with the project.json
       :param project_path: Path to project root, which is used to examined the project.json file in order to
              query either gems, templates or restricted directories registered with the project

       :return path value associated with the registered object name if found. Otherwise None is returned
    """
    json_data = load_o3de_manifest()

    # check global first then this engine
    if isinstance(engine_name, str):
        engines = get_manifest_engines()
        matching_engine_paths = []
        for engine in engines:
            if isinstance(engine, dict):
                engine_path = pathlib.Path(engine['path']).resolve()
            else:
                engine_path = pathlib.Path(engine).resolve()

            engine_json = engine_path / 'engine.json'
            if not pathlib.Path(engine_json).is_file():
                logger.warning(f'{engine_json} does not exist')
            else:
                with engine_json.open('r') as f:
                    try:
                        engine_json_data = json.load(f)
                    except json.JSONDecodeError as e:
                        logger.warning(f'{engine_json} failed to load: {str(e)}')
                    else:
                        this_engines_name = engine_json_data.get('engine_name','')
                        if this_engines_name == engine_name:
                            matching_engine_paths.append(engine_path)
        if matching_engine_paths:
            engine_path = matching_engine_paths[0]
            if len(matching_engine_paths) > 1:
                engines = "\n".join(map(str,matching_engine_paths))
                logger.warning(f"Multiple engines were found that match: '{engine_name}'\n{engines}\nSelecting first engine: '{engine_path}'")
            return engine_path
        

    elif isinstance(project_name, str):
        projects = get_all_projects()
        for project_path in projects:
            project_path = pathlib.Path(project_path).resolve()
            project_json = project_path / 'project.json'
            if not pathlib.Path(project_json).is_file():
                logger.warning(f'{project_json} does not exist')
            else:
                with project_json.open('r') as f:
                    try:
                        project_json_data = json.load(f)
                    except json.JSONDecodeError as e:
                        logger.warning(f'{project_json} failed to load: {str(e)}')
                    else:
                        this_projects_name = project_json_data['project_name']
                        if this_projects_name == project_name:
                            return project_path

    elif isinstance(gem_name, str):
        gems = []
        if project_path:
            gems = get_all_gems(project_path)
        else:
            # If project_path is not supplied
            registered_project_paths = get_all_projects()
            if not registered_project_paths:
                # query all gems from this engine if no projects exist
                gems = get_all_gems()
            else:
                # query all registered projects
                for registered_project_path in registered_project_paths:
                    gems.extend(get_all_gems(registered_project_path))
                gems = list(dict.fromkeys(gems))

        for gem_path in gems:
            gem_path = pathlib.Path(gem_path).resolve()
            gem_json = gem_path / 'gem.json'
            if not pathlib.Path(gem_json).is_file():
                logger.warning(f'{gem_json} does not exist')
            else:
                with gem_json.open('r') as f:
                    try:
                        gem_json_data = json.load(f)
                    except json.JSONDecodeError as e:
                        logger.warning(f'{gem_json} failed to load: {str(e)}')
                    else:
                        this_gems_name = gem_json_data['gem_name']
                        if this_gems_name == gem_name:
                            return gem_path

    elif isinstance(template_name, str):
        templates = []
        if project_path:
            templates = get_all_templates(project_path)
        else:
            # If project_path is not supplied
            registered_project_paths = get_all_projects()
            if not registered_project_paths:
                # if no projects exist, query all templates from this engine and gems
                templates = get_all_templates()
            else:
                # query all registered projects
                for registered_project_path in registered_project_paths:
                    templates.extend(get_all_templates(registered_project_path))
                templates = list(dict.fromkeys(templates))

        for template_path in templates:
            template_path = pathlib.Path(template_path).resolve()
            template_json = template_path / 'template.json'
            if not pathlib.Path(template_json).is_file():
                logger.warning(f'{template_json} does not exist')
            else:
                with template_json.open('r') as f:
                    try:
                        template_json_data = json.load(f)
                    except json.JSONDecodeError as e:
                        logger.warning(f'{template_path} failed to load: {str(e)}')
                    else:
                        this_templates_name = template_json_data['template_name']
                        if this_templates_name == template_name:
                            return template_path

    elif isinstance(restricted_name, str):
        restricted = get_manifest_restricted()
        for restricted_path in restricted:
            restricted_path = pathlib.Path(restricted_path).resolve()
            restricted_json = restricted_path / 'restricted.json'
            if not pathlib.Path(restricted_json).is_file():
                logger.warning(f'{restricted_json} does not exist')
            else:
                with restricted_json.open('r') as f:
                    try:
                        restricted_json_data = json.load(f)
                    except json.JSONDecodeError as e:
                        logger.warning(f'{restricted_json} failed to load: {str(e)}')
                    else:
                        this_restricted_name = restricted_json_data['restricted_name']
                        if this_restricted_name == restricted_name:
                            return restricted_path

    elif isinstance(default_folder, str):
        if default_folder == 'engines':
            if 'default_engines_folder' in json_data:
                default_engines_folder = pathlib.Path(json_data['default_engines_folder'])
            else:
                default_engines_folder = pathlib.Path(
                    get_default_o3de_manifest_json_data().get('default_engines_folder', None))
            return default_engines_folder.resolve() if default_engines_folder else None
        elif default_folder == 'projects':
            if 'default_projects_folder' in json_data:
                default_projects_folder = pathlib.Path(json_data['default_projects_folder'])
            else:
                default_projects_folder = pathlib.Path(
                    get_default_o3de_manifest_json_data().get('default_projects_folder', None))
            return default_projects_folder.resolve() if default_projects_folder else None
        elif default_folder == 'gems':
            if 'default_gems_folder' in json_data:
                default_gems_folder = pathlib.Path(json_data['default_gems_folder'])
            else:
                default_gems_folder = pathlib.Path(
                    get_default_o3de_manifest_json_data().get('default_gems_folder', None))
            return default_gems_folder.resolve() if default_gems_folder else None
        elif default_folder == 'templates':
            if 'default_templates_folder' in json_data:
                default_templates_folder = pathlib.Path(json_data['default_templates_folder'])
            else:
                default_templates_folder = pathlib.Path(
                    get_default_o3de_manifest_json_data().get('default_templates_folder', None))
            return default_templates_folder.resolve() if default_templates_folder else None
        elif default_folder == 'restricted':
            if 'default_restricted_folder' in json_data:
                default_restricted_folder = pathlib.Path(json_data['default_restricted_folder'])
            else:
                default_restricted_folder = pathlib.Path(
                    get_default_o3de_manifest_json_data().get('default_restricted_folder', None))
            return default_restricted_folder.resolve() if default_restricted_folder else None

    elif isinstance(repo_name, str):
        cache_folder = get_o3de_cache_folder()
        for repo_uri in json_data['repos']:
            cache_file = get_repo_path(repo_uri=repo_uri, cache_folder=cache_folder)
            if cache_file.is_file():
                repo = pathlib.Path(cache_file).resolve()
                with repo.open('r') as f:
                    try:
                        repo_json_data = json.load(f)
                    except json.JSONDecodeError as e:
                        logger.warning(f'{cache_file} failed to load: {str(e)}')
                    else:
                        this_repos_name = repo_json_data['repo_name']
                        if this_repos_name == repo_name:
                            return repo_uri
    return None
