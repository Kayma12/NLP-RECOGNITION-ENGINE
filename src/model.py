########################################################################################################################
### Creating a Consultant object, e.g.
### a_consultant = Consultant('Gertrude', 'Wilson', 'developer', {'Java' : 3, 'Python' : 9, 'HTML5' : 2, 'CSS3' : 2}, <availability = True>)
### a_consultant.__repr__() returns a dictionary of the form:
### {
###  'name': {'first_name': 'Gertrude', 'last_name': 'Wilson'},
###  'stream': 'developer',
###  'skills': {'Java' : 3, 'Python' : 9, 'HTML5' : 2, 'CSS3' : 2},,
###  'availability': True
### }
###
### a_consultant.__str__() returns a string representation of the object.
########################################################################################################################

class Consultant:

    def __init__(self, first_name, last_name, stream, skills, availability = True):
        self.name = {'first_name' : first_name, 'last_name' : last_name}
        self.stream = stream
        self.skills = skills
        self.availability = availability

    def __repr__(self):
        return {'name' : self.name, 'stream' : self.stream, 'skills' : self.skills, 'availability' : self.availability}

    def __str__(self):
        return '''Consultant:
                   name: {} {}, 
                   stream : {}, 
                   skills : {}, 
                   availability : {}'''.format(self.name['first_name'], self.name['last_name'], self.stream, self.skills, self.availability)