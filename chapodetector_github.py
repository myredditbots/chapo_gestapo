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

	print("Investigating " + user)
	
	
	rand = random.randrange(10)
	suspect = reddit.redditor(user)
	reddit.subreddit('chapotraphouse').quaran.opt_in() #ChapoFagHouse got got, so we have to opt in for the (Quran)tine
	
	
	#---------Statistics Variables---------------
	
	#Average
	average_score = 0
	i = 0 #Comment counter for average, incase they have less comments as the limit
	count = 0 #Number of Chapo posts
	
	#Best and worst comments
	best_comment = {"score": 0, "body": "error", "url":"gayporn.com"}
	worst_comment = {"score": 1, "body": "error", "url":"gayporn.com"}
	first_comment = True
	my_dick_is_small = True
	
	#----------Actual Bullshit-------------------
	
	#Grab the last 100 comments
	for comment in suspect.comments.new(limit=100):
		if(comment.subreddit.display_name == "ChapoTrapHouse"):
		
		
			#Perform work for the comment score average
			average_score += comment.score
			i += 1
			count += 1
			
			#Performs setup of structures if it's the user's first comment
			if(first_comment):
				best_comment = {"score": comment.score, "body": comment.body, "url": "https://np.reddit.com"+comment.permalink}
				worst_comment = best_comment
				first_comment = False
			
			#Handles best/worst comment handling
			else:
				if(comment.score > best_comment["score"]):
					best_comment = {"score": comment.score, "body": comment.body, "url": "https://np.reddit.com"+comment.permalink}
				if(comment.score < worst_comment["score"]):
					worst_comment = {"score": comment.score, "body": comment.body, "url": "https://np.reddit.com"+comment.permalink}
		else:
			i += 1
			
	
	#-------------Output Formatting---------------------
	
	if(count == 0):
		output= "This user has not posted in /r/ChapoTrapHouse"
	else:
		if(rand == 4):
			output += "**POINT OF PERSONAL PRIVILEGE: **\n\n"
		output = "**{} IS A CHAPO POSTER**\n\n".format(suspect.name.upper())
		output+= "Chapo posts: ({0}/{1}) with an average score of {2:.0f}\n\n --- \n\n".format(count,i,average_score/count)
		output+= "[Best comment]({}) (score:{})\n\n".format(best_comment["url"], best_comment["score"])
		output+= "> {}\n\n".format(best_comment["body"].split('\n')[0])
		output+= "[Worst comment]({}) (score:{})\n\n\n".format(worst_comment["url"],worst_comment["score"])
		output+= "> {}\n\n".format(worst_comment["body"].split('\n')[0])
		output+= "---\n\nBot is maintained by /u/GimmeFuel_GimmeGuy. If shit breaks, message him. Also, this bot is open source."
		if(rand == 8):
			output+= "You can help this bot by DMing it pics of your juicy milkers, or PAAGs."
		if(rand == 6):
			output+="https://www.youtube.com/watch?v=ryJteQTPBlU"
	return output

	
main()