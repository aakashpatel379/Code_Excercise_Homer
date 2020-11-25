-- Part 1 Query
CREATE TABLE itunes_subscription
(
    id integer NOT NULL PRIMARY KEY,
    transactions JSON,
    trial_start_date date,
    subscription_start_date date,
    expiration_date date NOT NULL,
    current_status varchar(255)
);

-- Part 3 Query
select current_status,count(current_status)
from itunes_subscription
group by current_status;
