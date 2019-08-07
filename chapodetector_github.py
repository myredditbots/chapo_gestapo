'''
/u/chapo_gestapo (he/him)

Maintained by main account /u/GimmeFuel_GimmeGuy

This is a automated bot that digs into a user's comment history and determines if they're a Chapo poster. 
The bot is called by pinging /u/chapo_gestapo in a reply comment to the user. At the moment, it responds to requests in any subreddit.
If the user is a Chapo poster, it prints out detailed stuff
about the user like:

* Number of Chapo Comments
* Average score of comments
* Best comment
* Worst comment

Ping syntax

/u/chapo_gestapo [username]

Honestly, I dont really give a fuck if anyone copies this shit and steals it for their own bot. I fucking suck at Guython, and most of this shit can
be written better, so take it and do whatever you want with it. I'm throwing this up as open source, so if the original /u/chapo_gestapo bot gets shut down
someone can literally just download this .py, change some of the Oauth information, and have it running again.
'''


import praw
import time, random

#Reddit setup
reddit = praw.Reddit("Reddit Stuff")

def main():
	while True:
		for message in reddit.inbox.unread(limit=None):
			subject = message.subject.lower()
			if subject == 'username mention' and isinstance(message, praw.models.Comment):
				try:
					reply = investigate(message.body.split()[1].replace("\\", ""))
					print("Mention found, replying...")
					message.reply(reply)
				except:
					print("Invalid syntax")
				finally:
					message.mark_read()
	sleep(5)

def investigate(user):
	#------------Debug and Shit----------------
	print("Investigating: " + user)
	if(user == "chapo_gestapo"):
		return "Let me check really quick... hmmm.... says here **you're gay**"
	
	
	#----------Setup Variables-----------------
	rand = random.randrange(10) #For a little 'spice'
	suspect = reddit.redditor(user)
	output = ""
	reddit.subreddit('chapotraphouse').quaran.opt_in() #ChapoFagHouse got got, so we have to opt in for the (Quran)tine
	
	
	#---------Statistics Variables---------------
	
	#Average
	average_score = 0
	i = 0 #Comment counter for average, incase they have less comments as the limit
	count = 0 #Number of Chapo posts
	
	#Best and worst comments
	best_comment = {"score": 0, "body": "error", "url":"gayporn.com"}
	worst_comment = {"score": 0, "body": "error", "url":"gayporn.com"}
	most_recent = {"score": 0, "body": "error", "url":"gayporn.com", "date":"4/20/69"}
	first_comment = True
	
	#Other subs (list needs to be expanded)
	other_subs = {"smalldickproblems": 0, "redscarepod":0, "chapotraphouse2":0, "SandersForPresident": 0, "LateStageCapitalism":0}
	has_other_subs = False
	
	my_dick_is_small = True
	
	#----------Actual Bullshit-------------------
	
	#Grab the last 100 comments
	for comment in suspect.comments.new(limit=100):
	
		#Processing for chapo posts
		if(comment.subreddit.display_name == "ChapoTrapHouse"):
		
		
			#Perform work for the comment score average
			average_score += comment.score
			i += 1
			count += 1
			
			#Performs setup of structures if it's the user's first comment
			if(first_comment):
				best_comment = {"score": comment.score, "body": comment.body, "url": "https://np.reddit.com"+comment.permalink}
				worst_comment = best_comment
				most_recent = best_comment
				most_recent["date"] = date.fromtimestamp(int(comment.created_utc)) #This sucks balls
				
				first_comment = False
			
			#Handles best/worst comment handling
			else:
				if(comment.score > best_comment["score"]):
					best_comment = {"score": comment.score, "body": comment.body, "url": "https://np.reddit.com"+comment.permalink}
				if(comment.score < worst_comment["score"]):
					worst_comment = {"score": comment.score, "body": comment.body, "url": "https://np.reddit.com"+comment.permalink}
		
		#Processing for 'other subs'
		else:
			for sub in other_subs:
				if(sub == comment.subreddit.display_name):
					other_subs[sub] += 1
					has_other_subs = True
			i += 1 #Increment the number of posts counted
			
	
	#-------------Output Formatting---------------------
	
	if(count == 0):
		output= "This user has not posted in /r/ChapoTrapHouse"
	else:
		if(rand == 4):
			output += "**POINT OF PERSONAL PRIVILEGE: **\n\n"
		
		#Chapo Posts
		output = "**{} IS A CHAPO POSTER**\n\n".format(suspect.name.upper())
		output+= "Chapo posts: ({0}/{1}) with an average score of {2:.0f}\n\n".format(count,i,average_score/count)
		
		#Other subs
		if(has_other_subs):
			output += "This user also posts in the following subs: \n\n"
			for sub in other_subs:
				if other_subs[sub] > 0:
					output += "* {} : {}\n\n".format(sub, other_subs[sub])
		
		#Most Recent, Best and Worst comments in r/ChapoTrapHous
		
		#Most Recent
		output+= "--- \n\n[Most Recent Comment]({}) (score:{}) on {}\n\n".format(most_recent["url"], most_recent["score"], most_recent["date"])
		for line in most_recent["body"].split('\n'):
			output += ">{}\n\n".format(line)
		
		#Best Comment
		output+= "\n\n[Best comment]({}) (score:{})\n\n".format(best_comment["url"], best_comment["score"])
		for line in best_comment["body"].split('\n'):
			output += ">{}\n\n".format(line)
		
		#Worst Comment
		output+= "[Worst comment]({}) (score:{})\n\n\n".format(worst_comment["url"],worst_comment["score"])
		for line in worst_comment["body"].split('\n'):
			output += ">{}\n\n".format(line)
		
		
		#Footer
		output+= "---\n\nBot is maintained by /u/GimmeFuel_GimmeGuy. If shit breaks, message him. Also, this bot is [open source](). "
		if(rand == 8):
			output+= "You can help this bot by DMing it pics of your juicy milkers, or PAAGs."
		if(rand == 6):
			output+="https://www.youtube.com/watch?v=ryJteQTPBlU"
		if(rand == 3):
			output+= "[Gayest redditor on the planet](https://www.reddit.com/user/me)"
		
		#Final sanitization
		output.replace("www.reddit", "np.reddit")
		output = output[:9999]
	return output

main()
