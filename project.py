import cx_Oracle
import sys
import random
import time

# Connects to the database and returns the connection object
def getConnection():
	f = open('connection.txt')
	username = f.readline().strip()
	password = f.readline().strip()
	f.close()
	try:
		return cx_Oracle.connect(username, password, "gwynne.cs.ualberta.ca:1521/CRS")

	except cx_Oracle.DatabaseError as exc:
		error = exc.args
		print(sys.stderr, "Oracle code:", error.code)
		print(sys.stderr, "Oracle message:", error.message)
		sys.exit()

# Asks the user if they want to login, create an account, or exit
# and call login(), createAccount(), or exit() appropriatly
# Returns a tuple (a, b) where A is a boolean representing
# whether a new account was created or not, and B is the users user_id
def loginOrCreatePrompt(connection):
	while (True):
		inp = input("Type 'login' to login, 'create' to create an account, or 'exit' to exit: ")
		if inp == "exit":
			connection.close()
			sys.exit()
		elif inp == "login":
			user_id = login(connection)
			if (user_id == False):
				print("Invalid user id/password.")
			else:
				print("Successfully logged in.")
				return (False, user_id)
		elif inp == "create":
			user_id = createAccount(connection)
			connection.commit()
			print("Successfully created an account and logged in.")
			return (True, user_id)
		else:
			print("Unrecognized input, please try again.")

# Trys to log in using a user id and password
# On success returns the user id, else returns false
def login(connection):
	while (True):
		user_id = input("Please input your user id: ")
		try:
			user_id = int(user_id)
			break
		except ValueError:
			print("User id must be an integer.")
	user_password = input("Please input your password: ")
	curs = connection.cursor()
	curs.prepare("select * from users where usr = :id and pwd = :password")
	curs.execute(None, {'id':user_id, 'password':user_password})
	if curs.fetchone():
		curs.close()
		return user_id
	else:
		curs.close()
		return False

# Creates a new account and returns the user id given by the system
def createAccount(connection):
	user_name = ""
	user_email = ""
	user_city = ""
	user_timezone = 0
	user_password = ""
	user_id = random.randrange(-2147483648, 2147483647) #-2^31 to (2^31)-1
	while (True):
		user_name = input("Please input a name: ")
		if len(user_name) > 20:
			print("Maximum length of name is 20.")
		else:
			break
	while (True):
		user_email = input("Please enter an email: ")
		if len(user_email) > 15:
			print("Maximum length of email is 15.")
		else:
			break
	while (True):
		user_city = input("Please enter a city: ")
		if len(user_city) > 12:
			print("Maximum length of city is 12.")
		else:
			break
	while (True):
		user_timezone = input("Please enter a timezone: ")
		try:
			user_timezone = float(user_timezone)
			break
		except ValueError:
			print("Timezone must be a float.")
	while (True):
		user_password = input("Please enter a password: ")
		if len(user_password) > 4:
			print("Maximum length of password is 4.")
		else:
			break

	# Check that the user id is unique
	while (True):
		curs = connection.cursor()
		curs.prepare("select * from users where usr = :id")
		curs.execute(None, {'id':user_id})
		if curs.fetchone():
			user_id = random.randrange(-2147483648, 2147483647)
			curs.close()
		else:
			print("User id is: ", user_id)
			curs.close()
			break

	curs = connection.cursor()
	curs.prepare("insert into users values (:id, :pwd, :name, :email, :city, :timezone)")
	curs.execute(None, {'id':user_id, 'pwd':user_password, 'name':user_name, 'email':user_email, 'city':user_city, 'timezone':user_timezone})
	curs.close()
	connection.commit()
	return user_id

