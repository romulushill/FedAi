#mstdn.py#
from mastodon import Mastodon
import random
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#print(mastodon.notifications())
#notifications = mastodon.notifications()
#for notification in notifications:



class RootApp:

    def __init__(self,authkey=None,target=None):
        try:
            self.mastodon = Mastodon(
                access_token = 'ccIFo24VX7O2IkoknpcPzUmdxXszJQ922HqW3at1LnY',
                api_base_url = 'https://techhub.social'
            )

            print(f"Authenticated RootApp - Mastodon.")
            self.conversation = ["What have you been doing lately?","what brings you to Mastodon?","If I said 'yellow' what would you say?","Is anybody else a huge fan of AI?","What weird food combinations do you really enjoy?","What social stigma does society need to get over?","What food have you never eaten but would really like to try?","What’s something you really resent paying for?","What would a world populated by clones of you be like?","Do you think that aliens exist?","What are you currently worried about?","Where are some unusual places you’ve been?","Where do you get your news?","What are some red flags to watch out for in daily life?","What movie can you watch over and over without ever getting tired of?","When you are old, what do you think children will ask you to tell stories about?","If you could switch two movie characters, what switch would lead to the most inappropriate movies?","What inanimate object would be the most annoying if it played loud upbeat music while being used?","When did something start out badly for you but in the end, it was great?","How would your country change if everyone, regardless of age, could vote?","What animal would be cutest if scaled down to the size of a cat?","If your job gave you a surprise three day paid break to rest and recuperate, what would you do with those three days?","What’s wrong but sounds right?","What’s the most epic way you’ve seen someone quit or be fired?","If you couldn’t be convicted of any one type of crime, what criminal charge would you like to be immune to?","What’s something that will always be in fashion, no matter how much time passes?","What actors or actresses play the same character in almost every movie or show they do?","In the past people were buried with the items they would need in the afterlife, what would you want buried with you so you could use it in the afterlife?","What’s the best / worst practical joke that you’ve played on someone or that was played on you?","Who do you go out of your way to be nice to?","Where do you get most of the decorations for your home?","What food is delicious but a pain to eat?","Who was your craziest / most interesting teacher","What ' old person' things do you do?","What was the last photo you took?","What is the most amazing slow motion video you’ve seen?","Which celebrity do you think is the most down to earth?","What would be the worst thing to hear as you are going under anesthesia before heart surgery?","What’s the spiciest thing you’ve ever eaten?","What’s the most expensive thing you’ve broken?","What obstacles would be included in the World’s most amazing obstacle course?","What makes you roll your eyes every time you hear it?","What do you think you are much better at than you actually are?","Should kidneys be able to be bought and sold?","What’s the most creative use of emojis you’ve ever seen?","When was the last time you got to tell someone “I told you so.”?","What riddles do you know?","What’s your cure for hiccups?","What invention doesn’t get a lot of love, but has greatly improved the world?","What’s the most interesting building you’ve ever seen or been in?","What mythical creature do you wish actually existed?","What are your most important rules when going on a date?","How do you judge a person?","If someone narrated your life, who would you want to be the narrator?","What was the most unsettling film you’ve seen?","What unethical experiment would have the biggest positive impact on society as a whole?","When was the last time you were snooping, and found something you wish you hadn’t?","Which celebrity or band has the worst fan base?","What are you interested in that most people aren’t?","If you were given a PhD degree, but had no more knowledge of the subject of the degree besides what you have now, what degree would you want to be given to you?","What smartphone feature would you actually be excited for a company to implement?","What’s something people don’t worry about but really should?","What movie quotes do you use on a regular basis?","Do you think that children born today will have better or worse lives than their parents?","What’s the funniest joke you know by heart?","When was the last time you felt you had a new lease on life?","What’s the funniest actual name you’ve heard of someone having?","Which charity or charitable cause is most deserving of money?","What TV show character would it be the most fun to change places with for a week?","What was cool when you were young but isn’t cool now?","If you were moving to another country, but could only pack one carry-on sized bag, what would you pack?","What’s the most ironic thing you’ve seen happen?","If magic was real, what spell would you try to learn first?","If you were a ghost and could possess people, what would you make them do?","What goal do you think humanity is not focused enough on achieving?"]
            self.pollq = []
            with open("PollQuestions.txt",'r',encoding='utf-8') as data_file:
                for line in data_file:
                    self.pollq.append(line)
            self.active = True
        except:
            print("Failed authentication of RootApp - Mastodon.")
            self.active = False

    def message(self,content,pollobj=None,in_reply_to_id=None,visibility="public"):
        error_count = 0
        completed = False
        while ((completed == False) and (error_count < 3)):
            print(f"[message_func]: Calling post")
            time.sleep(1)
            try:
                if self.mastodon.ratelimit_remaining > 0:
                    resp = self.mastodon.status_post(status=content,in_reply_to_id=in_reply_to_id,visibility=visibility,poll=pollobj)
                    completed = True
                    print("[message_func]: Completed toot")
                    return resp
                else:
                    print("[message_func]: Failed toot")
                    completed = False
                    error_count+=1
            except:
                completed = False
                error_count+=1

        print(f"[message_func]: Failed toot - attempted {error_count}")
        return None



    def listener(self):
        ready = False
        try:
            lastnotification = self.mastodon.notifications()[0]["id"]
            ready = True
        except:
            print("Unable to fetch last notification")
            ready = False
            pass
        while ((ready == True) and (self.active == True)):
            try:
                time.sleep(1)
                current = self.mastodon.notifications()[0]["id"]
                if current != lastnotification:
                    notification = self.mastodon.notifications()[0]
                    event = notification["type"]
                    user = notification["account"]
                    username = user["username"]
                    userid = user["id"]
                    acct = (f'@{user["acct"]}')
                    if event == "follow":
                        print("Detected Follow")
                        try:
                            self.mastodon.account_follow(userid)
                            print(f"Followed {username}")
                            lastnotification = current
                        except:
                            print(f"Failed Follow Re-Follow")
                            lastnotification = current
                            pass
                    elif event =="favourite":
                        print("Detected Favourite")
                        try:
                            messageid = int(self.mastodon.notifications()[0]["status"]["id"])
                            self.message(f"{acct} Thanks for the favourite!",in_reply_to_id=messageid,visibility="direct")
                            print(f"Tooted Favourite Thanks For {username}")
                            lastnotification = current
                        except:
                            print(f"Failed Favourite Toot")
                            lastnotification = current
                            pass
                    elif event == "reblog":
                        print("Detected Reblog")
                        try:
                            #msglink = notification["status"]["uri"]
                            messageid = int(self.mastodon.notifications()[0]["status"]["id"])
                            self.message(f"{acct} Thanks for the boost!",in_reply_to_id=messageid,visibility="direct")
                            print(f"Tooted Boost Thanks For {username}")
                            lastnotification = current

                        except:
                            print(f"Failed Boost Toot")
                            lastnotification = current
                            pass
                    elif event == "mention":
                        print("Detected Mention")
                        try:
                            messageid = int(self.mastodon.notifications()[0]["status"]["id"])
                            self.message(f"{acct} Thanks for the mention, whats up?\nRemember, I am a Neural Network therefore my responses are limited and I will learn from your dialogue too!",in_reply_to_id=messageid,visibility="unlisted")
                            print("Responded to a mention")
                            lastnotification = current
                        except:
                            print("Failed Mention Response")
                            lastnotification = current
                            pass

                    elif event == "poll":
                        print("Detected Poll")
                        try:
                            pass
                            #print(self.mastodon.notifications()[0])
                            #lastnotification = current
                        except:
                            print("Failed Poll Collection")
                            lastnotification = current
                            pass
                    else:
                        pass
                    
                    print(f"{user['username']} performed a {event}")
                else:
                    pass
            except:
                pass

    def start_listener(self):
        self.events = threading.Thread(target=self.listener)
        self.events.start()

    def chat(self):
        op = 2
        while self.active == True:
            error_count = 0
            try:
                if self.mastodon.ratelimit_remaining > 1:
                    

                    if op == 1:
                        print("Preparing to assemble a Question.")
                        choice = random.choice(self.conversation)
                        print(f"Chosen statement: {choice}")
                        try:
                            completed = False
                            while ((completed != True)and(error_count < 3)):
                                time.sleep(1)
                                try:
                                    print(f"Preparing to deploy toot")
                                    response = self.message(f"{choice}\nPlease reply to help me learn!")
                                    tootid = response["id"]
                                    print(f"Tooted: {choice}\nReturned: {tootid}")
                                    completed = True
                                    op = 2
                                except:
                                    print("Failed toot - Retrying")
                                    completed = False
                                    error_count+=1
                                    op = 2
                        except:
                            print("Toot Error Occured")
                            error_count+=1
                            op = 2
                    else:
                        print("Preparing to assemble a Poll.")
                        choice1 = (random.choice(self.pollq))
                        choice2 = (random.choice(self.pollq))
                        choice3 = (random.choice(self.pollq))
                        setoptions = [choice1,choice2,choice3]
                        print(setoptions)
                        while ((len(choice1) > 49) or (len(choice2) > 49) or (len(choice3) > 49)):
                            print("A chosen selector does not conform with size limits.")
                            if len(choice1) >49:
                                del setoptions[0]
                                new = (random.choice(self.pollq))
                                setoptions.append(new)
                                choice1 = setoptions[0]
                            elif len(choice2) >49:
                                del setoptions[1]
                                new = (random.choice(self.pollq))
                                setoptions.append(new)
                                choice2 = setoptions[1]
                            elif len(choice3) >49:
                                del setoptions[2]
                                new = (random.choice(self.pollq))
                                setoptions.append(new)
                                choice3 = setoptions[2]

                        try:
                            completed = False
                            while ((completed != True)and(error_count < 3)):
                                time.sleep(1)
                                try:
                                    assembly = self.mastodon.make_poll(options=setoptions,expires_in=300,multiple=True)

                                    print(f"Preparing to deploy poll: {setoptions}")

                                    response = self.message(content=f"Select the most appropriate conversation starters!",pollobj=assembly)
                                    tootid = response["id"]
                                    print(f"Tooted Poll\nReturned: {tootid}")
                                    completed = True
                                    op = 1
                                except:
                                    print("Failed toot - Retrying")
                                    completed = False
                                    error_count+=1
                                    op = 1
                        except:
                            print("Toot Error Occured")
                            error_count+=1
                            op = 1

                    time.sleep(random.randint(180,240))
            except:
                print(f"General Error Occured, Ratelimit At The Time: {self.mastodon.ratelimit_remaining}")




token = 'ccIFo24VX7O2IkoknpcPzUmdxXszJQ922HqW3at1LnY',
url = 'https://techhub.social'
Main = RootApp(token,url)
Main.start_listener()
Main.chat()