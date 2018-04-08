
import httplib2
import os

# apiclient is an alias for googleapiclient
from apiclient import discovery
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from io import FileIO
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

"""
Majority of code borrowed from python quickstart:
https://developers.google.com/drive/v3/web/quickstart/python

--------
The scope was originally:
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'

To update the scope, delete the old credentials file in the terminal:
rm ~/.credentials/drive-python-quickstart.json

Below scope allows for permissions beyond readonly:
SCOPES = 'https://www.googleapis.com/auth/drive'
"""

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    """Adds pdf files to Google Drive folder and downloads their text representations.

    Returns:
        Nothing, local folder will be populated with text files
    """

    # authorize access and create Google Drive API service object

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=http)

    # retrieve the file ID of a folder called Operating_Reports
    # below code based off of https://developers.google.com/drive/v3/web/search-parameters

    response = drive_service.files().list(q="name='Operating_Reports'", spaces='drive',
                                          fields='files(id, name)').execute()
    file = response.get('files', [])[0]
    folder_id = file.get('id')
    print('Found file: {0} ({1})'.format(file.get('name'), folder_id))

    reports_dir = "../data/operating_reports/pdf_files/"
    dest_dir = "../data/operating_reports/text_files/"

    # convert each pdf file in reports_dir to a txt file
    for item in os.listdir(reports_dir):

        file_path = reports_dir + item
        file_name = item[:-4]

        # upload pdf file to folder and convert to google doc
        # below code based off of https://developers.google.com/drive/v3/web/manage-uploads

        file_metadata = {
            'name': file_name,
            'mimeType': 'application/vnd.google-apps.document',
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path, mimetype='application/pdf')
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = file.get('id')
        print('File ID: {0}'.format(file_id))

        # download converted google doc as text file
        # below code based off of https://developers.google.com/drive/v3/web/manage-downloads
        # https://stackoverflow.com/questions/36173356/google-drive-api-download-files-python-no-files-downloaded

        file_dest = dest_dir + file_name + ".txt"

        request = drive_service.files().export_media(fileId=file_id, mimeType='text/plain')
        fh = FileIO(file_dest, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

    print('Files Successfully Converted')

if __name__ == '__main__':
    main()