# Displays all tweets and retweets from users that user_id follows
# Also asks the user if they want to see more information about a tweet
def displayTweetsAndRetweets(connection, user_id):
	rows = getTweetsFromFollowedUsers(connection, user_id)
	if len(rows) > 0:
		print("Tweets/retweets from the users you follow:")
		i = 1
		indices = []
		while (True):
			indices.append(i)
			print(i, rows[i-1])

			# Either 5 tweets/retweets have been printed or we have reached the end of the tweets/retweets
			if ((i%5) == 0) or (len(rows) == i):
				inp = ""
				while (True):
					# Check if we have reached the end of the tweets/retweets
					if len(rows) == i:
						# Check if a full 5 tweets/retweets were printed
						if (i%5) == 0:
							inp = input("Type numbers %s-%s to view more information about the tweet, "
							"or 'skip' to skip viewing the tweets: " % ((i-4), i))
						# Check if only a single tweet/retweet was printed
						elif (i%5) == 1:
							inp = input("Type number %s to view more information about the tweet, "
							"or 'skip' to skip viewing the tweets: " % (i))
						# Either 2, 3, or 4 tweets/retweets were printed
						else:
							inp = input("Type numbers %s-%s to view more information about the tweet, "
							"or 'skip' to skip viewing the tweets: " % ((i-(i%5)), i))

						# Check if the input is an int representing 1 of the tweets/retweets
						try:
							if int(inp) in indices:
								break
						except:
							pass
						if inp == "skip":
							break
						else:
							print("Unrecognized input, please try again.")

					# There are still more tweets/retweets to display so offer to display the next ones aswell
					else:
						inp = input("Type numbers %s-%s to view more information about the tweet, "
						"'more' to view the next 5 tweets, or 'skip' to skip viewing the tweets: " % ((i-4), i))

						# Check if the input is an int representing 1 of the tweets/retweets
						try:
							if int(inp) in indices:
								break
						except:
							pass
						if inp == "skip" or inp == "more":
							break
						else:
							print("Unrecognized input, please try again.")
				if inp == "skip":
					break
				elif inp == "more":
					indices = []
				# A tweet was selected
				else:
					displayTweetStats(connection, user_id, rows[int(inp)-1][0])
					indices = []
					if i%5 == 0:
						i = i-5
					else:
						i = i - (i%5)
			i = i + 1
	else:
		print("No tweets/retweets from users you follow.")

# Returns all tweets/retweets from users that the logged in user follows
def getTweetsFromFollowedUsers(connection, user_id):
	curs = connection.cursor()
	curs.prepare("select * from "
				"((select t.tid, t.writer, t.tdate, t.text, t.replyto "
				"from follows f, tweets t "
				"where f.flwer = :id and t.writer = f.flwee) "
				"union (select t.tid, t.usr as writer, t.rdate as tdate, ot.text, ot.replyto "
				"from follows f, retweets t, tweets ot "
				"where f.flwer = :id and t.usr = f.flwee and t.tid = ot.tid)) "
				"order by tdate desc")
	curs.execute(None, {'id':user_id})
	rows = curs.fetchall()
	curs.close()
	return rows

def displayTweetStats(connection, user_id, tweet_id):
	stats = getTweetStats(connection, tweet_id)
	print(stats)

	inp = ""
	while(True):
		inp = input("Type 'reply' to reply to the tweet, 'retweet' to retweet the tweet, "
		"or 'back' to return to the last screen: ")
		if inp != "reply" and inp != "retweet" and inp != "back":
			print("Unrecoginzed input, please try again")
		else:
			break
	if inp == "reply":
		text = ""
		while(True):
			text = input("Enter the text of your tweet: ")
			if len(text) > 80:
				print("Maximum length of tweet text is 80 characters, please try again.")
			else:
				break
		composeTweet(connection, user_id, text, tweet_id)
	elif inp == "retweet":
		retweet(connection, user_id, tweet_id)

# Returns the number of retweets and replies for the tweet
def getTweetStats(connection, tweet_id):
	curs = connection.cursor()
	curs.prepare("select tid, writer, tdate, text, replyto, (select nvl(count(*), 0) from tweets where replyto = :tid1) as num_tweets, "
		"(select nvl(count(*), 0) from retweets where tid = :tid2) as num_retweets from tweets where tid = :tid3")
	curs.execute(None, {'tid1':tweet_id, 'tid2':tweet_id, 'tid3':tweet_id})
	row = curs.fetchone()
	curs.close()
	return row

