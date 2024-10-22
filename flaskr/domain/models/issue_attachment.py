from uuid import UUID

class IssueAttachment:
    def __init__(self, id: UUID, issue_id: UUID, file_path: str):
        self.id = id
        self.issue_id = issue_id
        self.file_path = file_path

    def to_dict(self):
        return {
            'id': str(self.id),
            'issue_id': str(self.issue_id),
            'file_path': str(self.file_path),
        }