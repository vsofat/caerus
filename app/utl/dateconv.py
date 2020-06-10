from datetime import datetime

from .models import db, Opportunity

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
