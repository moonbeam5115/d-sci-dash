import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from . queries import query_research_location, query_funding_organizations, query_research_organizations, query_researchers

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/location', methods=['GET'])
def location():
    top_locations = query_research_location()

    return render_template('location/location.html', top_locations=top_locations)

@bp.route('/fund_orgs', methods=['GET'])
def fund_orgs():
    top_fund_orgs = query_funding_organizations()

    return render_template('fund_orgs/fund_orgs.html', top_fund_orgs=top_fund_orgs)

@bp.route('/research_orgs', methods=['GET'])
def research_orgs():
    top_research_orgs = query_research_organizations()

    return render_template('research_orgs/research_orgs.html', top_research_orgs=top_research_orgs)

@bp.route('/researchers', methods=['GET'])
def researchers():
    top_researchers = query_researchers()

    return render_template('researchers/researchers.html', top_researchers=top_researchers)