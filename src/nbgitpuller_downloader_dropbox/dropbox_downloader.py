from nbgitpuller.plugin_hook_specs import hookimpl
from nbgitpuller_downloader_plugins_util.plugin_helper import HandleFilesHelper


class DropBoxDownloader:
    """
    This class encapsulates the handle_files function used by nbgitpuller to download compressed archives
    from DropBox. The one instance variable, handle_files_results, is accessed by nbgitpuller after handle_files
    executes and contains the directory where the archive was decompressed to as well as the path to the local
    origin git repo established for this download.
    """
    def __init__(self):
        self.handle_files_results = None

    @hookimpl
    def handle_files(self, repo_parent_dir, other_kw_args):
        """
        :param str repo_parent_dir: the directory where the archive is downloaded to
        :param dict other_kw_args: this includes all the arguments included on the nbgitpuller URL or passed via CLI
        :return two parameter json unzip_dir and origin_repo_path
        :rtype json object
        """
        other_kw_args["repo"] = other_kw_args["repo"].replace("dl=0", "dl=1")  # dropbox: download set to 1
        hfh = HandleFilesHelper(repo_parent_dir, other_kw_args)
        output_info = yield from hfh.handle_files_helper()
        self.handle_files_results = output_info