# Return the followers that the selected user followed
def searchAllFollowers(connection, user_id):

	curs = connection.cursor()
	curs.prepare("select *  from  follows "
				"where flwer = :usr ")
	curs.execute(None, {'usr':user_id})
	rows = curs.fetchall()
	curs.close()
	return rows

#returning to follwing status, that is, when you select a user, you can follow this user
#each user can only be follwed by once.
#once followed the user, the comman should be: "successfully followed"
def followUsers(connection,flwee,user_id):
	#user_id = searchAllFollowers(connection,user_id)

	curs = connection.cursor()
	curs.prepare("select  * from  follows where  (flwer = :flwer and  flwee =:flwee)")
	curs.execute(None, {'flwer':user_id, 'flwee':flwee})
	rows = curs.fetchall()
	if ( len(rows) > 0) :
		print( "you have already followed this user")
	else :
		curs.prepare("insert into follows values (:flwer, :flwee, :start_date)")
		curs.execute(None, {'flwer':user_id, 'flwee':flwee, 'start_date':time.strftime("%d-%b-%Y")})
		print("Successfully followed")
	curs.close()
	connection.commit()

#the list followers function. when typing in the termial"search followers", it should be a list of followers
#that following the user you logged in. Once you select a follower,you can see informations about the user,
#and also have the option to follow this user.
def displayAllFollowers(connection,user_id):

	rows = searchAllFollowers(connection,user_id)

	if len(rows) > 0:
		print("Followers list,please choose:")
		i = 1
		indices = []
		while (True):
			indices.append(i)
			print(i, rows[i-1])

			# Either 5 Followers have been printed or we have reached the end of the users
			if ((i%5) == 0) or (len(rows) == i):
				inp = ""
				while (True):
					# Check if we have reached the end of the followers
					if len(rows) == i:
						# Check if a full 5 followers were printed
						if (i%5) == 0:
							inp = input("Type numbers %s-%s to view more information about the follower, "
								    " or ' 'skip' to skip viewing the follower: " % ((i-4), i))
						# Check if only a single follower was printed
						elif (i%5) == 1:
							inp = input("Type number %s to view more information about the follower, "
							 "or 'skip' to skip viewing the follower: " % (i))
						# Either 2, 3, or 4 follower were printed
						else:
							inp = input("Type numbers %s-%s to view more information about the follower, "
							"or 'follow' to follow the user:" % ((i-(i%5)), i))

						# Check if the input is an int representing 1 of the follower
						try:
							if int(inp) in indices:
								break
						except:
							pass
						if inp == "skip"  :
							break
						else:
							print("Unrecognized input, please try again.")

					# There are still more follower to display so offer to display the next ones aswell
					else:
						inp = input("Type numbers %s-%s to view more information about the follower, "
						"'more' to view the next 5 user, or 'skip' to skip viewing the follower: " % ((i-4), i))

						# Check if the input is an int representing 1 of the follower
						try:
							if int(inp) in indices:
								break
						except:
							pass
						if inp == "skip" or inp == "more":
							break
						else:
							print("Unrecognized input, please try again.")
				if inp == "skip":
					break
				elif inp == "more":
					indices = []
				#elif inp == "follow":
				#	followUsers(connection, rows[i-1][1],user_id)
				#	break
				# A user was selected
				else:
					displayUserStats(connection,  rows[int(inp)-1][1],user_id)
					indices = []
					if i%5 == 0:
						i = i-5
					else:
						i = i - (i%5)
			i = i + 1
	else:
		print("No Follower  .")

