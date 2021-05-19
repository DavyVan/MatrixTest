from typing import Dict, List
import os
import base64

import mailjet_rest as mailjet

from . import EmailProvider


class MailjetProvider(EmailProvider):
    """
    This is the adaptor class for `Mailjet <https://mailjet.com>`_.

    """
    def __init__(self, *, api_key: str, api_secret: str):
        self.client = mailjet.Client(auth=(api_key, api_secret), version='v3.1')        # type: mailjet.Client

    def send(self, matrix: Dict[str, List[str]], to: str, attachment_path: str = None) -> bool:
        # check attached file size
        if attachment_path is not None:
            if os.stat(attachment_path).st_size / 1024 / 1024 >= 15:        # >= 15MB
                print("Attached file is too large.")
                return False

        # generate string from matrix
        body = "Your MatrixTest job has completed. The argument matrix is shown below:\n"
        for k, v in matrix.items():
            body += "%s : %s\n" % (k, v)

        # send
        data = {
            "From": {
                "Email": "matrixtest@funqtion.xyz",
                "Name": "MatrixTest"
            },
            "To": [
                {
                    "Email": to
                }
            ],
            "Subject": "MatrixTest job has completed",
            "TextPart": body
        }
        if attachment_path is not None:
            attachment_fd = open(attachment_path, 'rb')
            data['Attachments'] = [{
                "ContentType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "Filename": os.path.basename(attachment_path),
                "Base64Content": base64.b64encode(attachment_fd.read()).decode()
            }]
        result = self.client.send.create(data={'Messages': [data]})

        if result.status_code != 200:
            print(result.status_code)
            print(result.json())
            return False
        else:
            return True
