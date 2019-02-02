-- 1a. Display the first and last names of all actors from the table actor.
SELECT first_name, last_name FROM sakila.actor;

-- 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.
SELECT upper(concat(first_name, ' ', last_name )) as 'Actor Name' FROM sakila.actor;

-- You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." 
-- What is one query would you use to obtain this information?
Select * from sakila.actor
where first_name = 'JOE';

-- 2b. Find all actors whose last name contain the letters GEN:
Select * from sakila.actor
where last_name like '%GEN%';

-- Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:
Select * from sakila.actor
where last_name like '%LI%'
order by last_name, first_name;

-- Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
Select country_id, country  from sakila.country
where country in ('Afghanistan', 'Bangladesh', 'China');

-- You want to keep a description of each actor. You don't think you will be performing queries on a description,
-- so create a column in the table actor named description and use the data type BLOB (Make sure to research the type BLOB, 
-- as the difference between it and VARCHAR are significant).
alter table sakila.actor
	add column description blob;
    
select * from sakila.actor;

-- 3b. Very quickly you realize that entering descriptions for each actor is too much effort. Delete the description column.
alter table sakila.actor
	drop column description;
    
select * from sakila.actor;

-- 4a. List the last names of actors, as well as how many actors have that last name.
Select  last_name, count(*) from sakila.actor
	group by last_name;

-- 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors
Select  last_name, count(*) as count from sakila.actor
	group by last_name having count > 1;

-- 4c. The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS. Write a query to fix the record.
update sakila.actor 
	set first_name = 'HARPO'
    where first_name = 'GROUCHO'
    and last_name = 'WILLIAMS';
select * from sakila.actor
	where first_name = 'HARPO'
    and last_name = 'WILLIAMS';

-- Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all! In a single query, 
-- if the first name of the actor is currently HARPO, change it to GROUCHO.
update sakila.actor 
	set first_name = 'GROUCHO'
    where first_name = 'HARPO';
select * from sakila.actor
	where first_name = 'GROUCHO';

-- 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?
SHOW CREATE TABLE sakila.address;

-- Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:
select first_name, last_name, address
	from sakila.staff staff,  sakila.address address
    where staff.address_id = address.address_id;

-- 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment.
select first_name, last_name, sum(amount) as "Total_Amount"
from  sakila.staff staff,  sakila.payment payment
	where staff.staff_id = payment.staff_id
    and payment.payment_date between '2005-08-01' and '2005-08-31'
    group by 1,2;

-- 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.    
select film.title, count(*) as "Number of Actors"
	from sakila.film, sakila.film_actor
    where film.film_id = film_actor.film_id
    group by 1;

-- How many copies of the film Hunchback Impossible exist in the inventory system?
select film.title, count(*) as 'Number of Copies'
from sakila.film as film, sakila.inventory inventory
where film.title = "Hunchback Impossible"
and film.film_id = inventory.film_id
group by film.title;

-- 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. 
-- List the customers alphabetically by last name:
select first_name, last_name, sum(amount) as "Total Amount Paid"
from  sakila.customer ,  sakila.payment 
	where customer.customer_id = payment.customer_id
    group by 1,2 order by 2;
    
-- 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, 
-- films starting with the letters K and Q have also soared in popularity. Use subqueries to display the titles 
-- of movies starting with the letters K and Q whose language is English.

Select title from sakila.film
where title in (
				select title from sakila.film, sakila.language
					where language.name = 'English'
                    and language.language_id = film.language_id
                    and (film.title like 'K%'
                    or film.title like 'Q%'));
                    
-- 7b. Use subqueries to display all actors who appear in the film Alone Trip.
select first_name, last_name from sakila.actor
where actor_id in (
					select actor_id from sakila.film_actor, sakila.film
						where film.title = "Alone Trip"
                        and film.film_id = film_actor.film_id);
                        
-- 7c. You want to run an email marketing campaign in Canada, for which you will need the names 
-- and email addresses of all Canadian customers. Use joins to retrieve this information.
select first_name, last_name, email
	from sakila.customer, sakila.address, sakila.city, sakila.country
    where customer.address_id = address.address_id
    and address.city_id = city.city_id
    and city.country_id = country.country_id
    and country.country = 'Canada';
-- with subquery    
select first_name, last_name, email
	from sakila.customer
    where address_id in (
						select address_id from sakila.address
							where city_id in (

												select city_id from sakila.city, sakila.country
													where city.country_id = country.country_id
													and country.country = 'Canada'));
                                                    
-- 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. 
-- Identify all movies categorized as family films.
Select title from 
	sakila.film, sakila.film_category, sakila.category
    where film.film_id = film_category.film_id
    and film_category.category_id = category.category_id
    and name = 'Family';
    
-- 7e. Display the most frequently rented movies in descending order.
Select f.title from sakila.film f,sakila.rental r, sakila.inventory i 
	where f.film_id = i.film_id
    and i.inventory_id = r.inventory_id
    order by r.rental_date desc;
    
-- 7f. Write a query to display how much business, in dollars, each store brought in.
select sto.store_id, sum(pay.amount) as 'Total Amount'
	from sakila.store sto, sakila.payment pay, sakila.staff sta
    where pay.staff_id = sta.staff_id
    and sta.store_id = sto.store_id
    group by 1;

-- 7g. Write a query to display for each store its store ID, city, and country.
Select sto.store_id, ct.city, co.country
	from sakila.store sto, sakila.address addr, sakila.city ct, sakila.country co
    where sto.address_id = addr.address_id
    and addr.city_id = ct.city_id
    and ct.country_id = co.country_id;
    
-- 7h. List the top five genres in gross revenue in descending order. 
-- (Hint: you may need to use the following tables: category, film_category, inventory, payment, and rental.)
Select cat.name Genres, sum(pay.amount) as 'Gross Revenue'
	from sakila.payment pay, sakila.rental rnt, sakila.inventory inv,
		sakila.film_category as fcat, sakila.category as cat
	where pay.rental_id = rnt.rental_id
    and rnt.inventory_id = inv.inventory_id
    and inv.film_id = fcat.film_id
    and fcat.category_id = cat.category_id
    group by 1 
    order by 2 desc
    limit 5;

-- 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. 
-- Use the solution from the problem above to create a view. If you haven't solved 7h, you can substitute another query to create a view.

create view sakila.top_five_genres as 
Select cat.name Genres, sum(pay.amount) as 'Gross Revenue'
	from sakila.payment pay, sakila.rental rnt, sakila.inventory inv,
		sakila.film_category as fcat, sakila.category as cat
	where pay.rental_id = rnt.rental_id
    and rnt.inventory_id = inv.inventory_id
    and inv.film_id = fcat.film_id
    and fcat.category_id = cat.category_id
    group by 1 
    order by 2 desc
    limit 5;

-- 8b. How would you display the view that you created in 8a?    
select * from sakila.top_five_genres;

-- 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.

drop view sakila.top_five_genres;