def composeTweet(connection, user_id, text, replyto):
	tid = random.randrange(-2147483648, 2147483647) #-2^31 to (2^31)-1

	# Check that the tweet id is unique
	while (True):
		curs = connection.cursor()
		curs.prepare("select * from tweets where tid = :tid")
		curs.execute(None, {'tid':tid})
		if curs.fetchone():
			tid = random.randrange(-2147483648, 2147483647)
		else:
			curs.close()
			break

	curs = connection.cursor()
	curs.prepare("insert into tweets values (:tid, :writer, :tdate, :text, :replyto)")
	curs.execute(None, {'tid':tid, 'writer':user_id, 'tdate':time.strftime("%d-%b-%Y"), 'text':text, 'replyto':replyto})
	curs.close()
	connection.commit()
	print("Successfully tweeted")

def retweet(connection, user_id, tweet_id):
	curs = connection.cursor()
	curs.prepare("insert into retweets values (:id, :tid, :tdate)")
	curs.execute(None, {'id':user_id, 'tid':tweet_id, 'tdate':time.strftime("%d-%b-%Y")})
	curs.close()
	connection.commit()
	print("Successfully retweeted.")

# return to users that you searched by the key word
def searchAllUsers(connection, inp):

	inp = '%' + inp + '%'
	curs = connection.cursor()

	curs.prepare("select * from (select name,usr,city from users  where name like :keyName order by length(trim(name)) asc) "
			" union  all select * from (select name,usr,city from users  where city like :keyName and name not like :keyName "
			" order by  length(trim(city)) asc)")

	curs.execute(None, {'keyName':inp})
	rows = curs.fetchall()
	curs.close()
	return rows

#the search users function. after logged in, you should be able to search any users by a key word. Thsy are
# listing by an ascending order. once you select a user, you can see any informations about the user. you can
# also have the option to follow this user.
def displayAllUsers(connection,user_id):
	inp = input("Please input a keyword   : ")
	#inp2 = input("Do you wanto to follow the user? ")
	rows = searchAllUsers(connection, inp)
	#follow = followusers(connection, flwer)
	if len(rows) > 0:
		print("users list,please choose:")
		i = 1
		indices = []
		while (True):
			indices.append(i)
			print(i, rows[i-1])

			# Either 5 user have been printed or we have reached the end of the users
			if ((i%5) == 0) or (len(rows) == i):
				inp = ""

				while (True):
					# Check if we have reached the end of the users
					if len(rows) == i:
						# Check if a full 5 user were printed
						if (i%5) == 0:
							inp = input("Type numbers %s-%s to view more information about the user, "
							"or 'skip' to skip viewing the users: " % ((i-4), i))

						# Check if only a single user was printed
						elif (i%5) == 1:
							inp = input("Type number %s to view more information about the user, "
							"or 'skip' to skip viewing the users: " % (i))

						# Either 2, 3, or 4 user were printed
						else:
							inp = input("Type numbers %s-%s to view more information about the tweet, "
							"or 'skip' to skip viewing the users: " % ((i-(i%5)), i))


						# Check if the input is an int representing 1 of the user
						try:
							if int(inp) in indices:
								break
						except:
							pass
						if inp == "skip":
							break
						else:
							print("Unrecognized input, please try again.")

					# There are still more user to display so offer to display the next ones aswell
					else:
						inp = input("Type numbers %s-%s to view more information about the user, "
						"'more' to view the next 5 user, or 'skip' to skip viewing the user: " % ((i-4), i))
						# Check if the input is an int representing 1 of the user
						try:
							if int(inp) in indices:
								break

						except:
							pass
						if inp == "skip" or inp == "more":
							break

						else:
							print("Unrecognized input, please try again.")
				if inp == "skip":
					break
				elif inp == "more":
					indices = []

				# A user was selected
				else:
					displayUserStats(connection,  rows[int(inp)-1][1],user_id)
					indices = []
					if i%5 == 0:
						i = i-5
					else:
						i = i - (i%5)
			i = i + 1
	else:
		print("No suit users  .")


# return to the users status, like number of followers, number of folowing users, number of tweets
def getUserStats(connection, user_id):

	curs = connection.cursor()
	curs.prepare("select  b1.twnum,b2.fenum,b3.frnum from (select count(tid) twnum  from tweets where writer =:user1 ) b1 ,"
		"(select  count(flwer) fenum from follows  where  flwee = :user1 ) b2,"
		"(select  count(flwee) frnum from follows  where  flwer = :user1 ) b3   ")
	curs.execute(None, {'user1':user_id })
	row = curs.fetchone()
	curs.close()
	return row

