Model Architecture planning

Membership
	-slug
	-type (free, pro, enterprise)
	-price
	-stripe plan id

UserMembership
	-user 						(foreignkey to default user)
	-stripe customer id
	-membership type			(foreignkey to Membership)

Subscription
	-user membership
	-stripe subscription id 	(foreignkey to UserMembership)
	-active

Course
	-slug
	-title
	-description
	-allowed memberships		(foreignkey to Membership)

Lesson
	-slug
	-title
	-Course 					(foreignkey to Course)
	-position
	-video
	-thumbnail