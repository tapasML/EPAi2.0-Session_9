from datetime import date
import dateutil.parser
from collections import namedtuple
from collections import Counter

file='nyc_parking_tickets_extract-1.csv'
#file='Parking_Violations_Issued_-_Fiscal_Year_2014__August_2013___June_2014_.csv'
data_types = ['INT', 'STR', 'STR', 'STR', 'DATE', 'INT', 'STR', 'STR', 'STR']

def cast(data_type, value):
    
    ''' cast data to appropriate field type'''
    
    if data_type == 'INT':
        return int(value)
    elif data_type == 'STR':
        return str(value)
    elif data_type == 'DATE':
        return dateutil.parser.parse(value).date()       
    else:
        return str(value)
    

def cast_row(data_types, data_row):
    return [cast(data_type, value) 
            for data_type, value in zip(data_types, data_row)]


def read_generator(file):  
    
    ''' read file lines lazily'''
    
    i = 0  
    with open(file) as f:               
        for line in f:            
            if i == 0:   # for (first line) namedtuple attributes names, spaces need to be removed
              line=line.replace(" ", "")
              i+=1                  
            yield line.strip('\n').split(',')
            

def readfile(file):      
        yield from read_generator(file)


def add_ticket(row):     
     row = cast_row(data_types, row)        
     ticket = Ticket(*row)    
     return ticket

def goal_one():      
    global Ticket 
    rows =  readfile(file)     
    header = iter(next(rows)) # iterate one time     
    Ticket = namedtuple('ViolationTicket', header) 
    g = (add_ticket(row) for row in rows)    
    return g

def goal_two():
  violation_tickets = goal_one()
  tickets_by_model=Counter(elem[7] for elem in violation_tickets)
  print(tickets_by_model)
  

def test_goal_one():
  violation_tickets = goal_one()
  for item in violation_tickets:
    print(item)

def test_goal_two():
  goal_two()


test_goal_one()

test_goal_two()