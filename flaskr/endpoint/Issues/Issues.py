from flask_restful import Resource
from flask import jsonify, request
import logging
import requests
from ...application.issue_service import IssueService
from ...infrastructure.databases.issue_postresql_repository import IssuePostgresqlRepository
from http import HTTPStatus
from ...utils import Logger

from config import Config

log = Logger()

class Issue(Resource):

    def __init__(self):
        config = Config()
        self.issue_repository = IssuePostgresqlRepository(config.DATABASE_URI)
        self.service = IssueService(self.issue_repository)

    def post(self,action=None):
        try:
            log.info(f"Receive request to create a new issue")

            data = request.get_json()
            auth_user_id = data.get("auth_user_id")
            auth_user_agent_id = data.get('auth_user_agent_id')
            subject = data.get("subject")
            description = data.get("description")

            issue_id = self.service.create_issue(
                auth_user_id=auth_user_id,
                auth_user_agent_id=auth_user_agent_id,
                subject=subject,
                description=description
            )

            return {"message": f"Issue created successfully with ID {issue_id}"}, HTTPStatus.CREATED

        except Exception as ex:
            log.error(f"Error while creating issue: {ex}")
            return {"message": "Error creating issue"}, HTTPStatus.INTERNAL_SERVER_ERROR

    def get(self, action=None):
        if action == 'getIssuesByCustomer':
            return self.getIssuesByCustomer()
        else:
            return {"message": "Action not found"}, 404
    
    def getIssuesByCustomer(self):
        try:

            log.info(f'Receive request to get issues by customer')
            customer_id = request.args.get('customer_id')
            year = request.args.get('year')
            month = request.args.get('month')
            issue_list = self.service.list_issues_period(customer_id=customer_id,year=year,month=month)
            list_issues=[]
            if issue_list:
                list_issues = [issue.to_dict() for issue in issue_list]

            
            return list_issues, HTTPStatus.OK
        except Exception as ex:
            log.error(f'Some error occurred trying to get issue list: {ex}')
            return {'message': 'Something was wrong trying to get issue list'}, HTTPStatus.INTERNAL_SERVER_ERROR
        
