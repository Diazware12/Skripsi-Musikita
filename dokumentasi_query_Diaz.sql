CTE buat product_page

with 
	avgUser as(
		select 
			FORMAT (avg(r.rating), 1) as user_avg,
			p.productId as productId
		from review_review as r
		join register_user as u on r.userID_id = u.userID
		join product_product as p on r.productId_id = p.productId
		where u.roleId like "%Reg_User%" and p.productId=23),

	avgMusStore as(
		select 
			FORMAT (avg(r.rating), 1) as Mus_store_avg,
			p.productId as productId
		from review_review as r
		join register_user as u on r.userID_id = u.userID
		join product_product as p on r.productId_id = p.productId
		where u.roleId like "%Mus_Store%" and p.productId=23),
    
    statsUser as (
        select 
 		FORMAT((
			(select count(*) from review_review as r
			join register_user as u on r.userID_id = u.userID
			where u.roleId like "%Reg_User%" and productId_id = 23 and r.rating < 10 and r.rating >=8)
            /(count(u.userID))
            *100
        ),0) as positive_user,
 		FORMAT((
			(select count(*) from review_review as r
			join register_user as u on r.userID_id = u.userID
			where u.roleId like "%Reg_User%" and productId_id = 24 and r.rating < 8 and r.rating >=5)
            /(count(u.userID))
            *100
        ),0) as mixed_user,
 		FORMAT((
			(select count(*) from review_review as r
			join register_user as u on r.userID_id = u.userID
			where u.roleId like "%Reg_User%" and productId_id = 23 and r.rating < 5 and r.rating >=0)
            /(count(u.userID))
            *100
        ),0) as negative_user,
		p.productId as productId
		from review_review as r
		join register_user as u on r.userID_id = u.userID
		join product_product as p on r.productId_id = p.productId
		where u.roleId like "%Reg_User%" and p.productId = 23
    ),

    statsMusStore as (
		select 
			FORMAT((
				(select count(*) from review_review as r
				join register_user as u on r.userID_id = u.userID
				where u.roleId like "%Mus_Store%" and productId_id = 23 and r.rating < 10 and r.rating >=8)
				/(count(u.userID))
				*100
			),0) as positive_ms,
			FORMAT((
				(select count(*) from review_review as r
				join register_user as u on r.userID_id = u.userID
				where u.roleId like "%Mus_Store%" and productId_id = 23 and r.rating < 8 and r.rating >=5)
				/(count(u.userID))
				*100
			),0) as mixed_ms,
			FORMAT((
				(select count(*) from review_review as r
				join register_user as u on r.userID_id = u.userID
				where u.roleId like "%Mus_Store%" and productId_id = 23 and r.rating < 5 and r.rating >=0)
				/(count(u.userID))
				*100
			),0) as negative_ms,
			p.productId as productId
			from review_review as r
			join register_user as u on r.userID_id = u.userID
			join product_product as p on r.productId_id = p.productId
			where u.roleId like "%Mus_Store%" and p.productId = 23
    )    
    
select user_avg, Mus_store_avg, positive_user, mixed_user, negative_user, positive_ms, mixed_ms, negative_ms
from avgUser join avgMusStore using (productId)
join statsUser using (productId)
join statsMusStore using (productId)

