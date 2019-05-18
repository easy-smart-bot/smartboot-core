#!/usr/bin/env

import json
import ibm_watson

NAMEFILE_CREDENTIALS='credentials.json'
NAMEFILE_BACKUP='backup.json'

class ibm_credentials:

    def __init__(
            self, version=None, iam_apikey=None, url=None, workspace_id=None,
            credentials_file=None
        ):

        print("READING CREDENTIALS")
        if credentials_file is not None:

            print("READING FILE")
            self.load_ibm_credentials(credentials_file)

        else:
            self.version = version
            self.iam_apikey = iam_apikey
            self.url = url
            self.workspace_id = workspace_id


    def load_ibm_credentials(self, credentials_file=NAMEFILE_CREDENTIALS ):

        with open(credentials_file, 'r') as opened_file:

            data = opened_file.read()
            print(data)

            credentials_data = json.loads( data )

            self.version = credentials_data['version']
            self.iam_apikey = credentials_data['iam_apikey']
            self.url = credentials_data['url']
            self.workspace_id = credentials_data['workspace_id']


class ibm_instance:

    def __init__(self, credentials=None):

        print("CREATING IBM INSTANCE")

        if credentials is not None:

            self.service = ibm_watson.AssistantV1(
                version = credentials.version,
                iam_apikey = credentials.iam_apikey,
                url = credentials.url
            )

            self.workspace_id = credentials.workspace_id

    def create_backup(self):

        self.response = self.service.get_workspace(
                    workspace_id = self.workspace_id,
                        export=True
                        ).get_result()

    def write_backup(self, namefile=NAMEFILE_BACKUP):

        with open(namefile, 'w') as opened_file:
            opened_file.write( json.dumps(self.response, indent=2))



if __name__ == "__main__":

    my_credentials = ibm_credentials( credentials_file = NAMEFILE_CREDENTIALS)
    my_instance = ibm_instance( my_credentials )
    my_instance.create_backup()
    my_instance.write_backup()

