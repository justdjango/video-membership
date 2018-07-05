Model Architecture Planning

Membership
	-slug
	-type (free, pro, enterprise)
	-price (monthly)
	-stripe plan id

UserMembership
	-user 						(foreignkey to default User)
	-stripe customer id
	-membership type 			(foreignkey to Membership)

Subscription
	-user membership 			(foreignkey to UserMembership)
	-stripe subscription id
	-active

Course
	-slug
	-title
	-description
	-allowed memberships 		(manytomanyfield with Membership)

Lesson
	-slug
	-Course						(foreignkey to Course)
	-position
	-title
	-video
	-thumbnail

