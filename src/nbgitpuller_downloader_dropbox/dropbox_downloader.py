from nbgitpuller.plugin_hook_specs import hookimpl
from nbgitpuller_downloader_plugins_util.plugin_helper import HandleFilesHelper


@hookimpl
def handle_files(repo_parent_dir, other_kw_args):
    """
    :param str repo_parent_dir: the directory where the archive is downloaded to
    :param dict other_kw_args: this includes all the arguments included on the nbgitpuller URL or passed via CLI
    :return two parameter json unzip_dir and origin_repo_path
    :rtype json object
    """
    other_kw_args["repo"] = other_kw_args["repo"].replace("dl=0", "dl=1")  # dropbox: download set to 1
    hfh = HandleFilesHelper(repo_parent_dir, other_kw_args)
    output_info = yield from hfh.handle_files_helper()
    other_kw_args["handle_files_output"] = output_info
