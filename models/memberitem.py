class MemberItem:

    #change this accordingly
    def __init__(self="", id="", name="", department="", college="", email="", interests="", domains=""):
        self.id = id # maybe unnecessary?
        self.name = name
        self.department = department
        self.college = college
        self.email = email
        self.interests = interests
        self.domains = domains

    def toJson(self):
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'college': self.college,
            'email': self.email,
            'interests': self.interests,
            'domains': self.domains
        }