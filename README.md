# overbond dev test submission

## Installation & Usage
```
git clone
cd overbond-dev-test-submission
pip install -r requirements.txt
```
- Move csv file into same directory
```
python app.py
csv name (with.csv): <filename goes here>
```

## testing
```pytest test.py```
## external libraries
- **scipy** and it's dependencies
    - has a built in interpolation method, this is much more reliable than implementing interpolation from scratch
    - Depending on the degree of size and precision of a bond's year, naively calculating the line equation could result in rounding error

### How I stored bond info
**Nested Dictionary**
```{"C1":"term": 0, "year":0}```
- Handles general data better, e.g more bond types, and non contiguous bond names e.g "C1, C8, C20" 

**List Dictionary**
``````["term": 0, "year":0]``````
- Can completely forgo bond names because of the way the data is currently formatted i.e contiguous names
- Implementing interpolation from scratch is less verbose compared to using a nested dictionary

- I decided to use a nested dictionary to make the code more extensible to future datasets that might not be as well formed 
- Future Changes:
 - I think using a pandas dataframe would make the logic even more succinct and explicit 
 - Test against more edge cases i.e empty ds, 'ill-formatted' dataset