# ===============================================================================
# Created:        11 Sep 2018
# @author:        Jesse Wilson (Anaplan Asia Pte Ltd)
# Description:    Library to implement Anaplan API to get lists of model resources, upload files to Anaplan server,
#                 download files from Anaplan server, and execute actions.
# ===============================================================================
from __future__ import annotations
import logging
from typing import TYPE_CHECKING
from .authentication.AuthorizationManager import AuthorizationManager
from .UploadFactory import UploadFactory
from .TaskController import TaskController
from .Resources import Resources
from .ResourceParserList import ResourceParserList
from .FileDownload import FileDownload

if TYPE_CHECKING:
    from .models.ActionResponse import ActionResponse
    from .models.AnaplanConnection import AnaplanConnection
    from .models.AnaplanResourceList import AnaplanResource

logger = logging.getLogger(__name__)


# ===========================================================================
# This function reads the authentication type, Basic or Certificate, then passes
# the remaining variables to anaplan_auth to generate the authorization for Anaplan API
# ===========================================================================
def authorize(method: str, **kwargs) -> AuthorizationManager:
    """
    :param method: Authorization method
    :type method: str
    :param kwargs: Additional arguments for the authorization
    :return: Class to manage authorization flow, hold the AuthToken object,
            and handle automatic refresh of the token.
    :rtype: AuthorizationManager
    """
    return AuthorizationManager(method, **kwargs)


def file_upload(conn: AnaplanConnection, file_id: str, chunk_size: int, data: str,IsStrToUpload=False,IsReturnLog=False): #-> None:
    """Upload a file to Anaplan model

    :param conn: AnaplanConnection object which contains AuthToken object, workspace ID, and model ID
    :param file_id: ID of the file in Anaplan
    :param chunk_size: Desired chunk size of the upload request between 1-50
    :param IsStrToUpload: If the data to upload is a stringIO object instead of a file.
    :param IsReturnLog: If you need the log to know if the update process was able to be performed or not.
    :param data: Data to load, either path to local file or string
    """

    file = UploadFactory(data,IsStrToUpload)
    uploader = file.get_uploader(conn, file_id,IsStrToUpload)
    if IsReturnLog==True: # 1. if IsReturnLog==True
        TxtLog = uploader.upload(chunk_size, data,IsReturnLog=IsReturnLog)
        return TxtLog
    else: # 1. if IsReturnLog==True
        uploader.upload(chunk_size, data)    
        
def execute_action(
    conn: AnaplanConnection,
    action_id: str,
    retry_count: int,
    mapping_params: dict = None,
    IsErrorDumpNeeded:bool=True
) -> ActionResponse:
    """Execute a specified Anaplan action

    :param conn: AnaplanConnection object which contains AuthToken object, workspace ID, and model ID
    :param action_id: ID of the Anaplan action to execute
    :param retry_count: Number of times to attempt to retry if an error occurs executing an action
    :param mapping_params: Optional dictionary of import mapping parameters
    :return: Detailed results of the requested action task.
    :param IsErrorDumpNeeded: Optional if you do not need the error dump dataframes that the process may bring.
    :return: A dataframe per error dump found by accessing .error_dumps.
    :rtype: ActionResponse
    """

    controller = TaskController(conn, action_id, retry_count, mapping_params,IsErrorDumpNeeded=IsErrorDumpNeeded)

    return controller.response


# ===========================================================================
# This function queries the Anaplan model for a list of the desired resources:
# files, actions, imports, exports, processes and returns the JSON response.
# ===========================================================================
def get_list(conn: AnaplanConnection, resource: str) -> AnaplanResource:
    """Get list of the specified resource in the Anaplan model

    :param conn: AnaplanConnection object which contains AuthToken object, workspace ID, and model ID
    :type conn: AnaplanConnection
    :param resource: The Anaplan model resource to be queried and returned to the user
    :type resource: str
    :return: Detailed list of the requested resource
    :rtype: AnaplanResource
    """

    resources = Resources(conn=conn, resource=resource)
    resources_list = resources.get_resources()
    resource_parser = ResourceParserList()
    return resource_parser.get_parser(resources_list)


# ===========================================================================
# This function downloads a file from Anaplan to the specified path.
# ===========================================================================
def get_file(conn: AnaplanConnection, file_id: str) -> str:
    """Download the specified file from the Anaplan model

    :param conn: AnaplanConnection object which contains AuthToken object, workspace ID, and model ID
    :type conn: AnaplanConnection
    :param file_id: ID of the Anaplan file to download
    :type file_id: str
    :return: File data from anaplan
    :rtype: str
    """

    file_download = FileDownload(conn=conn, file_id=file_id)
    return file_download.download_file()
