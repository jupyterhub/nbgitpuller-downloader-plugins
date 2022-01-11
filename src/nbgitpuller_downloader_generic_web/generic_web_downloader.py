import asyncio
import nest_asyncio
from nbgitpuller.plugin_hook_specs import hookimpl
from nbgitpuller_downloader_plugins_util.plugin_helper import HandleFilesHelper


# this allows us to nest usage of the event_loop from asyncio
# being used by tornado in jupyter distro
# Ref: https://medium.com/@vyshali.enukonda/how-to-get-around-runtimeerror-this-event-loop-is-already-running-3f26f67e762e
nest_asyncio.apply()

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
    loop = asyncio.get_event_loop()
    hfh = HandleFilesHelper(helper_args, query_line_args)
    tasks = hfh.handle_files_helper(), helper_args["wait_for_sync_progress_queue"]()
    result_handle, _ = loop.run_until_complete(asyncio.gather(*tasks))

    return result_handle
