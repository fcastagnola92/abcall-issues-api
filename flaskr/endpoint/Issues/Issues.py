from flask_restful import Resource
from flask import jsonify, request
import logging
import requests
from ...application.issue_service import IssueService
from ...infrastructure.databases.issue_postresql_repository import IssueRepository
from http import HTTPStatus
from ...utils import Logger

from config import Config

log = Logger()

class Issue(Resource):

    def __init__(self):
        config = Config()
        self.issue_repository = IssueRepository(config.DATABASE_URI)
        self.service = IssueService(self.issue_repository)


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
            list_issues = [issue.to_dict() for issue in issue_list]
            
            return list_issues, HTTPStatus.OK
        except Exception as ex:
            log.error(f'Some error occurred trying to get issue list: {ex}')
            return {'message': 'Something was wrong trying to get issue list'}, HTTPStatus.INTERNAL_SERVER_ERROR
        
