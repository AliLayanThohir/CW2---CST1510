#Class to represent a cybersecurity incident
class SecurityIncident:
    
    #Constructor to initialize the incident 
    def __init__(self, id, date, incident_type, severity, status, description, reported_by, created_at=None):
        self._id = id #ID for the incident
        self.date = date #Date the incident occurred
        self.incident_type = incident_type 
        self.severity = severity 
        self.status = status 
        self.description = description 
        self.reported_by = reported_by 
        self.created_at = created_at 

    #Function to get the incident ID
    def get_id(self):
        return self._id
    
    #Function to get the status of the incident
    def get_status(self):
        return self.status

    #Function to convert object data to a dictionary to be used in dataframe
    def to_dict(self):
        return {
            "id": self._id,
            "date": self.date,
            "incident_type": self.incident_type,
            "severity": self.severity,
            "status": self.status,
            "description": self.description,
            "reported_by": self.reported_by
        }

    #Ticket details
    def __str__(self):
        return f"Incident {self._id}: {self.incident_type}, {self.severity}"