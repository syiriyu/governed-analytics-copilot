SQL Syntax notes:

## Need to sum based on a condition in the table?

SUM(column_name) FILTER (WHERE column_name = 'condition')

## Need to rank something by the amount of times it appears?

Select,
  name,
  department,
  salary,
  rank() over(partition by department order by salary desc) as salary_rank -- pick the partition to group by, so we want to rank salary based on department

(note - dense rank doesn't skip numbers if there's a tie)


## Need to calculate a moving average?

ROUND(AVG(tweet_count) OVER (
  partition by user_id
  order by tweet_date
  rows between 2 preceding and current row),1) as rolling_avg

-- so we're calculating the avg tweet count, by tweet date, and outputting the 3 day rolling avg for users by specifying the row time horizon