# return to the tweets ordered by recent updated
def getUserTweets(connection, user_id):
	curs = connection.cursor()
	curs.prepare("select *   from tweets  where writer= :user1 order by tdate desc ")
	curs.execute(None, {'user1':user_id })
	row = curs.fetchall()
	curs.close()
	return row

#display the users users status, like number of followers, number of folowing users, number of 3 recent tweets
def displayUserStats(connection, user,user_id):

	stats = getUserStats(connection, user)
	print("the number of tweets is ",stats[0]," the number of users being followed is ",stats[1],"the number of followers is " ,stats[2])
	rows = getUserTweets(connection,user)
	inp = ""
	if len(rows) > 0:
		print("tweets list,please choose:")
		i = 1
		indices = []
		while (True):
			indices.append(i)
			print(i, rows[i-1])

			# Either 3 tweets have been printed or we have reached the end of the tweets
			if ((i%3) == 0) or (len(rows) == i):
				inp = ""
				while (True):
					# Check if we have reached the end of the tweets/retweets
					if len(rows) == i:
						# Check if a full 3 tweets were printed
						if (i%3) == 0:
							inp = input("Type 'skip' to skip viewing the tweets,or 'follow' to follow the user:  " )
						# Check if only a single tweet was printed
						elif (i%3) == 1:
							inp = input("Type skip' to skip viewing the tweets,or 'follow' to follow the user: " )
						# Either 2, 3 twees were printed
						else:
							inp = input("Type skip' to skip viewing the tweets,or 'follow' to follow the user: " )

						# Check if the input is an int representing 1 of the user
						try:
							if int(inp) in indices:
								break
						except:
							pass
						if inp == "skip" or inp == "follow" :
							break
						else:
							print("Unrecognized input, please try again.")

					# There are still more user to display so offer to display the next ones aswell
					else:
						inp = input("Type 'more' to view the next 5 tweets, or 'skip' to skip viewing the user,or 'follow' to follow the user: " % ((i-2), i))

						# Check if the input is an int representing 1 of the user
						try:
							if int(inp) in indices:
								break
						except:
							pass
						if inp == "skip" or inp == "more":
							break
						else:
							print("Unrecognized input, please try again.")
				if inp == "skip":
					break
				elif inp == "more":
					indices = []
				elif inp == "follow":
					followUsers(connection, rows[i-1][1],user_id)
					break
				# A user was selected
				else:
					displayUserStats(connection,  rows[int(inp)-1][1])
					indices = []
					if i%3 == 0:
						i = i-3
					else:
						i = i - (i%3)
			i = i + 1


	else:
		print("No tweet.")

		while(True):
			inp = input("Type 'follow' to follow the user: or 'skip' to skip viewing the follower: " )
			if inp == "skip":
				break
			elif inp == "follow":
				followUsers(connection, user,user_id)
				break
			else:
			       print("Unrecognized input, please try again.")


def main():
	connection = getConnection()
	ret = loginOrCreatePrompt(connection)
	createdAccount = ret[0]
	user_id = ret[1]

	if not createdAccount:
		displayTweetsAndRetweets(connection, user_id)

	while (True):
		inp = input("Type 'search tweets' to search tweets, 'search users' to search users, 'compose tweet' to write a tweet, 'list followers' to list your followers, 'manage lists' to see lists, or 'logout' to logout: ")

		if inp == "search tweets":
			break

		elif inp == "search users":
			displayAllUsers(connection,user_id)


		elif inp == "compose tweet":
			break

		elif inp == "list followers":
			displayAllFollowers(connection,user_id)


		elif inp == "manage lists":
			break

		elif inp == "logout":
			break

		else:
			print("Unrecognized input, please try again.")

	connection.commit()
	connection.close()

if __name__ == "__main__":
	main()
