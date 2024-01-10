# Django Backend Coding Challenge

## Requirements
- You don’t need to add anything else to the serialize method. Assume the client only needs the id, title, description, and also needs to know whether a Quest was completed or not.
- You can assume that the table holds all information for one user (eg. no need to differentiate between users)
- You don’t need to worry about migrating existing data over. Assume that we purge the database and re-create it with your new system.
- Code doesn’t need to compile as long as the logic makes sense.
- If you prefer, feel free to convert the views into a DRF ViewSet.

## Quest Behaviors

- General Quests should always appear in the get_quests response, until it gets completed. On the date that it is completed, the completed field should be True. On dates before the completion date, the completed field should be False.

- Repeating Quests should only appear when the date queried is on a day that it is supposed to repeat (see the weekday() function in datetime). If the Quest has been completed that day, completed should be True. If it hasn’t been completed on that day, completed should be False


## Results

To ensure the Quest behavior logic was working as intended, I add test cases for both the `views` and `models` files

### Testing


```commandline
python manage.py test
```
