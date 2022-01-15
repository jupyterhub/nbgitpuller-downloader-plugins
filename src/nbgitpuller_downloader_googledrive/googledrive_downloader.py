import re
import requests
from nbgitpuller.plugin_hook_specs import hookimpl
from nbgitpuller_downloader_plugins_util.plugin_helper import HandleFilesHelper

DOWNLOAD_URL = "https://docs.google.com/uc?export=download"


@hookimpl
def handle_files(helper_args, query_line_args):
    """
    This function calls nbgitpuller's handle_files_helper after first determining the
    file extension(e.g. zip, tar.gz, etc). Google Drive does not use the name of the file to
    identify the file on the URL so we must download the file first to get the extension from the
    response, set up a specialized download function and parameters and then pass off handling
    to nbgitpuller.
    :param dict helper_args: the function, helper_args["progress_func"], that writes messages to
    the progress stream in the browser window and the download_q, helper_args["download_q"] the progress function uses.
    :param dict query_line_args: this includes all the arguments included on the nbgitpuller URL
    :return two parameter json output_dir and origin_repo_path
    :rtype json object
    """
    repo = query_line_args["repo"]
    yield "Determining type of archive...\n"
    response = get_response_from_drive(DOWNLOAD_URL, get_id(repo))
    ext = determine_file_extension_from_response(response)
    yield f"Archive is: {ext}\n"
    helper_args["extension"] = ext
    helper_args["download_func"] = download_archive_for_google

    hfh = HandleFilesHelper(helper_args, query_line_args)
    output_info = yield from hfh.handle_files_helper()
    helper_args["handle_files_output"] = output_info


def get_id(repo):
    """
    This gets the id of the file from the URL.

    :param str repo: the url to the compressed file contained the google id
    :return the google drive id of the file to be downloaded
    :rtype str
    """
    start_id_index = repo.index("d/") + 2
    end_id_index = repo.index("/view")
    return repo[start_id_index:end_id_index]


def get_confirm_token(session):
    """
    Google may include a confirm dialog if the file is too big. This retreives the
    confirmation token and uses it to complete the download.

    :param requests.Session session: used to the get the cookies from the reponse
    :return the cookie if found or None if not found
    :rtype str
    """
    cookies = session.cookies
    for key, cookie in cookies.items():
        if key.startswith('download_warning'):
            return cookie
    return None


def download_archive_for_google(repo=None, temp_download_file=None):
    """
    This requests the file from the repo(url) given and saves it to the disk. This is executed
    in plugin_helper.py and note that the parameters to this function are the same as the standard
    parameters used by the standard download_archive function in plugin_helper. You may also note that I let
    plugin_helper handle passing the temp_download_file to the function

    :param str repo: the name of the repo
    :param str temp_download_file: the path to save the requested file to
    """
    yield "Downloading archive ...\n"
    try:
        file_id = get_id(repo)
        with requests.Session() as session:
            with session.get(DOWNLOAD_URL, params={'id': file_id}) as response:
                token = get_confirm_token(session)
                if token:
                    params = {'id': file_id, 'confirm': token}
                    response = session.get(DOWNLOAD_URL, params=params)
                with open(temp_download_file, 'ab') as f:
                    count_chunks = 1
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            count_chunks += 1
                            if count_chunks % 1000 == 0:
                                display = count_chunks / 1000
                                yield f"Downloading Progress ... {display}MB\n"
                            f.write(chunk)
        yield "Archive Downloaded....\n"
    except Exception as ex:
        raise ex

def get_response_from_drive(url, file_id):
    """
    You need to check to see that Google Drive has not asked the
    request to confirm that they disabled the virus scan on files that
    are bigger than 100MB(The size is mentioned online but I did not see
    confirmation - something larger essentially). For large files, you have
    to request again but this time putting the 'confirm=XXX' as a query
    parameter.

    :param str url: the google download URL
    :param str file_id: the google id of the file to download
    :return response object
    :rtype json object
    """
    with requests.Session() as session:
        with session.get(url, params={'id': file_id}) as response:
            token = get_confirm_token(session)
            if token:
                params = {'id': file_id, 'confirm': token}
                response = session.get(url, params=params)
                return response
            return response


def determine_file_extension_from_response(response):
    """
    This retrieves the file extension from the response.
    :param requests.Response response: the response object from the download
    :return the extension indicating the file compression(e.g. zip, tgz)
    :rtype str
    """
    content_disposition = response.headers.get('content-disposition')
    ext = None
    if content_disposition:
        file_name = re.findall("filename\\*?=([^;]+)", content_disposition)
        file_name = file_name[0].strip().strip('"')
        ext = file_name.split(".")[1]

    if ext is None:
        message = f"Could not determine compression type of: {content_disposition}"
        raise Exception(message)
    return ext
