from datetime import datetime

from .database.models.models import Opportunity, Scholarship, Resource
# from models import db, Opportunity, Scholarship, Resource

def allDateDisplay():
     opportunities = Opportunity.query.order_by(Opportunity.datePosted.desc()).all()
     dateDict = {}
     for opportunity in opportunities:
          temp = []
          if (opportunity.startDate):
               temp.append(opportunity.startDate.strftime("%B %d, %Y"))
          if (opportunity.endDate):
               temp.append(opportunity.endDate.strftime("%B %d, %Y"))
          if (opportunity.deadline):
               temp.append(opportunity.deadline.strftime("%A, %B %d, %Y"))
          dateDict[opportunity.opportunityID] = temp
     return dateDict 

def dateDisplay(opportunityID):
     opportunity = Opportunity.query.filter_by(
         opportunityID=opportunityID).first()
     dateList = []
     if (opportunity.startDate):
          dateList.append(opportunity.startDate.strftime("%B %d, %Y"))
     if (opportunity.endDate):
          dateList.append(opportunity.endDate.strftime("%B %d, %Y"))
     if (opportunity.deadline):
          dateList.append(opportunity.deadline.strftime("%A, %B %d, %Y"))
     return dateList

def allDateDisplayS():
     scholarships = Scholarship.query.order_by(Scholarship.datePosted.desc()).all()
     dateDict = {}
     for scholarship in scholarships:
          if (scholarship.deadline):
               dateDict[scholarship.scholarshipID] = scholarship.deadline.strftime("%A, %B %d, %Y")
     return dateDict

def dateDisplayS(scholarshipID):
     scholarship = Scholarship.query.filter_by(scholarshipID=scholarshipID).first()     
     dateList = []
     if (scholarship.deadline):
          dateList.append(scholarship.deadline.strftime("%A, %B %d, %Y"))
     return dateList
