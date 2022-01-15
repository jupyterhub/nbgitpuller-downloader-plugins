from nbgitpuller.plugin_hook_specs import hookimpl
from nbgitpuller_downloader_plugins_util.plugin_helper import HandleFilesHelper


@hookimpl
def handle_files(helper_args, query_line_args):
    """
    This begins the event loop that will both download the compressed archive and send messages
    about the progress of the download to the UI.
    :param dict helper_args: the function, helper_args["progress_func"], that writes messages to
    the progress stream in the browser window and the download_q, helper_args["download_q"] the progress function uses.
    :param dict query_line_args: this includes all the arguments included on the nbgitpuller URL
    :return two parameter json unzip_dir and origin_repo_path
    :rtype json object
    """
    hfh = HandleFilesHelper(helper_args, query_line_args)
    output_info = yield from hfh.handle_files_helper()
    helper_args["handle_files_output"] = output_info
