from nbgitpuller_downloader_plugins_util.plugin_helper import HandleFilesHelper
from nbgitpuller.plugin_hook_specs import hookimpl
import asyncio


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
    loop = asyncio.get_event_loop()
    hfh = HandleFilesHelper(helper_args, query_line_args)
    tasks = hfh.handle_files_helper(), helper_args["wait_for_sync_progress_queue"]()
    result_handle, _ = loop.run_until_complete(asyncio.gather(*tasks))
    return result_handle
