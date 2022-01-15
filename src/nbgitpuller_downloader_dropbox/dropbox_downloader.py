from nbgitpuller.plugin_hook_specs import hookimpl
from nbgitpuller_downloader_plugins_util.plugin_helper import HandleFilesHelper


@hookimpl
def handle_files(helper_args, query_line_args):
    """
    :param dict helper_args: the function, helper_args["progress_func"], that writes messages to
    the progress stream in the browser window and the download_q, helper_args["download_q"] the progress function uses.
    :param dict query_line_args: this includes all the arguments included on the nbgitpuller URL
    :return two parameter json unzip_dir and origin_repo_path
    :rtype json object
    """
    query_line_args["repo"] = query_line_args["repo"].replace("dl=0", "dl=1")  # dropbox: download set to 1
    hfh = HandleFilesHelper(helper_args, query_line_args)
    output_info = yield from hfh.handle_files_helper()
    helper_args["handle_files_output"] = output_info
