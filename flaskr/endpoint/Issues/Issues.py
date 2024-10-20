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

    def get(self, action=None):
        if action == 'getIssuesByCustomer':
            return self.getIssuesByCustomer()
        elif action == 'getIssuesDasboard':
            return self.getIssuesDasboard()
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
    
    def listIssuesFiltered(self, status=None, channel_plan_id=None, created_at=None, closed_at=None):
        query = self.session.query(Issue)

        if status:
            query = query.filter(Issue.status == status)
        if channel_plan_id:
            query = query.filter(Issue.channel_plan_id == channel_plan_id)
        if created_at:
            query = query.filter(Issue.created_at >= created_at)
        if closed_at:
            query = query.filter(Issue.closed_at <= closed_at)

        return query.all()

    def getIssuesDasboard(self):
        try:
            log.info(f'Receive request to get issues')
            
            customer_id = request.args.get('customer_id')
            status = request.args.get('status')
            channel_plan_id = request.args.get('channel_plan_id')
            created_at = request.args.get('created_at')
            closed_at = request.args.get('closed_at')

            issue_list = self.service.list_issues_filtered(
                customer_id=customer_id,
                status=status,
                channel_plan_id=channel_plan_id,
                created_at=created_at,
                closed_at=closed_at
            )

            list_issues = []
            if issue_list:
                list_issues = [issue.to_dict() for issue in issue_list]

            return list_issues, HTTPStatus.OK

        except Exception as ex:
            log.error(f'Error trying to get issue list: {ex}')
            return {'message': 'Something went wrong trying to get the issue dashboard'}, HTTPStatus.INTERNAL_SERVER_ERROR