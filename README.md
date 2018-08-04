# Database

Database is an easy to use dot-notation chaining class in Python to easily build MySQL queries easily and efficiently.

## Example

To build a query, simply do the following:

```
from database import DB
    
# Create new DB class
db = DB('main')
    
# Build query, get results
results = db.table('users')
            .select('*')
            .where('age < 30')
            .where('rank > 20')
            .orWhere('nickname = "John"')
            .where('nickname != "Peter"')
            .orderByAsc('created_by')
            .orderByDesc('name')
            .get()
    
# Parse Results            
for result in results:
    pprint.pprint(result['name'])

```
