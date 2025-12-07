#Class to represent a IT support ticket
class ITTicket:
    
    #Constructor to initialize the ticket 
    def __init__(self, id, ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to, created_at=None):
        self._id = id 
        self.ticket_id = ticket_id 
        self.priority = priority 
        self.status = status 
        self.category = category 
        self.subject = subject 
        self.description = description 
        self.created_date = created_date 
        self.resolved_date = resolved_date 
        self.assigned_to = assigned_to 
        self.created_at = created_at 

    #Function to get the ticket ID 
    def get_ticket_id(self):
        return self.ticket_id

    #Function to convert object data to a dictionary to be used in dataframe
    def to_dict(self):
        return {
            "ticket_id": self.ticket_id,
            "priority": self.priority,
            "status": self.status,
            "category": self.category,
            "subject": self.subject,
            "description": self.description,
            "created_date": self.created_date,
            "resolved_date": self.resolved_date,
            "assigned_to": self.assigned_to
        }

    #Ticket details
    def __str__(self):
        return f"Ticket {self.ticket_id}: {self.subject} [{self.status}]"