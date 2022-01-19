from nbgitpuller.plugin_hook_specs import hookimpl
from nbgitpuller_downloader_plugins_util.plugin_helper import HandleFilesHelper

class GenericWebDownloader:
    """
    This class encapsulates the handle_files function used by nbgitpuller to download compressed archives
    from publicly available generic web server. The one instance variable, handle_files_results, is accessed by
    nbgitpuller after handle_files executes and contains the directory where the archive was decompressed to as well
    as the path to the local origin git repo established for this download.
    """
    def __init__(self):
        self.handle_files_results = None

    @hookimpl
    def handle_files(self, repo_parent_dir, other_kw_args):
        """
        This begins the event loop that will both download the compressed archive and send messages
        about the progress of the download to the UI.
        :param str repo_parent_dir: the directory where the archive is downloaded to
        :param dict other_kw_args: this includes all the arguments included on the nbgitpuller URL or passed via CLI
        :return two parameter json unzip_dir and origin_repo_path
        :rtype json object
        """
        hfh = HandleFilesHelper(repo_parent_dir, other_kw_args)
        output_info = yield from hfh.handle_files_helper()
        self.handle_files_results = output_info
