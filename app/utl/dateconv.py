from datetime import datetime

from .models import db, Opportunity

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
