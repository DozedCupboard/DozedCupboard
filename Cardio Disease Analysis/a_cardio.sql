SELECT * FROM ocd_data.cardio;

use ocd_data;

-- Dataset
-- https://www.kaggle.com/code/jocelyndumlao/cardiovascular-health-analysis/input

-- 1) Which gender has the highest number of cardiovascular diease?
-- Male or Female? (1 male, 0 female)

select 
	gender, 
    count(*) as total_people, 
    count(case when target = 0 then 1 end) as no_heart_disease,
    round(avg(case when target = 0 then 1 else 0 end), 2) as percentage_no_heart_disease
from cardio
GROUP BY gender;
-- Conclusion: Men and Women have nearly equal odds of having heart-disease

-- 2) Which age group has the highest percentage of people with heart disease

select
	case 
		when age < 20 then "<20"
        when age between 20 and 30 then "20-30"
        when age between 30 and 40 then "30-40"
        when age between 40 and 50 then "40-50"
        when age between 50 and 60 then "50-60"
        else "60+"
	end as age_group,
    count(*) as people_in_age_group,
    sum(case when target = 1 then 1 end) as count_with_heart_disease,
    avg(case when target = 1 then 1 else 0 end) as percentage_with_heart_disease
from cardio
group by age_group
order by age_group;
-- Conclusion: People in the 40-50 age group have the highest percentage with heart_disease,
-- There is a pattern where the further you are away from this age-group the lower the percentage
-- of people with heart_disease


-- 3) Count the number of patients with each chest_pain type, do chest_pain types affect the likely hood of having
-- a cardiovascular disease?

select 
	chestpain, 
    count(target) as count_with_chestpain,  
    sum(case when target = 1 then 1 end) as count_with_heart_disease, 
    avg(case when target = 1 then 1 else 0 end) as percentage_with_heart_disease
from cardio
group by chestpain
order by chestpain;

-- 4) Group patients by chlorestrol level. Does this affect the likelyhood
-- of having a heart disease.

-- First find the lowest and highest chlorestrol levels to establish a range
-- highest
select serumcholestrol, restingBP, target
from cardio
where serumcholestrol >= 200
order by serumcholestrol desc
limit 10;
-- Highest is 602

-- Lowest
select serumcholestrol, restingBP, target
from cardio
where serumcholestrol <= 200 and serumcholestrol > 0
-- order by restingBP asc 
order by serumcholestrol asc
limit 10;
-- I chosen not to include 0 as a chlorestrol level since it is an impossible level thus invalid
-- (And there were patients with it)
-- The lowest is 85

-- Make chlorestrol level groups between 85 602
select 
    case 
        WHEN serumcholestrol BETWEEN 85 AND 149 THEN '1-Very Low Cholesterol (85-149)'
        WHEN serumcholestrol BETWEEN 150 AND 199 THEN '2-Low Cholesterol (150-199)'
        WHEN serumcholestrol BETWEEN 200 AND 239 THEN '3-Borderline High Cholesterol (200-239)'
        WHEN serumcholestrol BETWEEN 240 AND 299 THEN '4-High Cholesterol (240-299)'
        WHEN serumcholestrol BETWEEN 300 AND 399 THEN '5-Very High Cholesterol (300-399)'
        WHEN serumcholestrol BETWEEN 400 AND 602 THEN '6-Extremely High Cholesterol (400-602)'
        else 'Out of Range'
    end as cholesterol_group,
    count(*) AS patient_count,
    sum(case when target = 1 then 1 end) as count_with_heart_disease, 
    avg(case when target = 1 then 1 else 0 end) as percentage_with_heart_disease
FROM cardio
WHERE serumcholestrol > 0
GROUP BY cholesterol_group
ORDER BY cholesterol_group;
-- Conclusion, The cholesterol data seems inaccurate, as levels above 400 are unusually high
-- and not typical. Generally, doctors categorize cholesterol as less than 200 (healthy), 
-- 200-239 (borderline high), and above 240 (high). 
-- Despite this, extremely high cholesterol is clearly linked to a greater risk of heart disease.




