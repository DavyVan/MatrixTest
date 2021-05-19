import abc
from typing import Dict, List


class EmailProvider:
    """
    This is the base class of all email sending services. User can extend this abstract class to connect other email services.

    """
    @abc.abstractmethod
    def send(self, matrix: Dict[str, List[str]], to: str, attachment_path: str = None) -> bool:
        """
        Send the email.

        :param matrix: The argument matrix will be included in the email for reference.
        :param to: The recipient.
        :param attachment_path: The Excel file.
        :return: if the sending is successfully executed. Returning ``True`` does NOT mean the email has already been delivered,
            the meaning of return value may vary across difference email service platforms.
        """
        pass
